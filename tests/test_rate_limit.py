import logging
import os

import httpx
import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError, LagoRateLimitError
from lago_python_client.observability import LoggingRateLimitObserver
from lago_python_client.services.rate_limit import (
    RateLimitInfo,
    RateLimitRetryConfig,
    parse_rate_limit_info,
)

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


class TestRateLimitInfo:
    def test_usage_pct_basic(self):
        info = RateLimitInfo(
            limit=100,
            remaining=20,
            reset=30,
            url="u",
            method="GET",
        )
        assert info.usage_pct == pytest.approx(0.80)

    def test_usage_pct_full(self):
        info = RateLimitInfo(
            limit=100,
            remaining=0,
            reset=30,
            url="u",
            method="GET",
        )
        assert info.usage_pct == pytest.approx(1.0)

    def test_usage_pct_none_when_limit_missing(self):
        info = RateLimitInfo(
            limit=None,
            remaining=20,
            reset=30,
            url="u",
            method="GET",
        )
        assert info.usage_pct is None

    def test_usage_pct_none_when_remaining_missing(self):
        info = RateLimitInfo(
            limit=100,
            remaining=None,
            reset=30,
            url="u",
            method="GET",
        )
        assert info.usage_pct is None

    def test_usage_pct_none_when_limit_zero(self):
        info = RateLimitInfo(
            limit=0,
            remaining=0,
            reset=30,
            url="u",
            method="GET",
        )
        assert info.usage_pct is None


class TestParseRateLimitInfo:
    def _make_response(self, headers):
        class _R:
            def __init__(self, h):
                self.headers = h

        return _R(headers)

    def test_parse_full_headers(self):
        resp = self._make_response(
            {
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "42",
                "x-ratelimit-reset": "5",
            }
        )

        info = parse_rate_limit_info(resp, method="GET", url="https://x")

        assert info is not None
        assert info.limit == 100
        assert info.remaining == 42
        assert info.reset == 5
        assert info.method == "GET"
        assert info.url == "https://x"

    def test_parse_returns_none_when_headers_absent(self):
        resp = self._make_response({})
        assert parse_rate_limit_info(resp, method="GET", url="https://x") is None

    def test_parse_partial_headers(self):
        resp = self._make_response({"x-ratelimit-limit": "100"})

        info = parse_rate_limit_info(resp, method="GET", url="https://x")

        assert info is not None
        assert info.limit == 100
        assert info.remaining is None
        assert info.reset is None

    def test_parse_invalid_headers(self):
        resp = self._make_response(
            {
                "x-ratelimit-limit": "not-a-number",
                "x-ratelimit-remaining": "nope",
                "x-ratelimit-reset": "bad",
            }
        )

        # All fields fail to parse -> all None -> treated as no rate limit info
        assert parse_rate_limit_info(resp, method="GET", url="https://x") is None


class TestRateLimitInfoCallback:
    def test_callback_fires_on_success(self, httpx_mock: HTTPXMock):
        """Callback receives rate limit info after a 2xx response."""
        captured = []

        client = Client(api_key="test-key", on_rate_limit_info=captured.append)
        request_id = "test-id"

        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=200,
            headers={
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "20",
                "x-ratelimit-reset": "5",
            },
            content=mock_response("fixtures/api_log.json"),
        )

        client.api_logs.find(request_id)

        assert len(captured) == 1
        info = captured[0]
        assert info.limit == 100
        assert info.remaining == 20
        assert info.reset == 5
        assert info.usage_pct == pytest.approx(0.80)
        assert info.method == "GET"

    def test_callback_not_called_when_headers_absent(self, httpx_mock: HTTPXMock):
        """Self-hosted-style response with no rate limit headers must not call back."""
        captured = []

        client = Client(api_key="test-key", on_rate_limit_info=captured.append)
        request_id = "test-id"

        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=200,
            content=mock_response("fixtures/api_log.json"),
        )

        client.api_logs.find(request_id)

        assert captured == []

    def test_callback_exception_is_swallowed(self, httpx_mock: HTTPXMock, caplog):
        """A buggy callback must not break the request."""

        def boom(info):
            raise RuntimeError("intentional")

        client = Client(api_key="test-key", on_rate_limit_info=boom)
        request_id = "test-id"

        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=200,
            headers={
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "1",
                "x-ratelimit-reset": "5",
            },
            content=mock_response("fixtures/api_log.json"),
        )

        with caplog.at_level(logging.ERROR, logger="lago_python_client.services.rate_limit"):
            result = client.api_logs.find(request_id)

        assert result is not None
        assert any("on_rate_limit_info callback raised" in rec.message for rec in caplog.records)

    def test_callback_fires_only_once_after_429_retry_resolves(
        self,
        httpx_mock: HTTPXMock,
        monkeypatch,
    ):
        """After a 429 retry sequence resolves to 2xx, callback fires once for the success."""
        monkeypatch.setattr("lago_python_client.services.rate_limit.time.sleep", lambda _: None)

        captured = []
        client = Client(api_key="test-key", on_rate_limit_info=captured.append)
        request_id = "test-id"

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
            headers={
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "50",
                "x-ratelimit-reset": "5",
            },
            content=mock_response("fixtures/api_log.json"),
        )

        client.api_logs.find(request_id)

        assert len(captured) == 1
        assert captured[0].remaining == 50

    def test_callback_not_called_when_429_exhausts(
        self,
        httpx_mock: HTTPXMock,
        monkeypatch,
    ):
        """Exhausted 429 retries raise without ever invoking the success callback."""
        monkeypatch.setattr("lago_python_client.services.rate_limit.time.sleep", lambda _: None)

        captured = []
        client = Client(api_key="test-key", on_rate_limit_info=captured.append)
        request_id = "test-id"

        for _ in range(4):
            httpx_mock.add_response(
                method="GET",
                url=ENDPOINT + f"/{request_id}",
                status_code=429,
                headers={"x-ratelimit-reset": "1"},
            )

        with pytest.raises(LagoRateLimitError):
            client.api_logs.find(request_id)

        assert captured == []


