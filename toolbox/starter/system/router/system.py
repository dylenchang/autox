"""Routing of system modules"""

from fastapi import APIRouter

from toolbox.common.config import configs
from toolbox.starter.server import app
from toolbox.starter.system.api.v1.probe_controller import probe_router
from toolbox.starter.system.api.v1.user_controller import user_router
from toolbox.starter.system.api.v1.inventory_controller import inventory_router

system_router = APIRouter()
system_router.include_router(probe_router, tags=["probe"], prefix="/probe")
system_router.include_router(user_router, tags=["user"], prefix="/user")
system_router.include_router(inventory_router, tags=["inventory"], prefix="/inventory")

# Add system routing
app.include_router(system_router, prefix=configs.api_version)
