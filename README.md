# Zucane Backend - Sistema de Tokens CO2 con Stellar

Sistema completo de gestión de tokens de CO2 con integración real a la red Stellar, arquitectura por dominio y documentación completa.

## 🚀 Características Principales

- **Arquitectura por Dominio (DDD)** - Organización por entidades de negocio
- **Integración Real con Stellar** - Transacciones reales en blockchain
- **SQLAlchemy 2.0 + MySQL** - ORM moderno con base de datos robusta
- **FastAPI** - Framework web moderno y rápido
- **Documentación Completa** - Swagger con documentación detallada
- **Sistema de Auditoría** - Trazabilidad completa de transacciones
- **Autenticación Simple** - Sistema de login básico
- **Generación Automática de Claves Stellar** - Claves determinísticas basadas en datos de la empresa

## 📁 Estructura del Proyecto

```
Zucane-BackEnd/
├── src/
│   ├── auth/                      # Dominio: Autenticación
│   │   ├── entity/
│   │   │   └── user_entity.py     # Entidad Usuario
│   │   ├── dto/
│   │   │   └── auth_dto.py        # DTOs de autenticación
│   │   └── auth_controller.py     # Endpoints de login
│   ├── empresas/                  # Dominio: Empresas
│   │   ├── dto/
│   │   │   └── empresa_dto.py     # DTOs con validación Stellar
│   │   ├── entity/
│   │   │   └── empresa_entity.py  # Entidad Empresa
│   │   ├── empresa_repository.py  # Acceso a datos
│   │   ├── empresa_service.py     # Lógica de negocio
│   │   └── empresa_controller.py  # Endpoints REST
│   ├── tokens/                    # Dominio: Tokens CO2
│   │   ├── dto/
│   │   │   └── token_dto.py       # DTOs con validación Stellar
│   │   ├── entity/
│   │   │   └── token_entity.py    # Entidad Token
│   │   ├── token_repository.py    # Acceso a datos
│   │   ├── token_service.py       # Lógica de negocio
│   │   └── token_controller.py    # Endpoints REST
│   ├── transacciones/             # Dominio: Transacciones
│   │   ├── dto/
│   │   │   └── transaccion_dto.py # DTOs de transacciones
│   │   ├── entity/
│   │   │   └── transaccion_entity.py # Entidad Transacción
│   │   ├── transaccion_repository.py # Acceso a datos
│   │   ├── transaccion_service.py    # Lógica de negocio
│   │   └── transaccion_controller.py # Endpoints REST + Stellar
│   ├── pagos/                     # Dominio: Pagos
│   │   ├── dto/
│   │   │   └── pago_dto.py        # DTOs de pagos
│   │   ├── entity/
│   │   │   └── pago_entity.py     # Entidad Pago
│   │   ├── pago_repository.py     # Acceso a datos
│   │   ├── pago_service.py        # Lógica de negocio
│   │   └── pago_controller.py     # Endpoints REST
│   ├── auditoria/                 # Dominio: Auditoría
│   │   ├── dto/
│   │   │   └── auditoria_dto.py   # DTOs de auditoría
│   │   ├── entity/
│   │   │   └── auditoria_entity.py # Entidad Auditoría
│   │   ├── auditoria_repository.py # Acceso a datos
│   │   ├── auditoria_service.py     # Lógica de negocio
│   │   └── auditoria_controller.py  # Endpoints REST
│   ├── stellar/                   # Integración Stellar
│   │   ├── stellar_service.py     # Servicio Stellar real
│   │   └── key_generator.py       # Generador de claves determinísticas
│   ├── payments/                  # Pagos Stellar
│   │   ├── dto/
│   │   │   └── payment_dto.py     # DTOs de pagos Stellar
│   │   ├── payment_service.py     # Servicio de pagos
│   │   └── payment_controller.py  # Endpoints de pagos
│   └── shared/                    # Configuración compartida
│       ├── database.py            # SQLAlchemy 2.0 + MySQL
│       ├── config.py              # Configuración global
│       └── auth.py                # Utilidades de autenticación
├── .env                           # Variables de entorno
├── requirements.txt               # Dependencias de Python
├── app.py                        # Aplicación FastAPI principal
├── setup_database.py             # Script de configuración de BD
└── README.md                     # Este archivo
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Zucane-BackEnd
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env`:
```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=user
DB_PASSWORD=pass
DB_NAME=zucane_db
```

