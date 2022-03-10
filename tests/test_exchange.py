import asyncio
from app.schemas.exchange import ExchangeResult
from app.services.exchange import exchange_service


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
            ExchangeResult(**rate.dict())
        assert True
    except Exception:
        assert False


# def test_exchange_endpoint(test_app):
#     assert True
