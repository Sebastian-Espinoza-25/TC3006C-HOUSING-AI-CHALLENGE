# app/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt, get_jwt_identity
)
from .services import ClientService, VendorService
from .models import Client, Vendor

auth_bp = Blueprint("auth", __name__)

def _identity_payload(role: str, user_id: int):
    # Lo que se guardará en el token
    return {"role": role, "id": user_id}

@auth_bp.post("/login")
def login():
    """
    Body: { "identifier": "<email o username>", "password": "..." , "role": "client|vendor|auto" }
    role=auto: intenta primero como cliente y luego como vendor
    """
    data = request.get_json() or {}
    identifier = data.get("identifier")
    password   = data.get("password")
    role       = (data.get("role") or "auto").lower()

    if not identifier or not password:
        return jsonify({"error": "identifier y password son requeridos"}), 400

    user_dict = None
    resolved_role = None

    if role in ("client", "cliente"):
        user_dict = ClientService.authenticate(identifier, password)
        resolved_role = "client" if user_dict else None
    elif role in ("vendor", "vendedor"):
        user_dict = VendorService.authenticate(identifier, password)
        resolved_role = "vendor" if user_dict else None
    else:  # auto
        user_dict = ClientService.authenticate(identifier, password)
        resolved_role = "client" if user_dict else None
        if not user_dict:
            user_dict = VendorService.authenticate(identifier, password)
            resolved_role = "vendor" if user_dict else None

    if not user_dict:
        return jsonify({"error": "Credenciales inválidas"}), 401

    user_id = user_dict.get("client_id") if resolved_role == "client" else user_dict.get("vendor_id")
    ident = _identity_payload(resolved_role, user_id)

    access_token  = create_access_token(identity=ident, additional_claims=ident)
    refresh_token = create_refresh_token(identity=ident)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {**user_dict, "role": resolved_role}
    })

@auth_bp.get("/me")
@jwt_required()
def me():
    ident = get_jwt_identity()  # {"role":..., "id":...}
    role = ident.get("role")
    uid  = ident.get("id")

    user = Client.query.get(uid) if role == "client" else Vendor.query.get(uid)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"role": role, "user": user.to_dict()})

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    ident = get_jwt_identity()
    _ = get_jwt()  # por si necesitas claims
    access_token = create_access_token(identity=ident, additional_claims=ident)
    return jsonify({"access_token": access_token})
