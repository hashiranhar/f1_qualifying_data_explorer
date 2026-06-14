import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import DriverResult, DriversListResponse
from data_loader import load_json, get_all_drivers, get_driver_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent.parent / "data" / "session_laptimes.json"

app_state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app_state["data"] = load_json(str(DATA_PATH))
        logger.info("Dataset loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        app_state["data"] = None
    yield
    app_state.clear()


app = FastAPI(title="F1 Qualifying Explorer", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_data():
    if app_state.get("data") is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    return app_state["data"]


@app.get("/api/drivers", response_model=DriversListResponse)
def drivers():
    return {"drivers": get_all_drivers(get_data())}


@app.get("/api/driver/{code}", response_model=DriverResult)
def driver(code: str):
    result = get_driver_result(get_data(), code)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Driver '{code.upper()}' not found")
    return result