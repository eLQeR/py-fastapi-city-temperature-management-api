from typing import List

from fastapi import APIRouter, Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.temperature import schemas, crud
from src.temperature.utils import get_async_client, fetch_temperature
from src.database import get_async_session

router = APIRouter()


@router.get("/temperatures/update/")
async def fetch_temperatures(
        client: AsyncClient() = Depends(get_async_client),
        session: AsyncSession = Depends(get_async_session),

):
    return await fetch_temperature(
        session=session,
        client=client
    )


@router.get("/temperatures/updae/")
async def fetch_temperatures(
    city: str,
    client: AsyncClient() = Depends(get_async_client)
):
    res = await client.get(
        url="https://api.openweathermap.org/data/2.5/weather",
        params={'units': 'metric', "q": f"{city}", 'lang': 'ru', 'APPID': "a7a7fbefc785e02a7434d574acba0433"}
    )
    if res.status_code == 200:
        return res.json()
    return {"result": "City not found"}


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
        city_id: int,
        session: AsyncSession = Depends(get_async_session),

):
    return await crud.get_temperature(
        session=session,
        city_id=city_id
    )
