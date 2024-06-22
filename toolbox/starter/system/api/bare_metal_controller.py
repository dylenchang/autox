"""BareMetal operation controller"""

from fastapi import APIRouter, Depends, WebSocket

from toolbox.common.schema.schema import CurrentUser
from toolbox.common.security.security import get_current_user
from toolbox.common.util.ws import handle_playbook_result
from toolbox.starter.system.factory.service_factory import (
    get_bare_metal_service,
)
from toolbox.starter.system.schema.bare_metal_schema import RedisDeployCmd, UserDeployCmd
from toolbox.starter.system.schema.base_deploy_schema import BaseDeployCmd
from toolbox.starter.system.service.bare_metal_service import BareMetalService

bare_metal_router = APIRouter()
bare_metal_service: BareMetalService = get_bare_metal_service()


@bare_metal_router.websocket("/source")
async def change_source(
        websocket: WebSocket, current_user: CurrentUser = Depends(get_current_user)
):
    await websocket.accept()
    while True:
        req = await websocket.receive_text()
        baseDeployCmd: BaseDeployCmd = BaseDeployCmd.parse_raw(req)
        process = await bare_metal_service.source_deploy(baseDeployCmd)
        await handle_playbook_result(process, websocket)


@bare_metal_router.websocket("/redis")
async def deploy_redis(
        websocket: WebSocket, current_user: CurrentUser = Depends(get_current_user)
):
    await websocket.accept()
    while True:
        req = await websocket.receive_text()
        redisDeployCmd: RedisDeployCmd = RedisDeployCmd.parse_raw(req)
        process = await bare_metal_service.redis_deploy(redisDeployCmd)
        await handle_playbook_result(process, websocket)


@bare_metal_router.websocket("/user")
async def deploy_redis(
        websocket: WebSocket, current_user: CurrentUser = Depends(get_current_user)
):
    await websocket.accept()
    while True:
        req = await websocket.receive_text()
        userDeployCmd: UserDeployCmd = UserDeployCmd.parse_raw(req)
        process = await bare_metal_service.user_deploy(userDeployCmd)
        await handle_playbook_result(process, websocket)
