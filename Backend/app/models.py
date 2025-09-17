from datetime import datetime
from . import db

class Client(db.Model):
    """Modelo para clientes del sistema"""
    __tablename__ = 'clients'
    
    client_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Relación con preferencias
    preferences = db.relationship('ClientPreferences', backref='client', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'client_id': self.client_id,
            'email': self.email,
            'username': self.username
        }

class Vendor(db.Model):
    """Modelo para vendedores del sistema"""
    __tablename__ = 'vendors'
    
    vendor_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Relación con casas
    houses = db.relationship('VendorHouse', backref='vendor', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'vendor_id': self.vendor_id,
            'email': self.email,
            'username': self.username
        }

class ClientPreferences(db.Model):
    """Modelo para preferencias de clientes"""
    __tablename__ = 'client_preferences'
    
    preference_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('clients.client_id', ondelete='CASCADE'), nullable=False)
    
    # Preferencias de ubicación
    preferred_location = db.Column(db.String(200))
    max_distance_from_center = db.Column(db.Float)  # km
    
    # Preferencias de precio
    min_price = db.Column(db.Numeric(15, 2))
    max_price = db.Column(db.Numeric(15, 2))
    
    # Preferencias de tamaño
    min_bedrooms = db.Column(db.Integer)
    max_bedrooms = db.Column(db.Integer)
    min_bathrooms = db.Column(db.Integer)
    max_bathrooms = db.Column(db.Integer)
    min_area = db.Column(db.Float)  # m²
    max_area = db.Column(db.Float)  # m²
    
    # Preferencias de tipo de propiedad
    property_type = db.Column(db.String(50))  # casa, apartamento, loft, etc.
    
    # Preferencias de características
    features = db.Column(db.JSON)  # Array de características deseadas
    
    # Preferencias de transporte
    near_metro = db.Column(db.Boolean, default=False)
    near_bus_stop = db.Column(db.Boolean, default=False)
    parking_required = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'preference_id': self.preference_id,
            'client_id': self.client_id,
            'preferred_location': self.preferred_location,
            'max_distance_from_center': self.max_distance_from_center,
            'min_price': float(self.min_price) if self.min_price else None,
            'max_price': float(self.max_price) if self.max_price else None,
            'min_bedrooms': self.min_bedrooms,
            'max_bedrooms': self.max_bedrooms,
            'min_bathrooms': self.min_bathrooms,
            'max_bathrooms': self.max_bathrooms,
            'min_area': self.min_area,
            'max_area': self.max_area,
            'property_type': self.property_type,
            'features': self.features or [],
            'near_metro': self.near_metro,
            'near_bus_stop': self.near_bus_stop,
            'parking_required': self.parking_required
        }

class VendorHouse(db.Model):
    """Modelo para casas de vendedores"""
    __tablename__ = 'vendor_houses'
    
    house_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.BigInteger, db.ForeignKey('vendors.vendor_id', ondelete='CASCADE'), nullable=False)
    
    # Información básica
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Características físicas
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)  # m²
    property_type = db.Column(db.String(50), nullable=False)
    
    # Ubicación
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Características adicionales
    features = db.Column(db.JSON)  # Array de características
    images = db.Column(db.JSON)  # Array de URLs de imágenes
    
    # Estado y disponibilidad
    status = db.Column(db.String(20), default='available')  # available, sold, rented
    is_featured = db.Column(db.Boolean, default=False)
    
    # Información de contacto
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'house_id': self.house_id,
            'vendor_id': self.vendor_id,
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area': self.area,
            'property_type': self.property_type,
            'location': self.location,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'features': self.features or [],
            'images': self.images or [],
            'status': self.status,
            'is_featured': self.is_featured,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email
        }
