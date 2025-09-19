# app/__init__.py (fragmento)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=["http://localhost:3000","http://127.0.0.1:3000"],
         allow_headers=["Content-Type","Authorization"])

    db.init_app(app)
    jwt.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    # 👇 ESTO ES CLAVE para que /api/auth/login exista
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        db.create_all()
        
        # Cargar modelos de IA al iniciar la aplicación
        from .services import AIService
        print("🔄 Cargando modelos de IA...")
        AIService.load_models()
        print("✅ Modelos de IA cargados correctamente")

    # útil para depurar: imprime todas las rutas
    print(app.url_map)
    return app
