# 📊 API de Dashboard de KPIs de Ventas

API REST construida con **FastAPI** que sirve datos de ventas, productos, cumplimiento y ventas por categoría, con autenticación JWT y roles (admin, gerente, vendedor).

## 🚀 Tecnologías

- **FastAPI** – Framework web para APIs
- **SQLAlchemy** – ORM para PostgreSQL
- **PostgreSQL** – Base de datos relacional
- **JWT** – Autenticación stateless
- **bcrypt** – Hashing de contraseñas
- **Uvicorn** – Servidor ASGI
- **Pydantic** – Validación de datos

## 📦 Instalación local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ShigueruK/backend-kpis.git
   cd backend-kpis
   
2. Crea y activa un entorno virtual
    ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
    
3. Instala dependencias:
    ```bash
    pip install -r requirements.txt

4. Crea un archivo .env en la raíz con:
    ```bash
    DATABASE_URL=postgresql://postgres:tu_contraseña@localhost/kpi_dashboard
    SECRET_KEY=mi_clave_secreta_super_segura

5. Asegura que PostgreSQL esté corriendo y crea la base de datos kpi_dashboard. Luego ejecuta las migraciones (o crea las tablas manualmente con el script schema.sql).

6. Corre la API:
   ```bash
   uvicorn main:app --reload

7. Documentación interactiva: http://localhost:8000/docs

📌 Endpoints principales

Método	  Endpoint	          Descripción	                                        Autenticación
POST	    /registro	                Registrar nuevo usuario	                      No
POST	    /login	                  Iniciar sesión (devuelve token)	              No
GET	      /perfil	                  Obtener datos del usuario autenticado	        Sí (Bearer)
GET	      /ventas-mensuales	        Ventas mensuales vs objetivo	                Sí
GET	      /top-productos	          Top 5 productos más vendidos	                Sí
GET	      /cumplimiento	            Resumen de cumplimiento	                      Sí
GET	      /ventas-por-categoria	    Ventas por categoría (solo admin/gerente)	    Sí

🗂️ Estructura del proyecto

backend/
├── main.py           # Punto de entrada, endpoints
├── models.py         # Modelos SQLAlchemy
├── auth.py           # Autenticación JWT, hashing
├── database.py       # Conexión a BD, sesiones
├── requirements.txt  # Dependencias
├── .env              # Variables de entorno (no subir)
└── README.md

🔐 Credenciales de prueba (local)

Puedes crear usuarios vía /registro o usar estos (si los insertaste en la BD):

Admin: admin@example.com / admin123
Gerente: gerente@example.com / gerente123
Vendedor: vendedor@example.com / vendedor123

🌐 Despliegue
El backend está desplegado en Render: https://backend-kpis.onrender.com
(Tengo que reemplazarlo cuando lo tenga listo)
