import asyncio
from fastapi import FastAPI

from app.schemas.exchange import ExchangeResult, ExchangeOutput
from app.services.exchange import exchange_service


# SERVICE TEST
def test_exchange_rates(event_loop: asyncio.AbstractEventLoop):
    # Getting results from resources
    official_results = event_loop.run_until_complete(
        exchange_service.get_official_data()
    )
    fixer_results = event_loop.run_until_complete(
        exchange_service.get_data_from_fixer()
    )
    banxico_results = event_loop.run_until_complete(
        exchange_service.get_data_from_banxico()
    )

    rate_results = [official_results, fixer_results, banxico_results]

    try:
        # Make use of pydantic model validations for results
        for rate in rate_results:
            assert ExchangeResult(**rate.dict())
    except Exception:
        assert False


# ENDPOINT TEST
def test_exchange_endpoint(test_app: FastAPI):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJpZFwiOiA0NCwgXCJ1c2VybmFtZVwiOiBcImd1ZXN0XCIsIFwicmF0ZV9saW1pdFwiOiAwfSJ9.0qKPAfgj0oK8Z-d_ezvJ2jbwUEdq4vn1BiTufbcX4_0"
    response = test_app.get(
        "/api/exchange", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    rates = response.json()
    print(rates)
    assert ExchangeOutput(**rates)
    for rate in rates["rates"].values():
        assert ExchangeResult(**rate)
