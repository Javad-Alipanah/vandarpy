import pytest
import threading
from tests.helpers import MockRequestStrategy
from vandarpy.client import VandarClient


@pytest.fixture(scope="session", autouse=True)
def close_timer_threads(request):
    def finalize():
        running_timer_threads = [thread for thread in threading.enumerate() if isinstance(thread, threading.Timer)]
        for timer in running_timer_threads:
            timer.cancel()

    request.addfinalizer(finalize)


@pytest.fixture(scope="session")
def client():
    mock_req_strategy = MockRequestStrategy()
    client = VandarClient(
        token="token",
        refresh_token="refresh_token",
        business_name="test"
    )
    client.set_request_strategy(mock_req_strategy)
    return client
