from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(String(20), nullable=False, default="vendedor")
    created_at = Column(DateTime, server_default=func.now())

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
    