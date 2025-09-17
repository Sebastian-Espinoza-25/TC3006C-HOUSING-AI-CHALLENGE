# Housing AI - Backend API

Backend API para el sistema de Housing AI Challenge. Proporciona endpoints para gestión de propiedades, usuarios y búsquedas inteligentes.

## 🚀 Características

- **API REST** con Flask y SQLAlchemy
- **Base de datos MySQL** en AWS RDS
- **Modelos de datos** para propiedades, usuarios y historial de búsquedas
- **Filtros avanzados** para búsqueda de propiedades
- **Paginación** en todas las consultas
- **Validación de datos** y manejo de errores
- **Datos de ejemplo** para testing

## 📋 Requisitos

- Python 3.8+
- MySQL 8.0+
- Acceso a AWS RDS

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto:
   ```env
   # Database Configuration
   DB_HOST=database-1.c7qm8a6ski6h.us-east-1.rds.amazonaws.com
   DB_PORT=3306
   DB_NAME=housing_ai
   DB_USER=tu_usuario_aqui
   DB_PASSWORD=tu_password_aqui
   
   # Flask Configuration
   FLASK_ENV=development
   SECRET_KEY=tu_secret_key_aqui
   ```

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

6. **Poblar la base de datos (opcional)**
   ```bash
   python seed_data.py
   ```

## 📚 API Endpoints

### 👥 Clientes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/clients` | Obtener todos los clientes |
| GET | `/api/clients/{id}` | Obtener cliente específico |
| POST | `/api/clients` | Crear nuevo cliente |
| PUT | `/api/clients/{id}` | Actualizar cliente |

### 🏢 Vendedores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/vendors` | Obtener todos los vendedores |
| GET | `/api/vendors/{id}` | Obtener vendedor específico |
| POST | `/api/vendors` | Crear nuevo vendedor |
| PUT | `/api/vendors/{id}` | Actualizar vendedor |

### 🏠 Casas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/houses` | Obtener todas las casas (con filtros y paginación) |
| GET | `/api/houses/{id}` | Obtener casa específica |
| GET | `/api/vendors/{id}/houses` | Obtener casas de un vendedor |
| POST | `/api/vendors/{id}/houses` | Crear nueva casa para un vendedor |
| PUT | `/api/houses/{id}` | Actualizar casa |
| DELETE | `/api/houses/{id}` | Eliminar casa |

**Filtros disponibles:**
- `property_type`: casa, departamento, loft, penthouse
- `min_price`, `max_price`: rango de precios
- `bedrooms`, `bathrooms`: número de habitaciones/baños
- `location`: ubicación
- `min_area`: área mínima
- `status`: available, sold, rented
- `is_featured`: true/false

### ⚙️ Preferencias

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/clients/{id}/preferences` | Obtener preferencias de un cliente |
| POST | `/api/clients/{id}/preferences` | Crear/actualizar preferencias |
| GET | `/api/clients/{id}/recommendations` | Obtener recomendaciones basadas en preferencias |

### 🔍 Búsquedas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/search?q={query}` | Buscar casas por texto |

### 📊 Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/stats` | Obtener estadísticas del sistema |

## 💡 Ejemplos de Uso

### Crear un cliente
```bash
POST /api/clients
Content-Type: application/json

{
  "username": "juan_perez",
  "email": "juan@example.com",
  "password": "password123"
}
```

### Crear un vendedor
```bash
POST /api/vendors
Content-Type: application/json

{
  "username": "inmobiliaria_elite",
  "email": "contacto@inmobiliariaelite.com",
  "password": "vendor123"
}
```

### Obtener casas con filtros
```bash
GET /api/houses?property_type=casa&min_price=5000000&bedrooms=3&page=1&per_page=10
```

### Crear una nueva casa
```bash
POST /api/vendors/1/houses
Content-Type: application/json

{
  "title": "Casa moderna en Polanco",
  "description": "Hermosa casa de 3 recámaras...",
  "price": 8500000.00,
  "bedrooms": 3,
  "bathrooms": 3,
  "area": 180.5,
  "property_type": "casa",
  "location": "Polanco, CDMX",
  "address": "Av. Masaryk 123, Polanco",
  "latitude": 19.4326,
  "longitude": -99.1944,
  "images": ["url1.jpg", "url2.jpg"],
  "features": ["jardín", "cochera", "seguridad"],
  "contact_phone": "+52-55-1234-5678",
  "contact_email": "ventas@inmobiliariaelite.com"
}
```