### 5. Configurar base de datos MySQL

#### 5.0 Resumen rápido (3 pasos)
```bash
# 1. Crear BD y usuario
CREATE DATABASE zucane_db;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON zucane_db.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 2. Crear tablas
python app.py  # Dejar correr unos segundos, luego Ctrl+C

# 3. Insertar datos de prueba
mysql -u user -p zucane_db
# Ejecutar comandos SQL de la sección 5.6
```

#### 5.1 Crear base de datos y usuario
```bash

# Crear base de datos
CREATE DATABASE zucane_db;

# Crear usuario
CREATE USER 'user'@'localhost' IDENTIFIED BY 'pass';

# Dar permisos
GRANT ALL PRIVILEGES ON zucane_db.* TO 'user'@'localhost';
FLUSH PRIVILEGES;

# Verificar que funciona
USE zucane_db;
SHOW TABLES;
EXIT;
```

#### 5.2 Crear tablas y datos manualmente

**Paso 1: Crear las tablas**
```bash
# Ejecutar la aplicación para crear las tablas
python app.py
# Dejar corriendo unos segundos y luego Ctrl+C para detener
```

Esto creará automáticamente:
- ✅ Todas las tablas de la base de datos
- ✅ Estructura completa del sistema

**Paso 2: Insertar datos de prueba**
```bash
# Conectar a MySQL
mysql -u user -p zucane_db

# Ejecutar los comandos SQL de la sección 5.6
# (Roles, usuario admin, empresa de prueba, tokens)
```

**Paso 3: Verificar que todo funciona**
```bash
# Ejecutar la aplicación nuevamente
python app.py
# Ir a http://localhost:8000/docs para probar
```

#### 5.3 Verificar configuración
```bash
# Conectar con el usuario creado
mysql -u user -p zucane_db

# Verificar tablas creadas
SHOW TABLES;

# Verificar datos insertados
SELECT * FROM users;
SELECT * FROM roles;
SELECT * FROM empresas;
SELECT * FROM tokens_co2;
```

#### 5.4 Datos de prueba incluidos

**Usuario Administrador:**
- Email: `admin@gobierno.mx`
- Password: `admin123`
- Rol: `GOV_ADMIN`

**Empresa de Prueba:**
- RFC: `ABC123456789`
- Nombre: `Empresa de Prueba S.A. de C.V.`
- Email: `contacto@empresaprueba.com`
- **Claves Stellar**: Se generan automáticamente al crear la empresa

**Tipos de RFC soportados:**
- **Persona Física**: 13 caracteres (ej: `ABCD123456EF1`)
- **Persona Moral**: 12 caracteres (ej: `COS621024897`)

**Tokens de Prueba:**
- 3 tokens de 1.0 tonelada CO2 cada uno
- Status: `disponible`
- Asset: `XOCHI`

#### 5.5 Estructura de tablas creadas

```sql
-- Tablas principales
users                    # Usuarios del sistema
roles                    # Roles (GOV_ADMIN, COMPANY_USER)
empresas                 # Empresas compradoras
tokens_co2              # Tokens de CO2
transacciones           # Transacciones de compra
pagos_productores       # Pagos a productores
audit_logs              # Registros de auditoría
idempotency_keys        # Claves de idempotencia
outbox_events           # Eventos para procesar
orders                  # Órdenes de compra
order_items             # Items de órdenes
transaccion_items       # Items de transacciones
usuario_roles           # Relación usuarios-roles
```

#### 5.6 Comandos SQL manuales (si necesitas hacerlo paso a paso)

**Crear roles del sistema:**
```sql
INSERT INTO roles (nombre, descripcion) VALUES 
('GOV_ADMIN', 'Administrador del gobierno'),
('COMPANY_USER', 'Usuario de empresa');
```

