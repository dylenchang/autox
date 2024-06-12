"""Routing of system modules"""

from fastapi import APIRouter

from toolbox.common.config import configs
from toolbox.starter.server import app
from toolbox.starter.system.api.v1.probe_controller import probe_router
from toolbox.starter.system.api.v1.user_controller import user_router
from toolbox.starter.system.api.v1.role_controller import role_router

system_router = APIRouter()
system_router.include_router(probe_router, tags=["probe"], prefix="/probe")
system_router.include_router(user_router, tags=["user"], prefix="/user")
system_router.include_router(role_router, tags=["role"], prefix="/role")

# Add system routing
app.include_router(system_router, prefix=configs.api_version)
