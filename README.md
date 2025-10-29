# Zucane Backend - Stellar Network Integration

Este proyecto maneja la integración con la red Stellar para el proyecto Zucane, incluyendo la generación de claves, establecimiento de trustlines y emisión de tokens.

## 🚀 Características

- **Arquitectura por Dominio (DDD)** - Organización por entidades de negocio
- **SQLAlchemy 2.0 + MySQL** - ORM moderno con base de datos robusta
- **FastAPI** - Framework web moderno y rápido
- **Integración Stellar** - Blockchain para transacciones de tokens
- **Separación de responsabilidades** - Entity, DTO, Repository, Service, Controller
- **Configuración segura** - Variables de entorno y .gitignore

## 📁 Estructura del Proyecto - Arquitectura por Dominio

```
Zucane-BackEnd/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuración Stellar (legacy)
│   ├── 0_generate_keys.py     # Generador de claves Stellar
│   ├── stellar_setup.py       # Setup principal de Stellar
│   ├── empresas/              # Dominio: Empresas
│   │   ├── __init__.py
│   │   ├── dto/
│   │   │   ├── __init__.py
│   │   │   └── empresa_dto.py # Data Transfer Objects
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── empresa_entity.py # Entidad Empresa
│   │   ├── empresa_repository.py # Acceso a datos
│   │   ├── empresa_service.py    # Lógica de negocio
│   │   └── empresa_controller.py # Endpoints REST
│   ├── tokens/                # Dominio: Tokens CO2
│   │   ├── __init__.py
│   │   ├── dto/
│   │   │   ├── __init__.py
│   │   │   └── token_dto.py
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── token_entity.py
│   │   ├── token_repository.py
│   │   ├── token_service.py
│   │   └── token_controller.py
│   ├── transacciones/         # Dominio: Transacciones
│   │   ├── __init__.py
│   │   ├── dto/
│   │   │   ├── __init__.py
│   │   │   └── transaccion_dto.py
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── transaccion_entity.py
│   │   ├── transaccion_repository.py
│   │   ├── transaccion_service.py
│   │   └── transaccion_controller.py
│   ├── pagos/                 # Dominio: Pagos
│   │   ├── __init__.py
│   │   ├── dto/
│   │   │   ├── __init__.py
│   │   │   └── pago_dto.py
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── pago_entity.py
│   │   ├── pago_repository.py
│   │   ├── pago_service.py
│   │   └── pago_controller.py
│   ├── auditoria/             # Dominio: Auditoría
│   │   ├── __init__.py
│   │   ├── dto/
│   │   │   ├── __init__.py
│   │   │   └── auditoria_dto.py
│   │   ├── entity/
│   │   │   ├── __init__.py
│   │   │   └── auditoria_entity.py
│   │   ├── auditoria_repository.py
│   │   ├── auditoria_service.py
│   │   └── auditoria_controller.py
│   └── shared/                # Configuración compartida
│       ├── __init__.py
│       ├── database.py        # SQLAlchemy 2.0 + MySQL
│       └── config.py          # Configuración global
├── .env                       # Variables de entorno (NO committear)
├── .gitignore                 # Archivos a ignorar en Git
├── requirements.txt           # Dependencias de Python
├── main.py                    # Punto de entrada Stellar (legacy)
├── app.py                     # Aplicación FastAPI con arquitectura por dominio
└── README.md                  # Este archivo
```

## 🛠️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd Zucane-BackEnd
   ```

2. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   - Crea un archivo `.env` con las siguientes variables:
   ```env
   # Stellar Network Credentials
   GOVERNMENT_PUBLIC_KEY=tu_clave_publica_government
   GOVERNMENT_SECRET_KEY=tu_clave_secreta_government
   TREASURY_PUBLIC_KEY=tu_clave_publica_treasury
   TREASURY_SECRET_KEY=tu_clave_secreta_treasury
   ASSET_NAME=XOCHI
   HORIZON_URL=https://horizon-testnet.stellar.org
   
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=user
   DB_PASSWORD=pass
   DB_NAME=zucane_db
   ```

5. **Configurar base de datos MySQL:**
   - Instalar MySQL 8.0
   - Crear la base de datos `zucane_db`
   - Configurar usuario y contraseña según el `.env`

## 🎯 Uso

### 1. Generar Claves (Solo la primera vez)

```bash
python src/0_generate_keys.py
```

Este script generará las claves de Government y Treasury, y las activará en la red de prueba de Stellar. **IMPORTANTE**: Guarda estas claves en tu archivo `.env`.

### 2. Ejecutar Setup Principal

```bash
# Stellar Network (legacy)
python main.py

# FastAPI con arquitectura por dominio
python app.py
```

### 3. Acceder a la Documentación Swagger

Una vez ejecutando `python app.py`, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs` 📚
- **ReDoc**: `http://localhost:8000/redoc` 📖
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` 🔧

### 4. Endpoints Principales

- **Health Check**: `GET /health`
- **Empresas**: `GET /api/v1/empresas/`
- **Tokens**: `GET /api/v1/tokens/`
- **Transacciones**: `GET /api/v1/transacciones/`
- **Pagos**: `GET /api/v1/pagos/`
- **Auditoría**: `GET /api/v1/auditoria/`

## 📚 Documentación Swagger

FastAPI incluye automáticamente documentación interactiva con Swagger UI:

### 🎯 Características de Swagger

- **Documentación Automática**: Generada automáticamente desde el código
- **Interfaz Interactiva**: Prueba los endpoints directamente desde el navegador
- **Validación en Tiempo Real**: Valida los datos antes de enviar
- **Esquemas de Datos**: Ve la estructura de los DTOs y respuestas
- **Códigos de Error**: Documentación completa de errores posibles

### 🔧 URLs de Documentación

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000/docs` | Swagger UI (Interfaz principal) |
| `http://localhost:8000/redoc` | ReDoc (Documentación alternativa) |
| `http://localhost:8000/openapi.json` | Esquema OpenAPI en JSON |

### 📋 Cómo usar Swagger

1. **Ejecuta la aplicación**: `python app.py`
2. **Abre el navegador**: Ve a `http://localhost:8000/docs`
3. **Explora los endpoints**: Cada dominio tiene su sección
4. **Prueba las APIs**: Haz clic en "Try it out" en cualquier endpoint
5. **Envía datos**: Completa los campos y ejecuta la petición

### 🏷️ Tags Organizados

- **empresas**: Gestión de empresas compradoras
- **tokens**: Tokens de CO2 emitidos
- **transacciones**: Compras de tokens
- **pagos**: Pagos a productores
- **auditoria**: Registros de auditoría
- **health**: Estado del sistema

## 🔒 Seguridad

- **NUNCA** commitees el archivo `.env` al repositorio
- Las claves secretas son sensibles, mantenlas seguras
- Usa la red de prueba para desarrollo
- Cambia a mainnet solo cuando estés listo para producción

## 📚 Dependencias

- `stellar-sdk`: SDK oficial de Stellar
- `requests`: Para peticiones HTTP
- `python-dotenv`: Para cargar variables de entorno

## 📝 Notas

- Este proyecto usa la red de prueba de Stellar por defecto
- Las claves se generan automáticamente la primera vez
- El archivo `.env` está incluido en `.gitignore` por seguridad
- La estructura `src/` mantiene el código organizado y profesional

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'add: some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

