"""Inventory operation controller"""

from typing import List, Dict

from fastapi import APIRouter, Depends, WebSocket
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from toolbox.common.result import result
from toolbox.common.schema.schema import CurrentUser
from toolbox.common.security.security import get_current_user
from toolbox.starter.system.factory.service_factory import get_inventory_service
from toolbox.starter.system.model.inventory_do import InventoryDO
from toolbox.starter.system.schema.inventory_schema import InventoryCreateCmd
from toolbox.starter.system.service.inventory_service import InventoryService

inventory_router = APIRouter()
inventory_service: InventoryService = get_inventory_service()


@inventory_router.post("/")
async def create_inventory(
    inventory_create_cmd: InventoryCreateCmd,
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Creates a new inventory with the provided data.

    Args:

        inventory_create_cmd: Command with inventory creation data.

        current_user: Current user performing the action.
    Returns:
        BaseResponse with created inventory ID.
    """
    ipv4_address = inventory_create_cmd.ipv4_address
    ipv6_address = inventory_create_cmd.ipv6_address
    if ipv4_address:
        await inventory_service.ping_ip(ip_address=ipv4_address)
    if ipv6_address:
        await inventory_service.ping_ip(ip_address=ipv6_address)
    inventory: InventoryDO = await inventory_service.save(
        record=InventoryDO(**inventory_create_cmd.model_dump())
    )
    return result.success(data=inventory.id)


@inventory_router.post("/inventories")
async def get_inventory(
    ids: List[int],
    current_user: CurrentUser = Depends(get_current_user()),
) -> dict:
    """
    Retrieves inventories by a list of ID.

    Args:

        ids: The unique identifiers of the inventories.

        current_user: Current user performing the action.

    Returns:
        BaseResponse with a list of InventoryDO details.
    """
    return result.success(data=await inventory_service.retrieve_by_ids(ids=ids))


@inventory_router.websocket("/ping")
async def ping_test(
    websocket: WebSocket, current_user: CurrentUser = Depends(get_current_user)
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            ids = data.get("ids", [])
            if not isinstance(ids, list):
                await websocket.send_json(
                    {"error": "Invalid input, 'ids' should be a list of integers."}
                )
                continue
            process = await inventory_service.ping_test(ids=ids)
            for line in iter(process.stdout.readline, ""):
                await websocket.send_text(line)
            process.stdout.close()
            process.wait()
            await websocket.send_text("Playbook execution finished.")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
