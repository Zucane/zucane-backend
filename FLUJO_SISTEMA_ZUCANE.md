# 🌱 FLUJO COMPLETO DEL SISTEMA ZUCANE

## 📊 DIAGRAMA DE FLUJO PRINCIPAL

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🌱 SISTEMA ZUCANE - FLUJO COMPLETO                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIOS   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│   (Empresa +    │    │   (Next.js)     │    │   (FastAPI)     │
│    Gobierno)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               1️⃣ AUTENTICACIÓN                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Accede a     │───▶│ 2. Muestra      │───▶│ 3. Valida       │
│    /login       │    │    LoginForm    │    │    credenciales  │
│                 │    │                 │    │                 │
│ 4. Ingresa      │───▶│ 5. Envía POST   │───▶│ 6. Crea JWT     │
│    credenciales │    │    /auth/login  │    │    token         │
│                 │    │                 │    │                 │
│ 7. Recibe       │◀───│ 8. Guarda       │◀───│ 9. Retorna      │
│    token JWT    │    │    token        │    │    token + user │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               2️⃣ DASHBOARD                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Ve dashboard │───▶│ 2. Carga datos  │───▶│ 3. Obtiene      │
│    principal    │    │    del usuario   │    │    datos empresa│
│                 │    │                 │    │                 │
│ 4. Ve resumen   │◀───│ 5. Muestra      │◀───│ 6. Retorna      │
│    de tokens    │    │    Dashboard    │    │    estadísticas │
│    disponibles  │    │    Component    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               3️⃣ EXPLORAR TOKENS                              │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Navega a     │───▶│ 2. Carga lista  │───▶│ 3. Obtiene      │
│    /tokens      │    │    de tokens    │    │    tokens       │
│                 │    │                 │    │    disponibles  │
│                 │    │                 │    │                 │
│ 4. Filtra/      │───▶│ 5. Envía filtros│───▶│ 6. Aplica       │
│    busca tokens │    │    GET /tokens  │    │    filtros      │
│                 │    │                 │    │                 │
│ 7. Ve tokens    │◀───│ 8. Muestra      │◀───│ 9. Retorna      │
│    filtrados    │    │    TokenList    │    │    tokens       │
│                 │    │                 │    │    filtrados    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               4️⃣ CREAR RESERVA                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Selecciona   │───▶│ 2. Muestra      │───▶│ 3. Valida       │
│    tokens       │    │    carrito      │    │    disponibilidad│
│                 │    │                 │    │                 │
│ 4. Confirma     │───▶│ 5. Envía POST   │───▶│ 6. Crea Order   │
│    compra       │    │    /orders      │    │    con TTL      │
│                 │    │                 │    │                 │
│ 7. Ve reserva   │◀───│ 8. Muestra      │◀───│ 9. Retorna      │
│    creada       │    │    confirmación │    │    Order ID     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               5️⃣ PAGAR CON STELLAR                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Conecta      │───▶│ 2. Integra      │───▶│ 3. Valida       │
│    wallet       │    │    Stellar SDK  │    │    wallet       │
│    Stellar      │    │                 │    │                 │
│                 │    │                 │    │                 │
│ 4. Confirma     │───▶│ 5. Firma        │───▶│ 6. Crea         │
│    pago         │    │    transacción  │    │    Transacción  │
│                 │    │                 │    │                 │
│ 7. Ve pago      │◀───│ 8. Muestra      │◀───│ 9. Confirma     │
│    confirmado   │    │    confirmación │    │    en blockchain│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               6️⃣ CONFIRMACIÓN                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Ve tokens    │◀───│ 2. Actualiza    │◀───│ 3. Actualiza    │
│    comprados    │    │    estado       │    │    estados      │
│                 │    │                 │    │                 │
│ 4. Ve historial │◀───│ 5. Muestra      │◀───│ 6. Registra     │
│    de compras   │    │    Transaccion  │    │    auditoría    │
│                 │    │    List         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 FLUJOS ALTERNATIVOS

### **A. EXPIRACIÓN DE RESERVA**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. No paga      │    │ 2. Timer        │───▶│ 3. Job automático│
│    en 10 min    │    │    expiración   │    │    cada 1 min   │
│                 │    │                 │    │                 │
│ 4. Ve reserva   │◀───│ 5. Muestra      │◀───│ 6. Libera       │
│    expirada     │    │    notificación │    │    tokens       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **B. ERROR EN PAGO**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   👤 USUARIO    │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Pago falla   │◀───│ 2. Muestra      │◀───│ 3. Registra     │
│                 │    │    error        │    │    error        │
│                 │    │                 │    │                 │
│ 4. Reintenta    │───▶│ 5. Permite      │───▶│ 6. Valida       │
│    pago         │    │    reintento    │    │    nuevamente   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 PUNTOS CLAVE DEL FLUJO

