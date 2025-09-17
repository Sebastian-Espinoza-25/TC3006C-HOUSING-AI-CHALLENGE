from flask import Blueprint, request, jsonify
from .services import ClientService, VendorService, HouseService, PreferencesService
from .models import Client, Vendor, ClientPreferences, VendorHouse
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({
        "message": "HouseLink API corriendo 🚀",
        "version": "1.0.0",
        "endpoints": {
            "clients": "/api/clients",
            "vendors": "/api/vendors", 
            "houses": "/api/houses",
            "preferences": "/api/preferences",
            "search": "/api/search"
        }
    })

# ==================== RUTAS DE CLIENTES ====================

@main.route("/api/clients", methods=["GET"])
def get_clients():
    """Obtener todos los clientes"""
    try:
        clients = ClientService.get_all_clients()
        return jsonify(clients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    """Obtener un cliente específico por ID"""
    try:
        client = ClientService.get_client_by_id(client_id)
        if client:
            return jsonify(client)
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients", methods=["POST"])
def create_client():
    """Crear un nuevo cliente"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        
        client = ClientService.create_client(data)
        return jsonify(client), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    """Actualizar un cliente existente"""
    try:
        data = request.get_json()
        client = ClientService.update_client(client_id, data)
        if client:
            return jsonify(client)
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== RUTAS DE VENDEDORES ====================

@main.route("/api/vendors", methods=["GET"])
def get_vendors():
    """Obtener todos los vendedores"""
    try:
        vendors = VendorService.get_all_vendors()
        return jsonify(vendors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>", methods=["GET"])
def get_vendor(vendor_id):
    """Obtener un vendedor específico por ID"""
    try:
        vendor = VendorService.get_vendor_by_id(vendor_id)
        if vendor:
            return jsonify(vendor)
        return jsonify({"error": "Vendedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors", methods=["POST"])
def create_vendor():
    """Crear un nuevo vendedor"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        
        vendor = VendorService.create_vendor(data)
        return jsonify(vendor), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>", methods=["PUT"])
def update_vendor(vendor_id):
    """Actualizar un vendedor existente"""
    try:
        data = request.get_json()
        vendor = VendorService.update_vendor(vendor_id, data)
        if vendor:
            return jsonify(vendor)
        return jsonify({"error": "Vendedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== RUTAS DE CASAS ====================

@main.route("/api/houses", methods=["GET"])
def get_houses():
    """Obtener todas las casas con filtros y paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros
        filters = {}
        if request.args.get('property_type'):
            filters['property_type'] = request.args.get('property_type')
        if request.args.get('min_price'):
            filters['min_price'] = request.args.get('min_price')
        if request.args.get('max_price'):
            filters['max_price'] = request.args.get('max_price')
        if request.args.get('bedrooms'):
            filters['bedrooms'] = int(request.args.get('bedrooms'))
        if request.args.get('bathrooms'):
            filters['bathrooms'] = int(request.args.get('bathrooms'))
        if request.args.get('location'):
            filters['location'] = request.args.get('location')
        if request.args.get('min_area'):
            filters['min_area'] = float(request.args.get('min_area'))
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('is_featured'):
            filters['is_featured'] = request.args.get('is_featured').lower() == 'true'
        
        result = HouseService.get_all_houses(page, per_page, filters)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/houses/<int:house_id>", methods=["GET"])
def get_house(house_id):
    """Obtener una casa específica por ID"""
    try:
        house = HouseService.get_house_by_id(house_id)
        if house:
            return jsonify(house)
        return jsonify({"error": "Casa no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>/houses", methods=["GET"])
def get_vendor_houses(vendor_id):
    """Obtener casas de un vendedor específico"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = HouseService.get_houses_by_vendor(vendor_id, page, per_page)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/vendors/<int:vendor_id>/houses", methods=["POST"])
def create_house(vendor_id):
    """Crear una nueva casa para un vendedor"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['title', 'price', 'bedrooms', 'bathrooms', 'area', 'property_type', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        
        house = HouseService.create_house(vendor_id, data)
        return jsonify(house), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/houses/<int:house_id>", methods=["PUT"])
def update_house(house_id):
    """Actualizar una casa existente"""
    try:
        data = request.get_json()
        house = HouseService.update_house(house_id, data)
        if house:
            return jsonify(house)
        return jsonify({"error": "Casa no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/houses/<int:house_id>", methods=["DELETE"])
def delete_house(house_id):
    """Eliminar una casa"""
    try:
        success = HouseService.delete_house(house_id)
        if success:
            return jsonify({"message": "Casa eliminada correctamente"})
        return jsonify({"error": "Casa no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== RUTAS DE PREFERENCIAS ====================

@main.route("/api/clients/<int:client_id>/preferences", methods=["GET"])
def get_client_preferences(client_id):
    """Obtener preferencias de un cliente"""
    try:
        preferences = PreferencesService.get_client_preferences(client_id)
        if preferences:
            return jsonify(preferences)
        return jsonify({"message": "No se encontraron preferencias para este cliente"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>/preferences", methods=["POST"])
def create_or_update_preferences(client_id):
    """Crear o actualizar preferencias de un cliente"""
    try:
        data = request.get_json()
        preferences = PreferencesService.create_or_update_preferences(client_id, data)
        return jsonify(preferences), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>/recommendations", methods=["GET"])
def get_client_recommendations(client_id):
    """Obtener recomendaciones de casas para un cliente basadas en sus preferencias"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = PreferencesService.find_matching_houses(client_id, page, per_page)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== RUTAS DE BÚSQUEDA ====================

@main.route("/api/search", methods=["GET"])
def search_houses():
    """Buscar casas por texto"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({"error": "Parámetro de búsqueda requerido"}), 400
        
        # Filtros adicionales
        filters = {}
        if request.args.get('property_type'):
            filters['property_type'] = request.args.get('property_type')
        if request.args.get('min_price'):
            filters['min_price'] = request.args.get('min_price')
        if request.args.get('max_price'):
            filters['max_price'] = request.args.get('max_price')
        
        houses = HouseService.search_houses(query, filters)
        
        return jsonify({
            "query": query,
            "filters": filters,
            "results": houses,
            "count": len(houses)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== RUTAS DE ESTADÍSTICAS ====================

@main.route("/api/stats", methods=["GET"])
def get_stats():
    """Obtener estadísticas generales del sistema"""
    try:
        total_clients = Client.query.count()
        total_vendors = Vendor.query.count()
        total_houses = VendorHouse.query.count()
        
        # Casas por tipo
        house_types = db.session.query(
            VendorHouse.property_type, 
            db.func.count(VendorHouse.house_id)
        ).group_by(VendorHouse.property_type).all()
        
        # Casas por estado
        house_status = db.session.query(
            VendorHouse.status, 
            db.func.count(VendorHouse.house_id)
        ).group_by(VendorHouse.status).all()
        
        return jsonify({
            "total_clients": total_clients,
            "total_vendors": total_vendors,
            "total_houses": total_houses,
            "house_types": dict(house_types),
            "house_status": dict(house_status)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
