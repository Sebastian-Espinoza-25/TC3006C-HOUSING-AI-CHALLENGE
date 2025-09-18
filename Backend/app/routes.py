from flask import Blueprint, request, jsonify
from .services import ClientService, VendorService, HouseService, PreferencesService

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({
        "message": "HouseLink API corriendo 🚀",
        "version": "1.0.0",
        "endpoints": {
            # Clients
            "list_clients": "GET /api/clients",
            "get_client": "GET /api/clients/<client_id>",
            "create_client": "POST /api/clients",
            "update_client": "PUT /api/clients/<client_id>",
            "delete_client": "DELETE /api/clients/<client_id>",
            # Vendors
            "list_vendors": "GET /api/vendors",
            "get_vendor": "GET /api/vendors/<vendor_id>",
            "create_vendor": "POST /api/vendors",
            "update_vendor": "PUT /api/vendors/<vendor_id>",
            "delete_vendor": "DELETE /api/vendors/<vendor_id>",
            # Houses
            "create_house_for_vendor": "POST /api/vendors/<vendor_id>/houses",
            "delete_house": "DELETE /api/houses/<house_id>",
            # Preferences / Matching
            "create_or_update_preferences": "POST /api/clients/<client_id>/preferences",
            "delete_preferences": "DELETE /api/clients/<client_id>/preferences",
            "recommendations": "GET /api/clients/<client_id>/recommendations"
        }
    })

# CLIENTS

@main.route("/api/clients", methods=["GET"])
def get_clients():
    try:
        return jsonify(ClientService.get_all_clients())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    try:
        client = ClientService.get_client_by_id(client_id)
        if client:
            return jsonify(client)
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients", methods=["POST"])
def create_client():
    try:
        data = request.get_json(silent=True) or {}
        for field in ("username", "email", "password"):
            if not data.get(field):
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        created = ClientService.create_client(data)
        return jsonify(created), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    try:
        data = request.get_json(silent=True) or {}
        updated = ClientService.update_client(client_id, data)
        if updated:
            return jsonify(updated)
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        ok = ClientService.delete_client(client_id)
        if ok:
            return jsonify({"message": "Cliente eliminado correctamente"})
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# VENDORS 

@main.route("/api/vendors", methods=["GET"])
def get_vendors():
    try:
        return jsonify(VendorService.get_all_vendors())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>", methods=["GET"])
def get_vendor(vendor_id):
    try:
        vendor = VendorService.get_vendor_by_id(vendor_id)
        if vendor:
            return jsonify(vendor)
        return jsonify({"error": "Vendedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors", methods=["POST"])
def create_vendor():
    try:
        data = request.get_json(silent=True) or {}
        for field in ("username", "email", "password"):
            if not data.get(field):
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        created = VendorService.create_vendor(data)
        return jsonify(created), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>", methods=["PUT"])
def update_vendor(vendor_id):
    try:
        data = request.get_json(silent=True) or {}
        updated = VendorService.update_vendor(vendor_id, data)
        if updated:
            return jsonify(updated)
        return jsonify({"error": "Vendedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>", methods=["DELETE"])
def delete_vendor(vendor_id):
    try:
        ok = VendorService.delete_vendor(vendor_id)
        if ok:
            return jsonify({"message": "Vendedor eliminado correctamente"})
        return jsonify({"error": "Vendedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HOUSES

@main.route("/api/vendors/<int:vendor_id>/houses", methods=["POST"])
def create_house(vendor_id):
    """
    Crear una casa (recuerda: usar después de predecir el precio).
    Requiere al menos: title, sale_price.
    """
    try:
        data = request.get_json(silent=True) or {}
        if not data.get("title"):
            return jsonify({"error": "Campo requerido: title"}), 400
        if data.get("sale_price") is None:
            return jsonify({"error": "Campo requerido: sale_price"}), 400

        created = HouseService.create_house(vendor_id, data)
        if created is None:
            return jsonify({"error": "Vendedor no encontrado"}), 404
        return jsonify(created), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/houses/<int:house_id>", methods=["DELETE"])
def delete_house(house_id):
    try:
        ok = HouseService.delete_house(house_id)
        if ok:
            return jsonify({"message": "Casa eliminada correctamente"})
        return jsonify({"error": "Casa no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PREFERENCES/ MATCHING 

@main.route("/api/clients/<int:client_id>/preferences", methods=["POST"])
def create_or_update_preferences(client_id):
    try:
        data = request.get_json(silent=True) or {}
        prefs = PreferencesService.create_preference(client_id, data)
        if prefs is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(prefs), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>/preferences", methods=["DELETE"])
def delete_preferences(client_id):
    try:
        ok = PreferencesService.delete_preference(client_id)
        if ok:
            return jsonify({"message": "Preferencias eliminadas correctamente"})
        return jsonify({"error": "Preferencias no encontradas"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>/recommendations", methods=["GET"])
def get_recommendations(client_id):
    try:
        result = PreferencesService.find_matching_houses(client_id)
        # result: {'client': {...}|None, 'matches': [...], 'preferences_applied': {...}|None}
        if result.get("client") is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
