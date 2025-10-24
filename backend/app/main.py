from fastapi import FastAPI
from .session import init_db
from contextlib import asynccontextmanager

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


# root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the MOradai API 👾"}