from fastapi import APIRouter, status

route = APIRouter()


@route.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck() -> dict:
    return {"status": "ok"}