**Crear usuario administrador:**
```sql
INSERT INTO users (email, password_hash, nombre, apellido, telefono, created_at) VALUES 
('admin@gobierno.mx', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Admin', 'Sistema', '555-0001', NOW());
```

**Crear empresa de prueba:**
```sql
-- Nota: Las claves Stellar se generan automáticamente al crear la empresa
-- Usar el endpoint POST /api/v1/empresas/ en lugar de SQL directo
```

**Emitir tokens de prueba:**
```sql
INSERT INTO tokens_co2 (cantidad_co2, asset_code, issuer_pubkey, dist_pubkey, status, created_at) VALUES 
(1.0, 'XOCHI', 'GBL44HGF3K7NLLCIKIEILGVHMASXB7QAZROZU2XISRFOJG6R4GNWZ6RY', 'GCTWI7YUCLHG2KAYZPN2VZGLKXITW474P2CMP2UJTTH56PGDL72YLLNZ', 'disponible', NOW()),
(1.0, 'XOCHI', 'GBL44HGF3K7NLLCIKIEILGVHMASXB7QAZROZU2XISRFOJG6R4GNWZ6RY', 'GCTWI7YUCLHG2KAYZPN2VZGLKXITW474P2CMP2UJTTH56PGDL72YLLNZ', 'disponible', NOW()),
(1.0, 'XOCHI', 'GBL44HGF3K7NLLCIKIEILGVHMASXB7QAZROZU2XISRFOJG6R4GNWZ6RY', 'GCTWI7YUCLHG2KAYZPN2VZGLKXITW474P2CMP2UJTTH56PGDL72YLLNZ', 'disponible', NOW());
```

#### 5.7 Solución de problemas comunes

**Error: "Access denied for user 'user'@'localhost'"**
```bash
# Verificar que el usuario existe
mysql -u root -p
SELECT User, Host FROM mysql.user WHERE User = 'user';
```

**Error: "Database 'zucane_db' doesn't exist"**
```bash
# Crear la base de datos manualmente
mysql -u root -p
CREATE DATABASE zucane_db;
```

**Error: "Table doesn't exist"**
```bash
# Ejecutar la aplicación para crear tablas
python app.py
```

**Error: "Duplicate entry"**
```bash
# Limpiar datos existentes
mysql -u user -p zucane_db
DROP DATABASE zucane_db;
CREATE DATABASE zucane_db;
# Luego ejecutar python app.py y los comandos SQL de la sección 5.6
```

**Error: "Column 'stellar_public_key' cannot be null"**
```bash
# Verificar que la empresa tiene stellar_public_key
mysql -u user -p zucane_db
SELECT rfc, nombre, stellar_public_key FROM empresas;
```

#### 5.8 Verificación rápida del setup

**Comando de verificación completa:**
```bash
# Verificar que todo está configurado correctamente
mysql -u user -p zucane_db -e "
SELECT 'USERS' as tabla, COUNT(*) as registros FROM users
UNION ALL
SELECT 'ROLES', COUNT(*) FROM roles
UNION ALL
SELECT 'EMPRESAS', COUNT(*) FROM empresas
UNION ALL
SELECT 'TOKENS', COUNT(*) FROM tokens_co2;
"
```

**Resultado esperado:**
```
+----------+-----------+
| tabla    | registros |
+----------+-----------+
| USERS    |         1 |
| ROLES    |         2 |
| EMPRESAS |         1 |
| TOKENS   |         3 |
+----------+-----------+
```

**Verificar datos específicos:**
```bash
# Usuario admin
mysql -u user -p zucane_db -e "SELECT email, nombre FROM users WHERE email = 'admin@gobierno.mx';"

# Empresa de prueba
mysql -u user -p zucane_db -e "SELECT rfc, nombre, stellar_public_key FROM empresas WHERE rfc = 'ABC123456789';"

# Tokens disponibles
mysql -u user -p zucane_db -e "SELECT token_id, cantidad_co2, status FROM tokens_co2 WHERE status = 'disponible';"
```

