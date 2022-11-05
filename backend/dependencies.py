from backend.utils.console import console
from fastapi import Request


async def get_discord_id(request: Request):
    console.log(request.session['discord_id'])
    return request.session