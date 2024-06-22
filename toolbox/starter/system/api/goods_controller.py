"""Goods operation controller"""

from fastapi import APIRouter, UploadFile, File, Depends

from toolbox.common.result import result
from toolbox.common.schema.schema import CurrentUser
from toolbox.common.security.security import get_current_user
from toolbox.starter.system.enum.system import SystemResponseCode
from toolbox.starter.system.exception.system import SystemException
from toolbox.starter.system.factory.service_factory import get_goods_service
from toolbox.starter.system.model.goods_do import GoodsDO
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
