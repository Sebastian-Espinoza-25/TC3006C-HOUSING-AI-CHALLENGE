# app/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt, get_jwt_identity
)
from .services import ClientService, VendorService
from .models import Client, Vendor
from . import db

auth_bp = Blueprint("auth", __name__)

def _identity_payload(role, user_id):
    # Lo que quieras llevar en el token
    return {"role": role, "id": user_id}

@auth_bp.post("/login")
def login():
    """
    Body: { "identifier": "<email o username>", "password": "..." , "role": "client|vendor|auto" }
    - role=auto buscará primero cliente y luego vendor
    """
    data = request.get_json() or {}
    identifier = data.get("identifier")
    password   = data.get("password")
    role       = (data.get("role") or "auto").lower()

    if not identifier or not password:
        return jsonify({"error": "identifier y password son requeridos"}), 400

    user = None
    resolved_role = None

    if role in ("client", "cliente"):
        user = ClientService.verify_client_credentials(identifier, password)
        resolved_role = "client" if user else None
    elif role in ("vendor", "vendedor"):
        user = VendorService.verify_vendor_credentials(identifier, password)
        resolved_role = "vendor" if user else None
    else:  # auto
        user = ClientService.verify_client_credentials(identifier, password)
        resolved_role = "client" if user else None
        if not user:
            user = VendorService.verify_vendor_credentials(identifier, password)
            resolved_role = "vendor" if user else None

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    identity = _identity_payload(resolved_role, user.client_id if resolved_role=="client" else user.vendor_id)
    access_token  = create_access_token(identity=identity, additional_claims=identity)
    refresh_token = create_refresh_token(identity=identity)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "role": resolved_role,
            **(user.to_dict())
        }
    })

@auth_bp.get("/me")
@jwt_required()
def me():
    ident = get_jwt_identity()  # {"role":..., "id":...}
    role = ident.get("role")
    uid  = ident.get("id")

    if role == "client":
        user = Client.query.get(uid)
    else:
        user = Vendor.query.get(uid)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"role": role, "user": user.to_dict()})

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    ident = get_jwt_identity()
    claims = get_jwt()  # por si quieres leer más cosas
    access_token = create_access_token(identity=ident, additional_claims=ident)
    return jsonify({"access_token": access_token})