from typing import Optional, Dict, Any
from httpx._client import AsyncClient

from app.logger import get_logger


log = get_logger(__name__)


class HTTPClient:
    async def get(
        self,
        *,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        try:
            async with AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                if response is None:
                    raise Exception(f"Could not get response from {url}")
                return response
        except Exception as e:
            log.error(e)
            return None

    async def post(
        self,
        *,
        url_service: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        try:
            async with AsyncClient() as client:
                response = await client.post(
                    url_service,
                    data=data,
                    headers=headers,
                )
                return response
        except Exception as e:
            log.error(e)
            return None
