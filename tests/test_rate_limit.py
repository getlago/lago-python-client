import os
import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoRateLimitError, LagoApiError
from lago_python_client.services.rate_limit import RateLimitRetryConfig

ENDPOINT = "https://api.getlago.com/api/v1/api_logs"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


class TestRateLimitError:
    def test_rate_limit_error_parsing_headers(self):
        """Test that LagoRateLimitError correctly parses rate limit headers."""
        headers = {
            "x-ratelimit-limit": "100",
            "x-ratelimit-remaining": "0",
            "x-ratelimit-reset": "60",
        }

        error = LagoRateLimitError(
            status_code=429,
            url="https://api.example.com/test",
            response=None,
            headers=headers,
        )

        assert error.status_code == 429
        assert error.limit == 100
        assert error.remaining == 0
        assert error.reset == 60

    def test_rate_limit_error_missing_headers(self):
        """Test that LagoRateLimitError handles missing headers gracefully."""
        error = LagoRateLimitError(
            status_code=429,
            url="https://api.example.com/test",
            response=None,
            headers={"x-ratelimit-limit": "100"},
        )

        assert error.limit == 100
        assert error.remaining is None
        assert error.reset is None

    def test_rate_limit_error_no_headers(self):
        """Test that LagoRateLimitError works without headers."""
        error = LagoRateLimitError(
            status_code=429,
            url="https://api.example.com/test",
            response=None,
            headers=None,
        )

        assert error.status_code == 429
        assert error.limit is None
        assert error.remaining is None
        assert error.reset is None

    def test_rate_limit_error_invalid_header_values(self):
        """Test that LagoRateLimitError handles invalid header values gracefully."""
        headers = {
            "x-ratelimit-limit": "not-a-number",
            "x-ratelimit-remaining": "invalid",
            "x-ratelimit-reset": "also-invalid",
        }

        error = LagoRateLimitError(
            status_code=429,
            url="https://api.example.com/test",
            response=None,
            headers=headers,
        )

        # Should have None values for all, as parsing failed
        assert error.limit is None
        assert error.remaining is None
        assert error.reset is None

    def test_rate_limit_error_repr(self):
        """Test LagoRateLimitError string representation."""
        error = LagoRateLimitError(
            status_code=429,
            url="https://api.example.com/test",
            response=None,
            headers={
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "0",
                "x-ratelimit-reset": "60",
            },
        )

        repr_str = repr(error)
        assert "LagoRateLimitError" in repr_str
        assert "limit=100" in repr_str
        assert "remaining=0" in repr_str
        assert "reset=60" in repr_str


class TestRateLimitRetryConfig:
    def test_default_config(self):
        """Test default rate limit retry config."""
        config = RateLimitRetryConfig()

        assert config.max_retries == 3
        assert config.retry_on_rate_limit is True
        assert config.base_backoff_seconds == 1.0
        assert config.backoff_multiplier == 2.0

    def test_custom_config(self):
        """Test custom rate limit retry config."""
        config = RateLimitRetryConfig(
            max_retries=5,
            retry_on_rate_limit=False,
            base_backoff_seconds=2.0,
            backoff_multiplier=3.0,
        )

        assert config.max_retries == 5
        assert config.retry_on_rate_limit is False
        assert config.base_backoff_seconds == 2.0
        assert config.backoff_multiplier == 3.0

    def test_exponential_backoff_calculation(self):
        """Test exponential backoff duration calculation."""
        config = RateLimitRetryConfig(
            base_backoff_seconds=1.0,
            backoff_multiplier=2.0,
        )

        # First retry: 1 * 2^0 = 1
        assert config.calculate_backoff(0) == 1.0
        # Second retry: 1 * 2^1 = 2
        assert config.calculate_backoff(1) == 2.0
        # Third retry: 1 * 2^2 = 4
        assert config.calculate_backoff(2) == 4.0

    def test_custom_exponential_backoff(self):
        """Test custom exponential backoff calculation."""
        config = RateLimitRetryConfig(
            base_backoff_seconds=0.5,
            backoff_multiplier=3.0,
        )

        # 0.5 * 3^0 = 0.5
        assert config.calculate_backoff(0) == 0.5
        # 0.5 * 3^1 = 1.5
        assert config.calculate_backoff(1) == 1.5
        # 0.5 * 3^2 = 4.5
        assert config.calculate_backoff(2) == 4.5


