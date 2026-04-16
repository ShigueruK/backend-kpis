from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from models import Usuario, VentasMensualesDB, TopProductosDB, CumplimientoDB, VentasPorCategoriaDB
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from database import engine, get_db, Base
class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str = "vendedor"
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
class VentasPorCategoria(BaseModel):
    categoria: str
    ventas: int
    mes: str
    año: int
# Crear la app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=False,
    allow_methods=["*"],                  
    allow_headers=["*"],                       
)
from database import Base
Base.metadata.create_all(bind=engine)

# --- Endpoints públicos ---
@app.post("/registro")
def register(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    hashed = get_password_hash(usuario.password)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hashed,
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"msg": "Usuario creado exitosamente", "email": nuevo_usuario.email}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.email, "rol": user.rol})
    return {"access_token": access_token, "token_type": "bearer", "rol": user.rol}

# --- Endpoints protegidos (requieren token) ---
@app.get("/ventas-mensuales", response_model=list[VentasMensuales])
def get_ventas(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    ventas = db.query(VentasMensualesDB).order_by(VentasMensualesDB.id).all()
    return ventas

@app.get("/top-productos", response_model=list[TopProductos])
def get_top_productos(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    productos = db.query(TopProductosDB).order_by(TopProductosDB.ventas.desc()).all()
    return productos

@app.get("/cumplimiento", response_model=Cumplimiento)
def get_cumplimiento(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    cumplimiento = db.query(CumplimientoDB).first()
    return cumplimiento

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.email, "rol": user.rol})
    return {"access_token": access_token, "token_type": "bearer", "rol": user.rol}

@app.get("/ventas-por-categoria", response_model=list[VentasPorCategoria])
def get_ventas_por_categoria(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo admin o gerente pueden ver este KPI
    if current_user.rol not in ["admin", "gerente"]:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    ventas_cat = db.query(VentasPorCategoriaDB).all()
    return ventas_cat

@app.get("/perfil")
def get_perfil(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.rol,
        "created_at": str(current_user.created_at)
    }

