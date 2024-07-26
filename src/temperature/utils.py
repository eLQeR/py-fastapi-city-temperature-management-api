from http.client import HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.city.models import City
from src.temperature.models import Temperature
from src.config import API_KEY


async def get_async_client() -> AsyncClient:
    return AsyncClient()


async def fetch_temperature(session: AsyncSession, client: AsyncClient) -> None:
    stmt = select(City)
    cities_list = await session.execute(stmt)
    for city_tuple in cities_list.fetchall():
        city = city_tuple[0]
        res = await client.get(
            url="https://api.openweathermap.org/data/2.5/weather",
            params={'units': 'metric', "q": f"{city.name}", 'lang': 'ru', 'APPID': "a7a7fbefc785e02a7434d574acba0433"}
        )
        if res.status_code != 200:
            raise HTTPException("City not found")
        res = res.json()
        session.add(Temperature(
            city_id=city.id,
            temperature=res['main']['temp'],
        ))
    await session.commit()
    return {"result": "Temperature was fetched successfully"}
