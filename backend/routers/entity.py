from fastapi import APIRouter, HTTPException, Depends, Request

from backend.dependencies import check_have_discord_id
from backend.utils.console import console

router = APIRouter(
    prefix="/api/entity",
    tags=["entity"],

    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str, request: Request):
    console.log(request.session.get('discord_id'))

    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str, request: Request):
    console.log(request.session.get('discord_id'))
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}