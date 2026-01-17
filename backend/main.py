import os
import django
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Setup Django before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmp_project.settings")
django.setup()

from api import blueprints, contracts

app = FastAPI(title="Contract Management Platform API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to close stale DB connections
@app.middleware("http")
async def close_db_connections(request, call_next):
    django.db.close_old_connections()
    response = await call_next(request)
    django.db.close_old_connections()
    return response

# Include Routers
app.include_router(blueprints.router, prefix="/api/blueprints", tags=["blueprints"])
app.include_router(contracts.router, prefix="/api/contracts", tags=["contracts"])

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

@app.get("/create-blueprint")
async def create_blueprint_page():
    return FileResponse(os.path.join(BASE_DIR, "static", "create_blueprint.html"))

@app.get("/create-contract")
async def create_contract_page():
    return FileResponse(os.path.join(BASE_DIR, "static", "create_contract.html"))

@app.get("/contract-detail")
async def contract_detail_page():
    return FileResponse(os.path.join(BASE_DIR, "static", "contract_detail.html"))