### **1. Autenticación**
- **Frontend:** LoginForm, SocialLogin, ProfileCard
- **Backend:** `/api/v1/auth/*` endpoints
- **Flujo:** JWT tokens, roles, permisos

### **2. Gestión de Tokens**
- **Frontend:** TokenList, TokenCard, TokenSearch
- **Backend:** `/api/v1/tokens/*` endpoints
- **Flujo:** Listar, filtrar, buscar tokens disponibles

### **3. Sistema de Reservas**
- **Frontend:** NuevaReserva, ReservaList, ReservaCard
- **Backend:** `/api/v1/orders/*` endpoints
- **Flujo:** Crear reserva con TTL, expiración automática

### **4. Transacciones Stellar**
- **Frontend:** StellarWallet, PaymentForm
- **Backend:** `/api/v1/transacciones/*` endpoints
- **Flujo:** Integración con Stellar Network

### **5. Auditoría**
- **Frontend:** AuditoriaList, AuditoriaFiltros
- **Backend:** `/api/v1/auditoria/*` endpoints
- **Flujo:** Registro de todas las acciones

## 🏛️ FLUJO DEL GOBIERNO

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              🏛️ GOBIERNO - FLUJO COMPLETO                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│   (Admin)       │    │   (Next.js)     │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               1️⃣ LOGIN GOBIERNO                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Accede a     │───▶│ 2. Muestra      │───▶│ 3. Valida       │
│    /admin/login │    │    AdminLogin   │    │    credenciales  │
│                 │    │                 │    │    de gobierno   │
│ 4. Ingresa      │───▶│ 5. Envía POST   │───▶│ 6. Crea JWT     │
│    credenciales │    │    /auth/login  │    │    con rol      │
│    de admin     │    │                 │    │    GOV_ADMIN    │
│                 │    │                 │    │                 │
│ 7. Recibe       │◀───│ 8. Guarda       │◀───│ 9. Retorna      │
│    token admin  │    │    token        │    │    token + role │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               2️⃣ DASHBOARD GOBIERNO                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Ve dashboard │───▶│ 2. Carga datos  │───▶│ 3. Obtiene      │
│    de gobierno  │    │    administrativos│   │    estadísticas │
│                 │    │                 │    │    del sistema   │
│ 4. Ve resumen   │◀───│ 5. Muestra      │◀───│ 6. Retorna      │
│    del sistema  │    │    AdminDashboard│   │    métricas     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               3️⃣ EMITIR TOKENS CO2                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Navega a     │───▶│ 2. Muestra      │───▶│ 3. Obtiene      │
│    /admin/tokens│    │    TokenManager │    │    tokens       │
│                 │    │                 │    │    existentes   │
│                 │    │                 │    │                 │
│ 4. Crea nuevos  │───▶│ 5. Envía POST   │───▶│ 6. Crea tokens  │
│    tokens CO2   │    │    /tokens      │    │    en BD        │
│                 │    │                 │    │                 │
│ 7. Ve tokens    │◀───│ 8. Muestra      │◀───│ 9. Retorna      │
│    creados      │    │    confirmación │    │    tokens       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                   4️⃣ REGISTRAR TOKENS EN STELLAR NETWORK                      │
│                                                                                 │
│  ¿QUÉ SIGNIFICA "REGISTRAR EN STELLAR"?                                        │
│                                                                                 │
│  Cuando el gobierno crea tokens CO2 en la base de datos, solo existen          │
│  localmente. Para que sean tokens REALES y puedan usarse, deben registrarse    │
│  en Stellar Network (blockchain).                                              │
│                                                                                 │
│  PASOS DE REGISTRO:                                                            │
│  1. Gobierno crea activo "XOCHI" en Stellar                                    │
│  2. Establece trustline (confianza) entre Government y Treasury                │
│  3. Transfiere tokens desde Government → Treasury                              │
│  4. Los tokens ahora están en la blockchain y son verificables                 │
│                                                                                 │
│  BENEFICIOS:                                                                    │
│  ✅ Trazabilidad pública en blockchain                                         │
│  ✅ Inmutabilidad (no se pueden falsificar)                                    │
│  ✅ Verificación pública de autenticidad                                       │
│  ✅ Interoperabilidad con otras aplicaciones                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Selecciona   │───▶│ 2. Muestra      │───▶│ 3. Conecta con  │
│    tokens para  │    │    StellarForm  │    │    Stellar SDK  │
│    registrar    │    │                 │    │                 │
│                 │    │                 │    │                 │
│ 4. Confirma     │───▶│ 5. Envía POST   │───▶│ 6. Ejecuta:     │
│    registro     │    │    /tokens/     │    │    • Establece  │
│                 │    │    register     │    │      trustline  │
│                 │    │                 │    │    • Crea asset │
│                 │    │                 │    │      en Stellar │
│                 │    │                 │    │    • Transfiere │
│                 │    │                 │    │      tokens     │
│                 │    │                 │    │                 │
│ 7. Ve tokens    │◀───│ 8. Muestra      │◀───│ 9. Actualiza    │
│    en blockchain│    │    tx_hash      │    │    status +     │
│                 │    │    confirmación │    │    stellar_tx   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               5️⃣ GESTIONAR EMPRESAS                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Ve lista de  │───▶│ 2. Carga lista  │───▶│ 3. Obtiene      │
│    empresas     │    │    de empresas  │    │    empresas     │
│                 │    │                 │    │    registradas  │
│                 │    │                 │    │                 │
│ 4. Aprueba/     │───▶│ 5. Envía PUT    │───▶│ 6. Actualiza    │
│    rechaza      │    │    /empresas    │    │    status       │
│    empresas     │    │                 │    │    empresa      │
│                 │    │                 │    │                 │
│ 7. Ve cambios   │◀───│ 8. Muestra      │◀───│ 9. Retorna      │
│    aplicados    │    │    confirmación │    │    resultado    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               6️⃣ MONITOREAR TRANSACCIONES                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ GOBIERNO   │    │   🖥️ FRONTEND   │    │   🔧 BACKEND    │
│                 │    │                 │    │                 │
│ 1. Ve dashboard │───▶│ 2. Carga datos  │───▶│ 3. Obtiene      │
│    de transacciones│  │    de transacciones│  │    transacciones│
│                 │    │                 │    │    en tiempo real│
│                 │    │                 │    │                 │
│ 4. Ve reportes  │◀───│ 5. Muestra      │◀───│ 6. Genera       │
│    y métricas   │    │    Reportes     │    │    reportes     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📱 COMPONENTES PRINCIPALES DEL FRONTEND

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              🖥️ FRONTEND COMPONENTS                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🔐 AUTH       │    │   🏢 EMPRESAS   │    │   🪙 TOKENS     │
│                 │    │                 │    │                 │
│ • LoginForm     │    │ • EmpresaProfile│    │ • TokenList     │
│ • RegisterForm  │    │ • EmpresaSettings│   │ • TokenCard     │
│ • SocialLogin   │    │ • StellarWallet │    │ • TokenDetail   │
│ • ProfileCard   │    │                 │    │ • TokenSearch   │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   📋 RESERVAS   │    │   💳 TRANSACCIONES│   │   📊 AUDITORÍA  │
│                 │    │                 │    │                 │
│ • ReservaList   │    │ • TransaccionList│   │ • AuditoriaList │
│ • ReservaCard   │    │ • TransaccionCard│   │ • AuditoriaCard │
│ • NuevaReserva  │    │ • TransaccionDetail│  │ • AuditoriaFiltros│
│ • ReservaDetail │    │ • NuevaTransaccion│  │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   💰 PAGOS      │    │   🎨 SHARED     │    │   🔧 HOOKS      │
│                 │    │                 │    │                 │
│ • PagoList      │    │ • Layout        │    │ • useAuth       │
│ • PagoCard      │    │ • Navbar        │    │ • useApi        │
│ • PagoDetail    │    │ • Sidebar       │    │ • useTokens     │
│                 │    │ • Loading       │    │ • useReservas   │
│                 │    │ • ErrorBoundary │    │ • useTransacciones│
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🏛️ ADMIN      │    │   🌐 STELLAR    │    │   📈 REPORTES   │
│                 │    │                 │    │                 │
│ • AdminLogin    │    │ • StellarWallet │    │ • ReportesList  │
│ • AdminDashboard│    │ • StellarForm   │    │ • MetricasCard  │
│ • TokenManager  │    │ • StellarStatus │    │ • GraficosChart │
│ • EmpresaManager│    │ • StellarTx     │    │ • ExportData    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 TECNOLOGÍAS RECOMENDADAS

### **Frontend Stack:**
- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS
- **State:** Zustand
- **Forms:** React Hook Form + Zod
- **HTTP:** Axios
- **Icons:** Lucide React

### **Backend Stack:**
- **Framework:** FastAPI
- **Database:** MySQL + SQLAlchemy 2.0
- **Auth:** JWT + python-jose
- **Blockchain:** Stellar SDK
- **Docs:** Swagger/OpenAPI

## 📊 MÉTRICAS DE ÉXITO

### **UX Metrics:**
- ✅ Tiempo de login < 3 segundos
- ✅ Tiempo de carga de tokens < 2 segundos
- ✅ Tiempo de creación de reserva < 5 segundos
- ✅ Tiempo de pago < 10 segundos

### **Technical Metrics:**
- ✅ Uptime > 99.9%
- ✅ Response time < 200ms
- ✅ Error rate < 1%
- ✅ Mobile responsive 100%

---

**🎯 Este diagrama muestra el flujo completo del sistema Zucane, desde la autenticación hasta la confirmación de compra, con todos los componentes necesarios para el frontend.**