class TestClientRateLimitConfig:
    def test_client_default_rate_limit_config(self):
        """Test that Client has default rate limit config."""
        client = Client(api_key="test-key")

        assert client.rate_limit_retry_config is not None
        assert client.rate_limit_retry_config.max_retries == 3
        assert client.rate_limit_retry_config.retry_on_rate_limit is True

    def test_client_custom_max_retries(self):
        """Test Client with custom max_retries."""
        client = Client(
            api_key="test-key",
            max_retries=5,
        )

        assert client.rate_limit_retry_config.max_retries == 5
        assert client.rate_limit_retry_config.retry_on_rate_limit is True

    def test_client_disable_rate_limit_retry(self):
        """Test Client with rate limit retry disabled."""
        client = Client(
            api_key="test-key",
            retry_on_rate_limit=False,
        )

        assert client.rate_limit_retry_config.retry_on_rate_limit is False
        assert client.rate_limit_retry_config.max_retries == 3

    def test_client_custom_retry_config(self):
        """Test Client with all custom retry settings."""
        client = Client(
            api_key="test-key",
            max_retries=10,
            retry_on_rate_limit=False,
        )

        assert client.rate_limit_retry_config.max_retries == 10
        assert client.rate_limit_retry_config.retry_on_rate_limit is False


class TestRateLimitResponses:
    def test_429_raises_rate_limit_error(self, httpx_mock: HTTPXMock, monkeypatch):
        """Test that 429 responses raise LagoRateLimitError."""
        # Patch sleep so retries don't actually wait
        monkeypatch.setattr("lago_python_client.services.rate_limit.time.sleep", lambda _: None)

        client = Client(api_key="test-key")
        request_id = "test-id"

        # Queue 4 responses (1 initial + 3 retries) so retries exhaust
        for _ in range(4):
            httpx_mock.add_response(
                method="GET",
                url=ENDPOINT + f"/{request_id}",
                status_code=429,
                headers={
                    "x-ratelimit-limit": "100",
                    "x-ratelimit-remaining": "0",
                    "x-ratelimit-reset": "1",
                },
            )

        with pytest.raises(LagoRateLimitError) as exc_info:
            client.api_logs.find(request_id)

        error = exc_info.value
        assert error.status_code == 429
        assert error.limit == 100
        assert error.remaining == 0
        assert error.reset == 1

    def test_retry_disabled_raises_immediately(self, httpx_mock: HTTPXMock):
        """Test that retry_on_rate_limit=False raises on first 429 without retrying."""
        client = Client(api_key="test-key", retry_on_rate_limit=False)
        request_id = "test-id"

        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=429,
            headers={
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "0",
                "x-ratelimit-reset": "60",
            },
        )

        with pytest.raises(LagoRateLimitError):
            client.api_logs.find(request_id)

        # Should have made exactly 1 request (no retries)
        assert len(httpx_mock.get_requests()) == 1

    def test_custom_max_retries_respected(self, httpx_mock: HTTPXMock, monkeypatch):
        """Test that custom max_retries is propagated and respected."""
        monkeypatch.setattr("lago_python_client.services.rate_limit.time.sleep", lambda _: None)

        client = Client(api_key="test-key", max_retries=1)
        request_id = "test-id"

        # Queue 2 responses: initial 429 + 1 retry 429 = exhausted
        for _ in range(2):
            httpx_mock.add_response(
                method="GET",
                url=ENDPOINT + f"/{request_id}",
                status_code=429,
                headers={"x-ratelimit-reset": "1"},
            )

        with pytest.raises(LagoRateLimitError):
            client.api_logs.find(request_id)

        # Should have made exactly 2 requests (initial + 1 retry)
        assert len(httpx_mock.get_requests()) == 2

    def test_retry_then_success(self, httpx_mock: HTTPXMock, monkeypatch):
        """Test that retry on 429 followed by 200 succeeds."""
        monkeypatch.setattr("lago_python_client.services.rate_limit.time.sleep", lambda _: None)

        client = Client(api_key="test-key")
        request_id = "test-id"

        # First request: 429, second: 200 with full fixture
        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=429,
            headers={"x-ratelimit-reset": "1"},
        )
        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=200,
            content=mock_response("fixtures/api_log.json"),
        )

        result = client.api_logs.find(request_id)
        assert result is not None
        assert len(httpx_mock.get_requests()) == 2

    def test_other_errors_raise_api_error_not_rate_limit(self, httpx_mock: HTTPXMock):
        """Test that non-429 errors raise LagoApiError, not LagoRateLimitError."""
        client = Client(api_key="test-key")
        request_id = "invalid"

        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=404,
            content=b"",
        )

        with pytest.raises(LagoApiError) as exc_info:
            client.api_logs.find(request_id)

        error = exc_info.value
        assert isinstance(error, LagoApiError)
        assert not isinstance(error, LagoRateLimitError)