### Configurar preferencias de cliente
```bash
POST /api/clients/1/preferences
Content-Type: application/json

{
  "preferred_location": "Polanco",
  "min_price": 5000000.00,
  "max_price": 10000000.00,
  "min_bedrooms": 2,
  "max_bedrooms": 4,
  "property_type": "casa",
  "features": ["jardín", "cochera", "seguridad"],
  "near_metro": true,
  "parking_required": true
}
```

### Obtener recomendaciones para un cliente
```bash
GET /api/clients/1/recommendations?page=1&per_page=10
```

### Buscar casas
```bash
GET /api/search?q=casa polanco&property_type=casa&min_price=8000000
```

## 🗄️ Estructura de la Base de Datos

### Tabla: clients
- `client_id`: ID único (BIGSERIAL)
- `email`: Correo electrónico único
- `username`: Nombre de usuario único
- `password`: Contraseña (en producción, hashear)
- `created_at`, `updated_at`: Timestamps

### Tabla: vendors
- `vendor_id`: ID único (BIGSERIAL)
- `email`: Correo electrónico único
- `username`: Nombre de usuario único
- `password`: Contraseña (en producción, hashear)
- `created_at`, `updated_at`: Timestamps

### Tabla: client_preferences
- `preference_id`: ID único (BIGSERIAL)
- `client_id`: ID del cliente (FK)
- `preferred_location`: Ubicación preferida
- `max_distance_from_center`: Distancia máxima del centro (km)
- `min_price`, `max_price`: Rango de precios
- `min_bedrooms`, `max_bedrooms`: Rango de habitaciones
- `min_bathrooms`, `max_bathrooms`: Rango de baños
- `min_area`, `max_area`: Rango de área (m²)
- `property_type`: Tipo de propiedad preferido
- `features`: Características deseadas (JSON)
- `near_metro`, `near_bus_stop`, `parking_required`: Preferencias de transporte
- `created_at`, `updated_at`: Timestamps

### Tabla: vendor_houses
- `house_id`: ID único (BIGSERIAL)
- `vendor_id`: ID del vendedor (FK)
- `title`: Título de la casa
- `description`: Descripción detallada
- `price`: Precio (Decimal)
- `bedrooms`: Número de habitaciones
- `bathrooms`: Número de baños
- `area`: Área en metros cuadrados
- `property_type`: Tipo de propiedad
- `location`: Ubicación
- `address`: Dirección completa
- `latitude`, `longitude`: Coordenadas GPS
- `images`: Array de URLs de imágenes (JSON)
- `features`: Características especiales (JSON)
- `status`: Estado (available, sold, rented)
- `is_featured`: Casa destacada (boolean)
- `contact_phone`, `contact_email`: Información de contacto
- `created_at`, `updated_at`: Timestamps

## 🔧 Configuración de AWS RDS

1. **Crear instancia RDS MySQL**
2. **Configurar Security Groups** para permitir conexiones desde tu IP
3. **Obtener endpoint** y credenciales
4. **Actualizar variables de entorno** en `.env`

## 🚀 Despliegue

Para producción, considera:
- Usar un servidor WSGI como Gunicorn
- Configurar HTTPS
- Usar variables de entorno seguras
- Implementar autenticación JWT
- Configurar CORS para el frontend

## 📝 Notas

- La contraseña debe ser hasheada antes de guardar en la BD
- En producción, usar SSL para la conexión a la BD
- Implementar rate limiting para las APIs
- Agregar logs y monitoreo

---

## Branching Strategy

To keep the workflow clean and organized, we follow a **feature-based branching strategy**:

### Main branch
- **`main`** → Stable production branch.  

### Working branches
- **`feature/*`** → Development of new backend features or services.  
  Example: `feature/authentication-api`
- **`fix/*`** → Bug fixes in backend logic.  
  Example: `fix/jwt-expiration-bug`
- **`chore/*`** → Maintenance tasks (configs, dependencies, etc).  
  Example: `chore/update-dockerfile`
- **`docs/*`** → Documentation changes.  
  Example: `docs/api-endpoints`
- **`hotfix/*`** → Urgent fixes applied directly to `main`.  
  Example: `hotfix/payment-service-down`

---

## Workflow

1. Create a branch from `main`  
2. Push the branch to remote  
3. Merge manually into `main` once the feature or fix is complete  
4. Delete the local branch if no longer needed

---

## Commit Conventions

Examples of valid commit messages:
- `feat: add authentication middleware`
- `feat: implement user registration endpoint`
- `fix: correct database connection pool`
- `chore: update environment variables`
- `docs: add API usage guide`

---

## Quick Example

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b feature/authentication-api

# Work and commit
git add .
git commit -m "feat: add authentication middleware"

# Push branch
git push -u origin feature/authentication-api

# Merge back to main
git checkout main
git merge feature/authentication-api
git push origin main