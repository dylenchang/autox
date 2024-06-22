"""BareMetal operation controller"""

from fastapi import APIRouter, Depends, WebSocket
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from toolbox.common.schema.schema import CurrentUser
from toolbox.common.security.security import get_current_user
from toolbox.starter.system.factory.service_factory import (
    get_bare_metal_service,
)
from toolbox.starter.system.schema.bare_metal_schema import RedisDeployCmd
from toolbox.starter.system.service.bare_metal_service import BareMetalService

bare_metal_router = APIRouter()
bare_metal_service: BareMetalService = get_bare_metal_service()


@bare_metal_router.websocket("/redis")
async def redis(
    websocket: WebSocket, current_user: CurrentUser = Depends(get_current_user)
):
    await websocket.accept()
    try:
        while True:
            req = await websocket.receive_text()
            redisDeployCmd: RedisDeployCmd = RedisDeployCmd.parse_raw(req)
            process = await bare_metal_service.redis_deploy(redisDeployCmd)
            for line in iter(process.stdout.readline, ""):
                await websocket.send_text(line)
            process.stdout.close()
            process.wait()
            await websocket.send_text("Playbook execution finished.")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
