from flask import Blueprint, request, jsonify
from .services import ClientService, VendorService, HouseService, PreferencesService, AIService
from pprint import pprint

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
            "create_specific_preferences": "POST /api/clients/<client_id>/preferences/specific",
            "delete_preferences": "DELETE /api/clients/<client_id>/preferences",
            "recommendations": "GET /api/clients/<client_id>/recommendations",
            # AI Models
            "ai_predict_complex": "POST /api/ai/predict/complex",
            "ai_predict_simple": "POST /api/ai/predict/simple",
            "ai_predict_both": "POST /api/ai/predict/both",
            "ai_models_status": "GET /api/ai/models/status"
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
        data = request.get_json() or {}
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
        pprint(data)
        prefs = PreferencesService.create_preference(client_id, data)
        if prefs is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(prefs), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/clients/<int:client_id>/preferences/specific", methods=["POST"])
def create_specific_preferences(client_id):
    """
    Crear preferencias específicas del cliente con campos limitados.
    Acepta los campos específicos de la lista proporcionada y mapea campos del JSON de predicción.
    """
    try:
        data = request.get_json(silent=True) or {}
        
        # Mapear campos del JSON de predicción a campos de preferencias
        mapped_data = {}
        
        # 1. Campos directos de la lista
        direct_fields = [
            'preferred_neighborhood', 'preferred_condition1', 'preferred_house_style',
            'min_year_built', 'max_year_built', 'min_lot_area', 'max_lot_area',
            'min_lot_frontage', 'max_lot_frontage', 'min_1st_flr_sf', 'max_1st_flr_sf',
            'min_2nd_flr_sf', 'max_2nd_flr_sf', 'min_gr_liv_area', 'max_gr_liv_area',
            'min_bedroom_abv_gr', 'max_bedroom_abv_gr', 'min_kitchen_abv_gr', 'max_kitchen_abv_gr',
            'min_tot_rms_abv_grd', 'max_tot_rms_abv_grd', 'min_full_bath', 'max_full_bath',
            'min_half_bath', 'max_half_bath', 'preferred_heating_qc', 'min_fireplaces',
            'max_fireplaces', 'min_garage_cars', 'max_garage_cars', 'min_garage_area',
            'max_garage_area', 'min_wood_deck_sf', 'max_wood_deck_sf', 'min_open_porch_sf',
            'max_open_porch_sf', 'min_enclosed_porch', 'max_enclosed_porch', 'preferred_fence',
            'min_sale_price', 'max_sale_price', 'preferred_sale_type',
            # Nuevas columnas agregadas
            'min_total_bath', 'max_total_bath', 'min_total_sf', 'max_total_sf',
            'min_remod_age', 'max_remod_age', 'min_house_age', 'max_house_age',
            'min_garage_score', 'max_garage_score', 'min_total_porch_sf', 'max_total_porch_sf',
            'min_rooms_plus_bath_eq', 'max_rooms_plus_bath_eq'
        ]
        
        # Copiar campos directos si existen en el JSON
        for field in direct_fields:
            if field in data:
                mapped_data[field] = data[field]
        
        # 2. Mapear campos del JSON de predicción a campos de preferencias
        json_mapping = {
            'Neighborhood': 'preferred_neighborhood',
            'YearBuilt': 'min_year_built',  # Usar como min_year_built
            'YearBuilt': 'max_year_built',  # También como max_year_built
            'LotArea': 'min_lot_area',     # Usar como min_lot_area
            'LotArea': 'max_lot_area',     # También como max_lot_area
            '1stFlrSF': 'min_1st_flr_sf',  # Usar como min_1st_flr_sf
            '1stFlrSF': 'max_1st_flr_sf',  # También como max_1st_flr_sf
            '2ndFlrSF': 'min_2nd_flr_sf',  # Usar como min_2nd_flr_sf
            '2ndFlrSF': 'max_2nd_flr_sf',  # También como max_2nd_flr_sf
            'GrLivArea': 'min_gr_liv_area', # Usar como min_gr_liv_area
            'GrLivArea': 'max_gr_liv_area', # También como max_gr_liv_area
            'Fireplaces': 'min_fireplaces', # Usar como min_fireplaces
            'Fireplaces': 'max_fireplaces', # También como max_fireplaces
            'GarageCars': 'min_garage_cars', # Usar como min_garage_cars
            'GarageCars': 'max_garage_cars', # También como max_garage_cars
            'GarageArea': 'min_garage_area', # Usar como min_garage_area
            'GarageArea': 'max_garage_area', # También como max_garage_area
            'SaleCondition': 'preferred_sale_type',
            # Nuevos mapeos para las columnas agregadas
            'TotalBath': 'min_total_bath',  # Usar como min_total_bath
            'TotalBath': 'max_total_bath',  # También como max_total_bath
            'TotalSF': 'min_total_sf',     # Usar como min_total_sf
            'TotalSF': 'max_total_sf',     # También como max_total_sf
            'RemodAge': 'min_remod_age',   # Usar como min_remod_age
            'RemodAge': 'max_remod_age',   # También como max_remod_age
            'HouseAge': 'min_house_age',   # Usar como min_house_age
            'HouseAge': 'max_house_age',   # También como max_house_age
            'GarageScore': 'min_garage_score', # Usar como min_garage_score
            'GarageScore': 'max_garage_score', # También como max_garage_score
            'TotalPorchSF': 'min_total_porch_sf', # Usar como min_total_porch_sf
            'TotalPorchSF': 'max_total_porch_sf', # También como max_total_porch_sf
            'RoomsPlusBathEq': 'min_rooms_plus_bath_eq', # Usar como min_rooms_plus_bath_eq
            'RoomsPlusBathEq': 'max_rooms_plus_bath_eq'  # También como max_rooms_plus_bath_eq
        }
        
        # Aplicar mapeo del JSON
        for json_field, pref_field in json_mapping.items():
            if json_field in data and data[json_field] is not None:
                if pref_field in ['min_year_built', 'max_year_built'] and json_field == 'YearBuilt':
                    # Para YearBuilt, usar el mismo valor para min y max
                    mapped_data['min_year_built'] = int(data[json_field])
                    mapped_data['max_year_built'] = int(data[json_field])
                elif pref_field in ['min_lot_area', 'max_lot_area'] and json_field == 'LotArea':
                    # Para LotArea, usar el mismo valor para min y max
                    mapped_data['min_lot_area'] = float(data[json_field])
                    mapped_data['max_lot_area'] = float(data[json_field])
                elif pref_field in ['min_1st_flr_sf', 'max_1st_flr_sf'] and json_field == '1stFlrSF':
                    # Para 1stFlrSF, usar el mismo valor para min y max
                    mapped_data['min_1st_flr_sf'] = float(data[json_field])
                    mapped_data['max_1st_flr_sf'] = float(data[json_field])
                elif pref_field in ['min_2nd_flr_sf', 'max_2nd_flr_sf'] and json_field == '2ndFlrSF':
                    # Para 2ndFlrSF, usar el mismo valor para min y max
                    mapped_data['min_2nd_flr_sf'] = float(data[json_field])
                    mapped_data['max_2nd_flr_sf'] = float(data[json_field])
                elif pref_field in ['min_gr_liv_area', 'max_gr_liv_area'] and json_field == 'GrLivArea':
                    # Para GrLivArea, usar el mismo valor para min y max
                    mapped_data['min_gr_liv_area'] = float(data[json_field])
                    mapped_data['max_gr_liv_area'] = float(data[json_field])
                elif pref_field in ['min_fireplaces', 'max_fireplaces'] and json_field == 'Fireplaces':
                    # Para Fireplaces, usar el mismo valor para min y max
                    mapped_data['min_fireplaces'] = int(data[json_field])
                    mapped_data['max_fireplaces'] = int(data[json_field])
                elif pref_field in ['min_garage_cars', 'max_garage_cars'] and json_field == 'GarageCars':
                    # Para GarageCars, usar el mismo valor para min y max
                    mapped_data['min_garage_cars'] = int(data[json_field])
                    mapped_data['max_garage_cars'] = int(data[json_field])
                elif pref_field in ['min_garage_area', 'max_garage_area'] and json_field == 'GarageArea':
                    # Para GarageArea, usar el mismo valor para min y max
                    mapped_data['min_garage_area'] = float(data[json_field])
                    mapped_data['max_garage_area'] = float(data[json_field])
                elif pref_field in ['min_total_bath', 'max_total_bath'] and json_field == 'TotalBath':
                    # Para TotalBath, usar el mismo valor para min y max
                    mapped_data['min_total_bath'] = float(data[json_field])
                    mapped_data['max_total_bath'] = float(data[json_field])
                elif pref_field in ['min_total_sf', 'max_total_sf'] and json_field == 'TotalSF':
                    # Para TotalSF, usar el mismo valor para min y max
                    mapped_data['min_total_sf'] = float(data[json_field])
                    mapped_data['max_total_sf'] = float(data[json_field])
                elif pref_field in ['min_remod_age', 'max_remod_age'] and json_field == 'RemodAge':
                    # Para RemodAge, usar el mismo valor para min y max
                    mapped_data['min_remod_age'] = float(data[json_field])
                    mapped_data['max_remod_age'] = float(data[json_field])
                elif pref_field in ['min_house_age', 'max_house_age'] and json_field == 'HouseAge':
                    # Para HouseAge, usar el mismo valor para min y max
                    mapped_data['min_house_age'] = float(data[json_field])
                    mapped_data['max_house_age'] = float(data[json_field])
                elif pref_field in ['min_garage_score', 'max_garage_score'] and json_field == 'GarageScore':
                    # Para GarageScore, usar el mismo valor para min y max
                    mapped_data['min_garage_score'] = float(data[json_field])
                    mapped_data['max_garage_score'] = float(data[json_field])
                elif pref_field in ['min_total_porch_sf', 'max_total_porch_sf'] and json_field == 'TotalPorchSF':
                    # Para TotalPorchSF, usar el mismo valor para min y max
                    mapped_data['min_total_porch_sf'] = float(data[json_field])
                    mapped_data['max_total_porch_sf'] = float(data[json_field])
                elif pref_field in ['min_rooms_plus_bath_eq', 'max_rooms_plus_bath_eq'] and json_field == 'RoomsPlusBathEq':
                    # Para RoomsPlusBathEq, usar el mismo valor para min y max
                    mapped_data['min_rooms_plus_bath_eq'] = float(data[json_field])
                    mapped_data['max_rooms_plus_bath_eq'] = float(data[json_field])
                else:
                    # Para otros campos, mapear directamente
                    mapped_data[pref_field] = data[json_field]
        
        # Validar que al menos se proporcione algún campo
        if not mapped_data:
            return jsonify({"error": "No se proporcionaron campos válidos para las preferencias"}), 400
        
        # Crear o actualizar preferencias
        prefs = PreferencesService.create_preference(client_id, mapped_data)
        if prefs is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        
        return jsonify({
            "message": "Preferencias específicas creadas/actualizadas correctamente",
            "preferences": prefs,
            "mapped_fields": list(mapped_data.keys())
        }), 201
        
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

# AI MODELS

@main.route("/api/ai/predict/complex", methods=["POST"])
def predict_complex():
    """Predicción de precio usando el modelo complejo (todas las características)"""
    try:
        data = request.get_json(silent=True) or {}
        if not data:
            return jsonify({"error": "Datos de entrada requeridos"}), 400
        
        result = AIService.predict_complex(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/ai/predict/simple", methods=["POST"])
def predict_simple():
    """Predicción de precio usando el modelo sencillo (top 20 características)"""
    try:
        data = request.get_json(silent=True) or {}
        if not data:
            return jsonify({"error": "Datos de entrada requeridos"}), 400
        
        result = AIService.predict_simple(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/ai/predict/both", methods=["POST"])
def predict_both():
    """Predicción usando ambos modelos para comparar resultados"""
    try:
        data = request.get_json(silent=True) or {}
        if not data:
            return jsonify({"error": "Datos de entrada requeridos"}), 400
        
        result = AIService.predict_both(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/ai/models/status", methods=["GET"])
def ai_models_status():
    """Obtener el estado de los modelos de IA"""
    try:
        status = AIService.get_model_status()
        return jsonify(status)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
