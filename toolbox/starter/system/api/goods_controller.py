"""Goods operation controller"""
import io
import os
import tempfile
import zipfile
from fastapi import APIRouter, UploadFile, File, Depends, WebSocket
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from toolbox.common.result import result
from toolbox.common.schema.schema import CurrentUser
from toolbox.common.security.security import get_current_user
from toolbox.common.util.file import generate_playbook_paths
from toolbox.starter.system.enum.system import SystemResponseCode
from toolbox.starter.system.exception.system import SystemException
from toolbox.starter.system.factory.service_factory import get_goods_service
from toolbox.starter.system.model.goods_do import GoodsDO
from toolbox.starter.system.schema.goods_schema import RedisDeployCmd
from toolbox.starter.system.service.goods_service import GoodsService

goods_router = APIRouter()
goods_service: GoodsService = get_goods_service()


@goods_router.post("/")
async def upload_zip(
        file: UploadFile = File(...),
        file_name: str = None,
        url: str = None,
        description: str = None,
        current_user: CurrentUser = Depends(get_current_user()),
):
    if not file.filename.endswith(".zip"):
        raise SystemException(
            code=SystemResponseCode.MEDIA_TYPE_ERROR.code,
            msg=SystemResponseCode.MEDIA_TYPE_ERROR.msg,
        )

    # 读取 ZIP 文件为二进制流
    binary_data = await file.read()
    goods_record = GoodsDO(
        name=file_name, pic_url=url, description=description, data=binary_data
    )
    goods_record = await goods_service.save(record=goods_record)
    return result.success(data=goods_record.id)


@goods_router.websocket("/redis")
async def redis(websocket: WebSocket, current_user: CurrentUser = Depends(get_current_user)):
    await websocket.accept()
    try:
        while True:
            req = await websocket.receive_text()
            redisDeployCmd: RedisDeployCmd = RedisDeployCmd.parse_raw(req)
            process = await goods_service.redis_deploy(redisDeployCmd)
            for line in iter(process.stdout.readline, ""):
                await websocket.send_text(line)
            process.stdout.close()
            process.wait()
            await websocket.send_text("Playbook execution finished.")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
