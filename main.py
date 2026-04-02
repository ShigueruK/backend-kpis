from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:Matier620@localhost/kpi_dashboard"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Modelos SQLAlchemy (reflejan las tablas) ---
class VentasMensualesDB(Base):
    __tablename__ = "ventas_mensuales"
    id = Column(Integer, primary_key=True, index=True)
    mes = Column(String)
    ventas = Column(Integer)
    objetivo = Column(Integer)

class TopProductosDB(Base):
    __tablename__ = "top_productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ventas = Column(Integer)

class CumplimientoDB(Base):
    __tablename__ = "cumplimiento"
    id = Column(Integer, primary_key=True, index=True)
    promedio = Column(Integer)
    meses_sobre_objetivo = Column(Integer)
    mejor_mes = Column(String)

# --- Esquemas Pydantic (para validación y serialización) ---
class VentasMensuales(BaseModel):
    mes: str
    ventas: int
    objetivo: int

class TopProductos(BaseModel):
    nombre: str
    ventas: int

class Cumplimiento(BaseModel):
    promedio: int
    meses_sobre_objetivo: int
    mejor_mes: str

# --- Crear la app FastAPI ---
app = FastAPI()

# Configurar CORS para permitir peticiones desde React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependencia para obtener sesión de BD ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---
@app.get("/ventas-mensuales", response_model=list[VentasMensuales])
def get_ventas():
    db = SessionLocal()
    ventas = db.query(VentasMensualesDB).order_by(VentasMensualesDB.id).all()
    db.close()
    return ventas

@app.get("/top-productos", response_model=list[TopProductos])
def get_top_productos():
    db = SessionLocal()
    productos = db.query(TopProductosDB).order_by(TopProductosDB.ventas.desc()).all()
    db.close()
    return productos

@app.get("/cumplimiento", response_model=Cumplimiento)
def get_cumplimiento():
    db = SessionLocal()
    cumplimiento = db.query(CumplimientoDB).first()
    db.close()
    return cumplimiento