## 🎯 Uso

### 1. Ejecutar la aplicación
```bash
python app.py
```

### 2. Acceder a la documentación
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 📚 API Endpoints

### 🔐 Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/auth/profile/{user_id}` - Obtener perfil
- `POST /api/v1/auth/logout` - Cerrar sesión

### 🏢 Empresas
- `POST /api/v1/empresas/` - Crear empresa
- `GET /api/v1/empresas/{id}` - Obtener empresa
- `GET /api/v1/empresas/rfc/{rfc}` - Buscar por RFC
- `GET /api/v1/empresas/` - Listar empresas
- `PUT /api/v1/empresas/{id}` - Actualizar empresa
- `PATCH /api/v1/empresas/{id}/activar` - Activar empresa
- `PATCH /api/v1/empresas/{id}/desactivar` - Desactivar empresa

### 🪙 Tokens CO2
- `POST /api/v1/tokens/` - Emitir token
- `GET /api/v1/tokens/{id}` - Obtener token
- `GET /api/v1/tokens/` - Listar tokens disponibles
- `GET /api/v1/tokens/status/{status}` - Filtrar por status
- `POST /api/v1/tokens/reservar` - Reservar tokens
- `POST /api/v1/tokens/liberar` - Liberar tokens
- `POST /api/v1/tokens/vender` - Marcar como vendidos
- `GET /api/v1/tokens/inventario/summary` - Resumen de inventario

### 💰 Transacciones
- `POST /api/v1/transacciones/` - Crear transacción
- `GET /api/v1/transacciones/{id}` - Obtener transacción
- `GET /api/v1/transacciones/empresa/{id}` - Por empresa
- `GET /api/v1/transacciones/status/{status}` - Por status
- `POST /api/v1/transacciones/{id}/confirmar` - Confirmar
- `POST /api/v1/transacciones/{id}/fallar` - Marcar como fallida
- `GET /api/v1/transacciones/pendientes/procesar` - Procesar pendientes

### 🌟 Pagos Stellar
- `POST /api/v1/transacciones/stellar/pagar` - Pagar con Stellar
- `POST /api/v1/transacciones/stellar/verificar` - Verificar pago
- `POST /api/v1/transacciones/stellar/balance` - Consultar balance
- `POST /api/v1/payments/process` - Procesar pago directo
- `POST /api/v1/payments/verify` - Verificar pago directo
- `POST /api/v1/payments/balance` - Balance de empresa
- `GET /api/v1/payments/stellar/info` - Información Stellar

### 💳 Pagos a Productores
- `POST /api/v1/pagos/` - Crear pago
- `GET /api/v1/pagos/{id}` - Obtener pago
- `GET /api/v1/pagos/transaccion/{id}` - Por transacción
- `GET /api/v1/pagos/status/{status}` - Por status
- `POST /api/v1/pagos/{id}/completar` - Completar pago
- `PUT /api/v1/pagos/{id}` - Actualizar pago
- `GET /api/v1/pagos/pendientes/listar` - Listar pendientes
- `GET /api/v1/pagos/resumen/summary` - Resumen estadístico

### 📊 Auditoría
- `POST /api/v1/auditoria/` - Crear auditoría
- `GET /api/v1/auditoria/{id}` - Obtener auditoría
- `GET /api/v1/auditoria/transaccion/{id}` - Por transacción
- `GET /api/v1/auditoria/usuario/{id}` - Por usuario
- `POST /api/v1/auditoria/buscar` - Buscar con filtros
- `GET /api/v1/auditoria/` - Listar todas
- `PUT /api/v1/auditoria/{id}` - Actualizar auditoría
- `POST /api/v1/auditoria/registrar` - Registrar acción rápida
- `GET /api/v1/auditoria/resumen/summary` - Resumen estadístico

## 🌟 Integración Stellar

### Características
- **Generación Automática de Claves**: Claves Stellar determinísticas basadas en datos de la empresa
- **Validación Real**: Claves Stellar validadas con `stellar_sdk.StrKey`
- **Transacciones Reales**: Pagos procesados en la red Stellar
- **Verificación Automática**: Confirmación de transacciones
- **Consultas de Balance**: Balance real de cuentas Stellar
- **Manejo de Errores**: Gestión robusta de errores de red

