from fastapi import FastAPI
from .session import init_db
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api.v1 import user, referalcode,auth


# lifespan context manager
# this runs code when the app starts and shuts down.
# here we initialize the database tables on startup.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Creando tablas si no existen...")
    await init_db()
    yield
    print("🧹 Cerrando aplicación...")


#app info
app = FastAPI(
    title="Moradai API",
    version="1.0.0",
    description="Moradai Backend",
    lifespan=lifespan,
)

app.include_router(user.router)
app.include_router(referalcode.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the MOradai API 👾"}