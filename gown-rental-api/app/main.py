from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, gowns, appointments, rental_orders, gown_cares


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Gown Rental API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(gowns.router)
app.include_router(appointments.router)
app.include_router(rental_orders.router)
app.include_router(gown_cares.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