### Generación Determinística de Claves
El sistema genera automáticamente claves Stellar únicas para cada empresa basándose en:
- **RFC de la empresa** (12-13 caracteres, persona física o moral)
- **Email de contacto**
- **Nombre de la empresa**

**Ventajas:**
- ✅ **No requiere claves manuales** - Se generan automáticamente
- ✅ **Determinísticas** - Mismos datos = mismas claves
- ✅ **Únicas** - Diferentes datos = claves diferentes
- ✅ **Seguras** - Basadas en HMAC-SHA256
- ✅ **Consistentes** - Siempre reproducibles

### Flujo de Transacción
1. **Crear Transacción** → Status: "pendiente"
2. **Reservar Token** → Status: "reservado"
3. **Procesar Pago Stellar** → Pago real en blockchain
4. **Verificar Pago** → Confirmación en Stellar
5. **Confirmar Transacción** → Status: "confirmada"
6. **Marcar Token Vendido** → Status: "vendido"

### Configuración Stellar
- **Red**: Testnet (desarrollo)
- **Asset**: XOCHI
- **Gobierno**: GBL44HGF3K7NLLCIKIEILGVHMASXB7QAZROZU2XISRFOJG6R4GNWZ6RY
- **Tesorería**: GCTWI7YUCLHG2KAYZPN2VZGLKXITW474P2CMP2UJTTH56PGDL72YLLNZ

## 📋 Documentación Swagger

### Características
- **Documentación Completa**: Cada endpoint documentado
- **Interfaz Interactiva**: Prueba endpoints desde el navegador
- **Validación en Tiempo Real**: Valida datos antes de enviar
- **Esquemas de Datos**: Estructura completa de DTOs
- **Códigos de Error**: Documentación de errores posibles

### Estructura de Documentación
Cada endpoint incluye:
- **TÍTULO** - Nombre claro del endpoint
- **QUE HACE** - Lista de acciones que realiza
- **COMO USAR** - Pasos numerados para usar el endpoint
- **RESPUESTA** - Campos que devuelve

## 🔒 Seguridad

- **Variables de Entorno**: Configuración segura
- **Validación Stellar**: Claves públicas validadas
- **Autenticación**: Sistema de login básico
- **Auditoría**: Trazabilidad completa
- **Base de Datos**: Transacciones ACID

## 📚 Dependencias Principales

- `fastapi` - Framework web moderno
- `sqlalchemy` - ORM para base de datos
- `mysqlclient` - Driver MySQL
- `stellar-sdk` - SDK oficial de Stellar
- `pydantic` - Validación de datos
- `uvicorn` - Servidor ASGI
- `python-dotenv` - Variables de entorno

## 🚀 Flujo de Trabajo

### 1. Configuración Inicial
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar base de datos
python setup_database.py

# 3. Ejecutar aplicación
python app.py
```

### 2. Uso Básico
1. **Acceder a Swagger**: `http://localhost:8000/docs`
2. **Crear empresa** con clave Stellar válida
3. **Emitir tokens** de CO2
4. **Crear transacción** de compra
5. **Procesar pago** con Stellar
6. **Verificar transacción** en blockchain

### 3. Monitoreo
- **Auditoría**: Todos los cambios registrados
- **Logs**: Trazabilidad completa
- **Swagger**: Documentación interactiva
- **Base de Datos**: Estado persistente

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Notas

- **Stellar Testnet**: Usa red de prueba para desarrollo
- **Claves Configuradas**: Ya incluye claves válidas para testing
- **Documentación Completa**: Cada endpoint está documentado
- **Arquitectura Limpia**: Separación clara de responsabilidades
- **Integración Real**: No es simulación, es integración real con Stellar

## 🎯 Próximos Pasos

- [ ] Implementar autenticación JWT completa
- [ ] Agregar tests unitarios
- [ ] Agregar métricas y monitoreo
