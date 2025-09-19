from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Inicializar extensiones
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurar la aplicación
    app.config.from_object(Config)
    
    # Configurar CORS para permitir requests del frontend
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    
    # Registrar rutas
    from .routes import main
    app.register_blueprint(main)
    
    # Crear tablas de la base de datos
    with app.app_context():
        db.create_all()
        
        # Cargar modelos de IA al iniciar la aplicación
        from .services import AIService
        print("🔄 Cargando modelos de IA...")
        AIService.load_models()
        print("✅ Modelos de IA cargados correctamente")

    return app
