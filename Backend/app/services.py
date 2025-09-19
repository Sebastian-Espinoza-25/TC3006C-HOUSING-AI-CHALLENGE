from . import db
from .models import Client, Vendor, ClientPreferences, VendorHouse
from werkzeug.security import generate_password_hash, check_password_hash

# Helpers
def _assign_model_fields(instance, data, *, exclude=()):
    """
    Assign only keys that exist as mapped columns on the instance's model.
    Excludes any keys in 'exclude'.
    """
    cols = {c.name for c in instance.__table__.columns}
    for k, v in (data or {}).items():
        if k in exclude:
            continue
        if k in cols:
            setattr(instance, k, v)

def _truthy_strings():
    # For vendor_houses.central_air (VARCHAR)
    return {"Y", "Yes", "1", "True", "T", "SI", "SÍ", "ON"}

# Client Service
class ClientService:
    @staticmethod
    def get_all_clients():
        clients = Client.query.all()
        return [c.to_dict() for c in clients]

    @staticmethod
    def get_client_by_id(client_id):
        c = Client.query.get(client_id)
        return c.to_dict() if c else None

    @staticmethod
    def create_client(client_data):
        try:
            c = Client(
                username=client_data['username'],
                email=client_data['email'],
                password=generate_password_hash(client_data['password'])  # hash
            )
            db.session.add(c)
            db.session.commit()
            return c.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def update_client(client_id, client_data):
        try:
            c = Client.query.get(client_id)
            if not c:
                return None
            if "password" in client_data:
                client_data["password"] = generate_password_hash(client_data["password"])
            _assign_model_fields(c, client_data, exclude=('client_id',))
            db.session.commit()
            return c.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_client(client_id):
        try:
            c = Client.query.get(client_id)
            if not c:
                return False
            db.session.delete(c)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def authenticate(identifier: str, password: str):
        """
        Autentica un cliente por email o username.
        Devuelve dict si coincide la contraseña, si no None.
        """
        client = Client.query.filter(
            (Client.email == identifier) | (Client.username == identifier)
        ).first()
        if not client:
            return None

        if check_password_hash(client.password, password):
            return client.to_dict()

        # Fallback por si alguna contraseña se guardó en texto plano (temporal)
        if client.password == password:
            return client.to_dict()

        return None

# Vendor Service
class VendorService:
    @staticmethod
    def get_all_vendors():
        vendors = Vendor.query.all()
        return [v.to_dict() for v in vendors]

    @staticmethod
    def get_vendor_by_id(vendor_id):
        v = Vendor.query.get(vendor_id)
        return v.to_dict() if v else None

    @staticmethod
    def create_vendor(vendor_data):
        try:
            v = Vendor(
                username=vendor_data['username'],
                email=vendor_data['email'],
                password=generate_password_hash(vendor_data['password'])  # hash
            )
            db.session.add(v)
            db.session.commit()
            return v.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def update_vendor(vendor_id, vendor_data):
        try:
            v = Vendor.query.get(vendor_id)
            if not v:
                return None
            if "password" in vendor_data:
                vendor_data["password"] = generate_password_hash(vendor_data["password"])
            _assign_model_fields(v, vendor_data, exclude=('vendor_id',))
            db.session.commit()
            return v.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_vendor(vendor_id):
        try:
            v = Vendor.query.get(vendor_id)
            if not v:
                return False
            db.session.delete(v)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def authenticate(identifier: str, password: str):
        """
        Autentica un vendedor por email o username.
        Devuelve dict si coincide la contraseña, si no None.
        """
        vendor = Vendor.query.filter(
            (Vendor.email == identifier) | (Vendor.username == identifier)
        ).first()
        if not vendor:
            return None

        if check_password_hash(vendor.password, password):
            return vendor.to_dict()

        if vendor.password == password:  # fallback temporal
            return vendor.to_dict()

        return None

