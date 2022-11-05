from backend.utils.console import console
from fastapi import Request


async def login(request: Request):
    console.log(request.session['discord_id'])
    return request.session