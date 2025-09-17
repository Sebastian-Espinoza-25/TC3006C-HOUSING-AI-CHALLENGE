from . import db
from .models import Client, Vendor, ClientPreferences, VendorHouse
from sqlalchemy import or_, and_
from decimal import Decimal
import json

class ClientService:
    """Servicio para manejar operaciones de clientes"""
    
    @staticmethod
    def get_all_clients():
        """Obtener todos los clientes"""
        clients = Client.query.all()
        return [client.to_dict() for client in clients]
    
    @staticmethod
    def get_client_by_id(client_id):
        """Obtener un cliente por ID"""
        client = Client.query.get(client_id)
        return client.to_dict() if client else None
    
    @staticmethod
    def create_client(client_data):
        """Crear un nuevo cliente"""
        try:
            client = Client(
                username=client_data['username'],
                email=client_data['email'],
                password=client_data['password']  # En producción, hashear la contraseña
            )
            
            db.session.add(client)
            db.session.commit()
            return client.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_client(client_id, client_data):
        """Actualizar un cliente existente"""
        try:
            client = Client.query.get(client_id)
            if not client:
                return None
            
            for key, value in client_data.items():
                if hasattr(client, key) and key != 'client_id':
                    setattr(client, key, value)
            
            db.session.commit()
            return client.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

class VendorService:
    """Servicio para manejar operaciones de vendedores"""
    
    @staticmethod
    def get_all_vendors():
        """Obtener todos los vendedores"""
        vendors = Vendor.query.all()
        return [vendor.to_dict() for vendor in vendors]
    
    @staticmethod
    def get_vendor_by_id(vendor_id):
        """Obtener un vendedor por ID"""
        vendor = Vendor.query.get(vendor_id)
        return vendor.to_dict() if vendor else None
    
    @staticmethod
    def create_vendor(vendor_data):
        """Crear un nuevo vendedor"""
        try:
            vendor = Vendor(
                username=vendor_data['username'],
                email=vendor_data['email'],
                password=vendor_data['password']  # En producción, hashear la contraseña
            )
            
            db.session.add(vendor)
            db.session.commit()
            return vendor.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_vendor(vendor_id, vendor_data):
        """Actualizar un vendedor existente"""
        try:
            vendor = Vendor.query.get(vendor_id)
            if not vendor:
                return None
            
            for key, value in vendor_data.items():
                if hasattr(vendor, key) and key != 'vendor_id':
                    setattr(vendor, key, value)
            
            db.session.commit()
            return vendor.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

