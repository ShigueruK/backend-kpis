import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.auth import get_password_hash
from app.models import Usuario
import asyncio
from httpx import AsyncClient

# Base de datos de prueba: SQLite en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db?cache=shared"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribir la dependencia de la DB
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Usuario admin
    hashed_pw_admin = get_password_hash("admin123")
    admin = db.query(Usuario).filter(Usuario.email == "admin@example.com").first()
    if not admin:
        admin = Usuario(
            email="admin@example.com",
            nombre="Admin",
            rol="admin",
            hashed_password=hashed_pw_admin
        )
        db.add(admin)
    
    # Usuario vendedor (para pruebas de permisos)
    hashed_pw_vendedor = get_password_hash("vendedor123")
    vendedor = db.query(Usuario).filter(Usuario.email == "vendedor@example.com").first()
    if not vendedor:
        vendedor = Usuario(
            email="vendedor@example.com",
            nombre="Vendedor Test",
            rol="vendedor",
            hashed_password=hashed_pw_vendedor
        )
        db.add(vendedor)
    
    db.commit()
    
    # Opcional: insertar datos de prueba en las tablas de KPIs
    # (Si no hay datos, los tests pasarán con listas vacías, pero es mejor tener datos reales)
    # Aquí puedes agregar filas a VentasMensualesDB, TopProductosDB, etc.
    
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client