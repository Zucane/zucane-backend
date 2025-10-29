# QRise Backend - Stellar Network Integration

Este proyecto maneja la integración con la red Stellar para el proyecto Zucane, incluyendo la generación de claves, establecimiento de trustlines y emisión de tokens.

## 🚀 Características

- Generación automática de pares de claves para Government y Treasury
- Establecimiento de trustlines en la red Stellar
- Emisión y fondeo de tokens personalizados
- Configuración segura usando variables de entorno
- Estructura de proyecto profesional

## 📁 Estructura del Proyecto

```
QRise-BackEnd/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuración con variables de entorno
│   ├── 0_generate_keys.py     # Generador de claves (ejecutar solo una vez)
│   └── stellar_setup.py       # Setup principal de Stellar
├── .env                       # Variables de entorno (NO committear)
├── .gitignore                 # Archivos a ignorar en Git
├── requirements.txt           # Dependencias de Python
├── main.py                    # Punto de entrada principal
└── README.md                  # Este archivo
```

## 🛠️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd QRise-BackEnd
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
   - Copia el archivo `.env.example` a `.env` (si existe)
   - O crea un archivo `.env` con las siguientes variables:
   ```env
   GOVERNMENT_PUBLIC_KEY=tu_clave_publica_government
   GOVERNMENT_SECRET_KEY=tu_clave_secreta_government
   TREASURY_PUBLIC_KEY=tu_clave_publica_treasury
   TREASURY_SECRET_KEY=tu_clave_secreta_treasury
   ASSET_NAME=XOCHI
   HORIZON_URL=https://horizon-testnet.stellar.org
   ```

## 🎯 Uso

### 1. Generar Claves (Solo la primera vez)

```bash
python src/0_generate_keys.py
```

Este script generará las claves de Government y Treasury, y las activará en la red de prueba de Stellar. **IMPORTANTE**: Guarda estas claves en tu archivo `.env`.

### 2. Ejecutar Setup Principal

```bash
python main.py
```

O ejecutar directamente:

```bash
python src/stellar_setup.py
```

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