class HouseService:
    """Servicio para manejar operaciones de casas"""
    
    @staticmethod
    def get_all_houses(page=1, per_page=10, filters=None):
        """Obtener todas las casas con paginación y filtros"""
        query = VendorHouse.query
        
        if filters:
            # Filtro por tipo de propiedad
            if filters.get('property_type'):
                query = query.filter(VendorHouse.property_type == filters['property_type'])
            
            # Filtro por rango de precio
            if filters.get('min_price'):
                query = query.filter(VendorHouse.price >= Decimal(filters['min_price']))
            if filters.get('max_price'):
                query = query.filter(VendorHouse.price <= Decimal(filters['max_price']))
            
            # Filtro por número de habitaciones
            if filters.get('bedrooms'):
                query = query.filter(VendorHouse.bedrooms >= filters['bedrooms'])
            
            # Filtro por número de baños
            if filters.get('bathrooms'):
                query = query.filter(VendorHouse.bathrooms >= filters['bathrooms'])
            
            # Filtro por ubicación
            if filters.get('location'):
                query = query.filter(VendorHouse.location.ilike(f"%{filters['location']}%"))
            
            # Filtro por área mínima
            if filters.get('min_area'):
                query = query.filter(VendorHouse.area >= filters['min_area'])
            
            # Filtro por estado
            if filters.get('status'):
                query = query.filter(VendorHouse.status == filters['status'])
            
            # Filtro por destacadas
            if filters.get('is_featured'):
                query = query.filter(VendorHouse.is_featured == True)
        
        # Aplicar paginación
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'houses': [house.to_dict() for house in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_house_by_id(house_id):
        """Obtener una casa por ID"""
        house = VendorHouse.query.get(house_id)
        return house.to_dict() if house else None
    
    @staticmethod
    def get_houses_by_vendor(vendor_id, page=1, per_page=10):
        """Obtener casas de un vendedor específico"""
        query = VendorHouse.query.filter_by(vendor_id=vendor_id)
        
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'houses': [house.to_dict() for house in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def create_house(vendor_id, house_data):
        """Crear una nueva casa"""
        try:
            house = VendorHouse(
                vendor_id=vendor_id,
                title=house_data['title'],
                description=house_data.get('description', ''),
                price=Decimal(house_data['price']),
                bedrooms=house_data['bedrooms'],
                bathrooms=house_data['bathrooms'],
                area=house_data['area'],
                property_type=house_data['property_type'],
                location=house_data['location'],
                address=house_data.get('address', ''),
                latitude=house_data.get('latitude'),
                longitude=house_data.get('longitude'),
                images=house_data.get('images', []),
                features=house_data.get('features', []),
                status=house_data.get('status', 'available'),
                is_featured=house_data.get('is_featured', False),
                contact_phone=house_data.get('contact_phone'),
                contact_email=house_data.get('contact_email')
            )
            
            db.session.add(house)
            db.session.commit()
            return house.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_house(house_id, house_data):
        """Actualizar una casa existente"""
        try:
            house = VendorHouse.query.get(house_id)
            if not house:
                return None
            
            for key, value in house_data.items():
                if hasattr(house, key) and key not in ['house_id', 'vendor_id']:
                    if key == 'price':
                        setattr(house, key, Decimal(value))
                    else:
                        setattr(house, key, value)
            
            db.session.commit()
            return house.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_house(house_id):
        """Eliminar una casa"""
        try:
            house = VendorHouse.query.get(house_id)
            if not house:
                return False
            
            db.session.delete(house)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def search_houses(search_query, filters=None):
        """Buscar casas por texto"""
        query = VendorHouse.query.filter(
            or_(
                VendorHouse.title.ilike(f"%{search_query}%"),
                VendorHouse.description.ilike(f"%{search_query}%"),
                VendorHouse.location.ilike(f"%{search_query}%")
            )
        )
        
        if filters:
            if filters.get('property_type'):
                query = query.filter(VendorHouse.property_type == filters['property_type'])
            if filters.get('min_price'):
                query = query.filter(VendorHouse.price >= Decimal(filters['min_price']))
            if filters.get('max_price'):
                query = query.filter(VendorHouse.price <= Decimal(filters['max_price']))
        
        houses = query.all()
        return [house.to_dict() for house in houses]

class PreferencesService:
    """Servicio para manejar preferencias de clientes"""
    
    @staticmethod
    def get_client_preferences(client_id):
        """Obtener preferencias de un cliente"""
        preferences = ClientPreferences.query.filter_by(client_id=client_id).first()
        return preferences.to_dict() if preferences else None
    
    @staticmethod
    def create_or_update_preferences(client_id, preferences_data):
        """Crear o actualizar preferencias de un cliente"""
        try:
            preferences = ClientPreferences.query.filter_by(client_id=client_id).first()
            
            if not preferences:
                preferences = ClientPreferences(client_id=client_id)
                db.session.add(preferences)
            
            # Actualizar campos
            for key, value in preferences_data.items():
                if hasattr(preferences, key) and key != 'preference_id':
                    if key in ['min_price', 'max_price'] and value is not None:
                        setattr(preferences, key, Decimal(value))
                    else:
                        setattr(preferences, key, value)
            
            db.session.commit()
            return preferences.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_matching_houses(client_id, page=1, per_page=10):
        """Encontrar casas que coincidan con las preferencias del cliente"""
        preferences = ClientPreferences.query.filter_by(client_id=client_id).first()
        if not preferences:
            return {'houses': [], 'total': 0, 'pages': 0, 'current_page': page, 'per_page': per_page}
        
        query = VendorHouse.query.filter(VendorHouse.status == 'available')
        
        # Aplicar filtros basados en preferencias
        if preferences.min_price:
            query = query.filter(VendorHouse.price >= preferences.min_price)
        if preferences.max_price:
            query = query.filter(VendorHouse.price <= preferences.max_price)
        if preferences.min_bedrooms:
            query = query.filter(VendorHouse.bedrooms >= preferences.min_bedrooms)
        if preferences.max_bedrooms:
            query = query.filter(VendorHouse.bedrooms <= preferences.max_bedrooms)
        if preferences.min_bathrooms:
            query = query.filter(VendorHouse.bathrooms >= preferences.min_bathrooms)
        if preferences.max_bathrooms:
            query = query.filter(VendorHouse.bathrooms <= preferences.max_bathrooms)
        if preferences.min_area:
            query = query.filter(VendorHouse.area >= preferences.min_area)
        if preferences.max_area:
            query = query.filter(VendorHouse.area <= preferences.max_area)
        if preferences.property_type:
            query = query.filter(VendorHouse.property_type == preferences.property_type)
        if preferences.preferred_location:
            query = query.filter(VendorHouse.location.ilike(f"%{preferences.preferred_location}%"))
        
        # Aplicar paginación
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'houses': [house.to_dict() for house in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'preferences_applied': preferences.to_dict()
        }