# House Service 
class HouseService:
    @staticmethod
    def get_houses_by_vendor(vendor_id):
        """
        Retorna todas las casas que pertenecen a un vendor_id.
        """
        vendor = Vendor.query.get(vendor_id)
        if not vendor:
            return None
        houses = VendorHouse.query.filter_by(vendor_id=vendor_id).all()
        return [h.to_dict() for h in houses]
    
    @staticmethod
    def create_house(vendor_id, house_data):
        """
        Create a house for a vendor.
        Requires vendor_id and at least: title, sale_price.
        """
        try:
            h = VendorHouse(vendor_id=vendor_id)
            h.title = house_data['title']
            h.sale_price = float(house_data['sale_price'])
            _assign_model_fields(h, house_data, exclude=('house_id', 'vendor_id', 'title', 'sale_price'))
            db.session.add(h)
            db.session.commit()
            return h.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_house(house_id):
        try:
            h = VendorHouse.query.get(house_id)
            if not h:
                return False
            db.session.delete(h)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

# Preferences Service 
class PreferencesService:
    @staticmethod
    def create_preference(client_id, preferences_data):
        try:
            print(f"DEBUG: Creating preference for client_id: {client_id}")
            print(f"DEBUG: Preferences data: {preferences_data}")
            
            p = ClientPreferences.query.filter_by(client_id=client_id).first()
            if not p:
                print("DEBUG: Creating new preference record")
                p = ClientPreferences(client_id=client_id)
                db.session.add(p)
            else:
                print("DEBUG: Updating existing preference record")
            
            _assign_model_fields(p, preferences_data, exclude=('preference_id', 'client_id'))
            db.session.commit()
            
            result = p.to_dict()
            print(f"DEBUG: Final result: {result}")
            return result
        except Exception as e:
            print(f"DEBUG: Error occurred: {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def delete_preference(client_id):
        try:
            p = ClientPreferences.query.filter_by(client_id=client_id).first()
            if not p:
                return False
            db.session.delete(p)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def find_matching_houses(client_id):
        client = Client.query.get(client_id)
        if not client:
            return {'client': None, 'matches': [], 'preferences_applied': None}

        prefs = ClientPreferences.query.filter_by(client_id=client_id).order_by(ClientPreferences.preference_id.desc()).first()
        if not prefs:
            return {'client': client.to_dict(), 'matches': [], 'preferences_applied': None}

        # Crear lista de condiciones OR
        from sqlalchemy import or_, and_
        conditions = []
        
        # Filtro base: solo casas disponibles
        base_query = VendorHouse.query.filter(VendorHouse.status == 'available')

        # Precio
        if prefs.min_sale_price is not None and prefs.max_sale_price is not None:
            conditions.append(
                and_(VendorHouse.sale_price >= float(prefs.min_sale_price),
                     VendorHouse.sale_price <= float(prefs.max_sale_price))
            )
        elif prefs.min_sale_price is not None:
            conditions.append(VendorHouse.sale_price >= float(prefs.min_sale_price))
        elif prefs.max_sale_price is not None:
            conditions.append(VendorHouse.sale_price <= float(prefs.max_sale_price))

        # Ubicación
        if prefs.preferred_neighborhood:
            conditions.append(VendorHouse.neighborhood == prefs.preferred_neighborhood)
        if prefs.preferred_ms_zoning:
            conditions.append(VendorHouse.ms_zoning == prefs.preferred_ms_zoning)

        # Características exactas
        exact_string_cols = [
            ('preferred_bldg_type', 'bldg_type'),
            ('preferred_house_style', 'house_style'),
            ('preferred_roof_style', 'roof_style'),
            ('preferred_exterior1st', 'exterior1st'),
            ('preferred_exterior2nd', 'exterior2nd'),
            ('preferred_foundation', 'foundation'),
            ('preferred_condition1', 'condition1'),
            ('preferred_functional', 'functional'),
            ('preferred_fireplace_qu', 'fireplace_qu'),
            ('preferred_garage_type', 'garage_type'),
            ('preferred_garage_finish', 'garage_finish'),
            ('preferred_garage_qual', 'garage_qual'),
            ('preferred_garage_cond', 'garage_cond'),
            ('preferred_paved_drive', 'paved_drive'),
            ('preferred_pool_qc', 'pool_qc'),
            ('preferred_fence', 'fence'),
            ('preferred_misc_feature', 'misc_feature'),
            ('preferred_bsmt_qual', 'bsmt_qual'),
            ('preferred_bsmt_cond', 'bsmt_cond'),
            ('preferred_bsmt_exposure', 'bsmt_exposure'),
            ('preferred_bsmt_fin_type1', 'bsmt_fin_type1'),
            ('preferred_bsmt_fin_type2', 'bsmt_fin_type2'),
            ('preferred_heating_qc', 'heating_qc'),
            ('preferred_electrical', 'electrical'),
        ]
        for pref_attr, house_col in exact_string_cols:
            val = getattr(prefs, pref_attr)
            if val:
                conditions.append(getattr(VendorHouse, house_col) == val)

        # Aire acondicionado
        if prefs.central_air_required:
            conditions.append(VendorHouse.central_air.in_(_truthy_strings()))

        # Rangos numéricos
        if prefs.min_bedroom_abv_gr is not None and prefs.max_bedroom_abv_gr is not None:
            conditions.append(
                and_(VendorHouse.bedroom_abv_gr >= float(prefs.min_bedroom_abv_gr),
                     VendorHouse.bedroom_abv_gr <= float(prefs.max_bedroom_abv_gr))
            )
        elif prefs.min_bedroom_abv_gr is not None:
            conditions.append(VendorHouse.bedroom_abv_gr >= float(prefs.min_bedroom_abv_gr))
        elif prefs.max_bedroom_abv_gr is not None:
            conditions.append(VendorHouse.bedroom_abv_gr <= float(prefs.max_bedroom_abv_gr))

        if prefs.min_full_bath is not None and prefs.max_full_bath is not None:
            conditions.append(
                and_(VendorHouse.full_bath >= float(prefs.min_full_bath),
                     VendorHouse.full_bath <= float(prefs.max_full_bath))
            )
        elif prefs.min_full_bath is not None:
            conditions.append(VendorHouse.full_bath >= float(prefs.min_full_bath))
        elif prefs.max_full_bath is not None:
            conditions.append(VendorHouse.full_bath <= float(prefs.max_full_bath))

        if prefs.min_gr_liv_area is not None and prefs.max_gr_liv_area is not None:
            conditions.append(
                and_(VendorHouse.gr_liv_area >= float(prefs.min_gr_liv_area),
                     VendorHouse.gr_liv_area <= float(prefs.max_gr_liv_area))
            )
        elif prefs.min_gr_liv_area is not None:
            conditions.append(VendorHouse.gr_liv_area >= float(prefs.min_gr_liv_area))
        elif prefs.max_gr_liv_area is not None:
            conditions.append(VendorHouse.gr_liv_area <= float(prefs.max_gr_liv_area))

        # Nuevas columnas - Total Bath
        if prefs.min_total_bath is not None and prefs.max_total_bath is not None:
            conditions.append(
                and_(VendorHouse.total_bath >= float(prefs.min_total_bath),
                     VendorHouse.total_bath <= float(prefs.max_total_bath))
            )
        elif prefs.min_total_bath is not None:
            conditions.append(VendorHouse.total_bath >= float(prefs.min_total_bath))
        elif prefs.max_total_bath is not None:
            conditions.append(VendorHouse.total_bath <= float(prefs.max_total_bath))

        # Total SF
        if prefs.min_total_sf is not None and prefs.max_total_sf is not None:
            conditions.append(
                and_(VendorHouse.total_sf >= float(prefs.min_total_sf),
                     VendorHouse.total_sf <= float(prefs.max_total_sf))
            )
        elif prefs.min_total_sf is not None:
            conditions.append(VendorHouse.total_sf >= float(prefs.min_total_sf))
        elif prefs.max_total_sf is not None:
            conditions.append(VendorHouse.total_sf <= float(prefs.max_total_sf))

        # Remod Age
        if prefs.min_remod_age is not None and prefs.max_remod_age is not None:
            conditions.append(
                and_(VendorHouse.remod_age >= float(prefs.min_remod_age),
                     VendorHouse.remod_age <= float(prefs.max_remod_age))
            )
        elif prefs.min_remod_age is not None:
            conditions.append(VendorHouse.remod_age >= float(prefs.min_remod_age))
        elif prefs.max_remod_age is not None:
            conditions.append(VendorHouse.remod_age <= float(prefs.max_remod_age))

        # House Age
        if prefs.min_house_age is not None and prefs.max_house_age is not None:
            conditions.append(
                and_(VendorHouse.house_age >= float(prefs.min_house_age),
                     VendorHouse.house_age <= float(prefs.max_house_age))
            )
        elif prefs.min_house_age is not None:
            conditions.append(VendorHouse.house_age >= float(prefs.min_house_age))
        elif prefs.max_house_age is not None:
            conditions.append(VendorHouse.house_age <= float(prefs.max_house_age))

        # Garage Score
        if prefs.min_garage_score is not None and prefs.max_garage_score is not None:
            conditions.append(
                and_(VendorHouse.garage_score >= float(prefs.min_garage_score),
                     VendorHouse.garage_score <= float(prefs.max_garage_score))
            )
        elif prefs.min_garage_score is not None:
            conditions.append(VendorHouse.garage_score >= float(prefs.min_garage_score))
        elif prefs.max_garage_score is not None:
            conditions.append(VendorHouse.garage_score <= float(prefs.max_garage_score))

        # Total Porch SF
        if prefs.min_total_porch_sf is not None and prefs.max_total_porch_sf is not None:
            conditions.append(
                and_(VendorHouse.total_porch_sf >= float(prefs.min_total_porch_sf),
                     VendorHouse.total_porch_sf <= float(prefs.max_total_porch_sf))
            )
        elif prefs.min_total_porch_sf is not None:
            conditions.append(VendorHouse.total_porch_sf >= float(prefs.min_total_porch_sf))
        elif prefs.max_total_porch_sf is not None:
            conditions.append(VendorHouse.total_porch_sf <= float(prefs.max_total_porch_sf))

        # Rooms Plus Bath Eq
        if prefs.min_rooms_plus_bath_eq is not None and prefs.max_rooms_plus_bath_eq is not None:
            conditions.append(
                and_(VendorHouse.rooms_plus_bath_eq >= float(prefs.min_rooms_plus_bath_eq),
                     VendorHouse.rooms_plus_bath_eq <= float(prefs.max_rooms_plus_bath_eq))
            )
        elif prefs.min_rooms_plus_bath_eq is not None:
            conditions.append(VendorHouse.rooms_plus_bath_eq >= float(prefs.min_rooms_plus_bath_eq))
        elif prefs.max_rooms_plus_bath_eq is not None:
            conditions.append(VendorHouse.rooms_plus_bath_eq <= float(prefs.max_rooms_plus_bath_eq))

        # Aplicar condiciones OR si hay alguna
        if conditions:
            q = base_query.filter(or_(*conditions))
        else:
            q = base_query

        houses = q.all()
        matches = []
        for h in houses:
            v = Vendor.query.get(h.vendor_id)
            vendor_info = v.to_dict() if v else None
            if vendor_info is None:
                continue

            vendor_info_with_contact = {
                **vendor_info,
                'contact_phone': h.contact_phone,
                'contact_email': h.contact_email,
            }

            matches.append({
                'house': h.to_dict(),
                'vendor': vendor_info_with_contact
            })

        return {
            'client': client.to_dict(),
            'matches': matches,
            'preferences_applied': prefs.to_dict()
        }


# AI SERVICE

class AIService:
    """Servicio para manejar predicciones de modelos de IA"""
    
    _full_pipeline = None
    _top20_pipeline = None
    _models_loaded = False
    
    @classmethod
    def load_models(cls):
        """Cargar los modelos de IA desde la carpeta resources"""
        try:
            import joblib
            import os
            import warnings
            
            # Suprimir warnings de compatibilidad
            warnings.filterwarnings("ignore", category=UserWarning)
            
            # Ruta a la carpeta resources
            current_dir = os.path.dirname(os.path.abspath(__file__))
            resources_dir = os.path.join(current_dir, '../resources')
            
            # Cargar modelo complejo
            full_pipeline_path = os.path.join(resources_dir, 'xgb_full_pipeline.pkl')
            if os.path.exists(full_pipeline_path):
                try:
                    cls._full_pipeline = joblib.load(full_pipeline_path)
                    print(f"Modelo complejo cargado desde: {full_pipeline_path}")
                except Exception as e:
                    print(f"Error cargando modelo complejo: {e}")
                    cls._full_pipeline = None
            else:
                print(f"Archivo no encontrado: {full_pipeline_path}")
            
            # Cargar modelo sencillo
            top20_pipeline_path = os.path.join(resources_dir, 'xgb_top20_pipeline.pkl')
            if os.path.exists(top20_pipeline_path):
                try:
                    cls._top20_pipeline = joblib.load(top20_pipeline_path)
                    print(f"Modelo sencillo cargado desde: {top20_pipeline_path}")
                except Exception as e:
                    print(f"Error cargando modelo sencillo: {e}")
                    cls._top20_pipeline = None
            else:
                print(f"Archivo no encontrado: {top20_pipeline_path}")
            
            cls._models_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar modelos de IA: {e}")
            cls._models_loaded = False
            return False
    
    @classmethod
    def get_model_status(cls):
        """Obtener el estado de los modelos"""
        return {
            'models_loaded': cls._models_loaded,
            'complex_model_available': cls._full_pipeline is not None,
            'simple_model_available': cls._top20_pipeline is not None
        }
    
    @classmethod
    def predict_complex(cls, data):
        """Predicción usando el modelo complejo (todas las características)"""
        if not cls._models_loaded:
            cls.load_models()
        
        if cls._full_pipeline is None:
            raise Exception("Modelo complejo no disponible")
        
        try:
            import pandas as pd
            import numpy as np
            
            # Convertir datos a DataFrame
            df = pd.DataFrame([data])
            
            # Realizar predicción
            prediction = cls._full_pipeline.predict(df)[0]
            
            return {
                'model_type': 'complex',
                'predicted_price': float(prediction),
                'status': 'success'
            }
            
        except Exception as e:
            raise Exception(f"Error en predicción compleja: {str(e)}")
    
    @classmethod
    def predict_simple(cls, data):
        """Predicción usando el modelo sencillo (top 20 características)"""
        if not cls._models_loaded:
            cls.load_models()
        
        if cls._top20_pipeline is None:
            raise Exception("Modelo sencillo no disponible")
        
        try:
            import pandas as pd
            import numpy as np
            
            # Convertir datos a DataFrame
            df = pd.DataFrame([data])
            
            # Realizar predicción
            prediction = cls._top20_pipeline.predict(df)[0]
            
            return {
                'model_type': 'simple',
                'predicted_price': float(prediction),
                'status': 'success'
            }
            
        except Exception as e:
            raise Exception(f"Error en predicción sencilla: {str(e)}")
    
    @classmethod
    def predict_both(cls, data):
        """Predicción usando ambos modelos para comparar"""
        if not cls._models_loaded:
            cls.load_models()
        
        results = {}
        
        # Predicción compleja
        if cls._full_pipeline is not None:
            try:
                complex_result = cls.predict_complex(data)
                results['complex_prediction'] = complex_result
            except Exception as e:
                results['complex_error'] = str(e)
        
        # Predicción sencilla
        if cls._top20_pipeline is not None:
            try:
                simple_result = cls.predict_simple(data)
                results['simple_prediction'] = simple_result
            except Exception as e:
                results['simple_error'] = str(e)
        
        if not results:
            raise Exception("Ningún modelo de IA disponible")
        
        return results
    
    @classmethod
    def predict_house_price(cls, house_data):
        """Predicción de precio para una casa existente en la base de datos"""
        try:
            # Filtrar campos que no son relevantes para el modelo
            excluded_fields = [
                'house_id', 'vendor_id', 'title', 'description', 
                'images', 'features', 'status', 'is_featured', 
                'contact_phone', 'contact_email'
            ]
            
            # Crear datos limpios para predicción
            clean_data = {
                k: v for k, v in house_data.items() 
                if k not in excluded_fields and v is not None
            }
            
            return cls.predict_both(clean_data)
            
        except Exception as e:
            raise Exception(f"Error al predecir precio de casa: {str(e)}")

        