class TestLoggingRateLimitObserver:
    def _info(self, *, limit, remaining):
        return RateLimitInfo(
            limit=limit,
            remaining=remaining,
            reset=10,
            url="https://x",
            method="GET",
        )

    def test_logs_above_threshold(self, caplog):
        observer = LoggingRateLimitObserver(thresholds=(0.80, 0.90, 0.95))

        with caplog.at_level(logging.WARNING, logger="lago_python_client.rate_limit"):
            observer(self._info(limit=100, remaining=4))  # 96% used

        assert any("96%" in rec.getMessage() for rec in caplog.records)

    def test_silent_below_threshold(self, caplog):
        observer = LoggingRateLimitObserver(thresholds=(0.80,))

        with caplog.at_level(logging.WARNING, logger="lago_python_client.rate_limit"):
            observer(self._info(limit=100, remaining=50))  # 50% used

        assert caplog.records == []

    def test_silent_when_usage_pct_unavailable(self, caplog):
        observer = LoggingRateLimitObserver()

        with caplog.at_level(logging.WARNING, logger="lago_python_client.rate_limit"):
            observer(self._info(limit=None, remaining=None))

        assert caplog.records == []


class TestNetworkRetryResiliency:
    def test_network_error_retries_and_exhausts(self, httpx_mock: HTTPXMock, monkeypatch):
        slept_durations = []
        monkeypatch.setattr("lago_python_client.services.request.time.sleep", slept_durations.append)

        client = Client(api_key="test-key")
        request_id = "test-id"

        # Queue 4 errors (1 initial + 3 retries) so it raises on exhaustion
        for _ in range(4):
            httpx_mock.add_exception(
                httpx.ConnectError("Connection refused"),
                method="GET",
                url=ENDPOINT + f"/{request_id}",
            )

        with pytest.raises(httpx.ConnectError):
            client.api_logs.find(request_id)

        # 4 attempts total = 1 initial + 3 retries
        assert len(httpx_mock.get_requests()) == 4
        assert slept_durations == [1.0, 2.0, 4.0]

    def test_network_error_recovers(self, httpx_mock: HTTPXMock, monkeypatch):
        slept_durations = []
        monkeypatch.setattr("lago_python_client.services.request.time.sleep", slept_durations.append)

        client = Client(api_key="test-key")
        request_id = "test-id"

        # 2 failures followed by 1 success
        httpx_mock.add_exception(
            httpx.ConnectError("Connection failed"),
            method="GET",
            url=ENDPOINT + f"/{request_id}",
        )
        httpx_mock.add_exception(
            httpx.ConnectError("Connection failed again"),
            method="GET",
            url=ENDPOINT + f"/{request_id}",
        )
        httpx_mock.add_response(
            method="GET",
            url=ENDPOINT + f"/{request_id}",
            status_code=200,
            content=mock_response("fixtures/api_log.json"),
        )

        result = client.api_logs.find(request_id)
        assert result is not None
        assert len(httpx_mock.get_requests()) == 3
        assert slept_durations == [1.0, 2.0]

    def test_server_error_502_503_504_retries_and_exhausts(self, httpx_mock: HTTPXMock, monkeypatch):
        slept_durations = []
        monkeypatch.setattr("lago_python_client.services.request.time.sleep", slept_durations.append)

        client = Client(api_key="test-key")
        request_id = "test-id"

        # Queue 4 server error responses
        for status_code in [502, 503, 504, 502]:
            httpx_mock.add_response(
                method="GET",
                url=ENDPOINT + f"/{request_id}",
                status_code=status_code,
            )

        with pytest.raises(httpx.HTTPStatusError):
            client.api_logs.find(request_id)

        assert len(httpx_mock.get_requests()) == 4
        assert slept_durations == [1.0, 2.0, 4.0]
