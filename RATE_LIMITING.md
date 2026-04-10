# Rate Limiting Support in Lago Python Client

## Overview

The Lago Python client now includes built-in support for HTTP 429 (Too Many Requests) responses from the Lago API. This implementation provides automatic retry capabilities with exponential backoff when rate limits are exceeded.

## Features

### 1. Rate Limit Headers Parsing

When the API returns a 429 response, it includes rate limit information in response headers:
- `x-ratelimit-limit`: Maximum number of requests allowed in the current window
- `x-ratelimit-remaining`: Number of requests remaining in the current window
- `x-ratelimit-reset`: Number of seconds until the rate limit window resets

The client automatically parses these headers and exposes them through the `LagoRateLimitError` exception.

### 2. LagoRateLimitError Exception

A new exception class `LagoRateLimitError` (subclass of `LagoApiError`) is raised when the API returns a 429 response.

```python
from lago_python_client.exceptions import LagoRateLimitError

try:
    client.customers.find_all()
except LagoRateLimitError as e:
    print(f"Rate limit exceeded!")
    print(f"  Limit: {e.limit}")
    print(f"  Remaining: {e.remaining}")
    print(f"  Reset in: {e.reset} seconds")
```

### 3. Automatic Retry Configuration

Configure retry behavior when creating a client:

```python
from lago_python_client import Client

# Use default retry settings (max_retries=3, retry_on_rate_limit=True)
client = Client(api_key="your-api-key")

# Customize retry behavior
client = Client(
    api_key="your-api-key",
    max_retries=5,           # Maximum number of retry attempts
    retry_on_rate_limit=True # Enable/disable automatic retries
)
```

### 4. RateLimitRetryConfig

For advanced configuration, use `RateLimitRetryConfig` directly:

```python
from lago_python_client.services.rate_limit import RateLimitRetryConfig

config = RateLimitRetryConfig(
    max_retries=3,                    # Maximum retry attempts
    retry_on_rate_limit=True,         # Enable retries
    base_backoff_seconds=1.0,         # Initial backoff duration
    backoff_multiplier=2.0            # Exponential backoff multiplier
)

# The Client will use this config automatically for all API calls
```

## Retry Behavior

### Exponential Backoff Strategy

When a 429 response is received, the client uses two strategies:

1. **Server-provided reset time (preferred)**:
   - If the `x-ratelimit-reset` header is present, the client waits for the specified number of seconds before retrying.

2. **Exponential backoff (fallback)**:
   - If the reset header is missing, the client uses exponential backoff.
   - Wait duration = `base_backoff_seconds * (backoff_multiplier ^ retry_attempt)`
   - Default: 1s → 2s → 4s → ...

### Example Retry Sequence

With default settings (max_retries=3, base_backoff=1.0, multiplier=2.0):

```
Attempt 1: API request → 429 response
Wait: x-ratelimit-reset header (e.g., 60 seconds) OR 1 second

Attempt 2: API request → 429 response
Wait: x-ratelimit-reset header OR 2 seconds

Attempt 3: API request → 429 response
Wait: x-ratelimit-reset header OR 4 seconds

Attempt 4: API request → 429 response
Raise: LagoRateLimitError (max retries exhausted)
```

## Implementation Details

### Request Wrapper

The retry logic is implemented in `services/rate_limit.py` with a wrapper around httpx HTTP methods. The wrapper:

1. Detects 429 responses
2. Calculates appropriate backoff duration
3. Waits and retries the request
4. Raises `LagoRateLimitError` when max retries are exhausted

### Integration Points

**exceptions.py**:
- New `LagoRateLimitError` class with header parsing

**services/rate_limit.py**:
- `RateLimitRetryConfig`: Configuration class
- `handle_rate_limit_response()`: Retry logic
- `is_rate_limit_response()`: 429 detection
- `wait_for_retry()`: Sleep wrapper

**services/request.py**:
- Wrapper functions that integrate retry logic with httpx methods
- Transparent to existing client code

**services/response.py**:
- `verify_response()` now raises `LagoRateLimitError` for 429 responses

**client.py**:
- `Client.__init__()` accepts `max_retries` and `retry_on_rate_limit` parameters
- Propagates `rate_limit_retry_config` to all API client instances

**base_client.py**:
- Updated to store and pass through `rate_limit_retry_config`

## Disabling Rate Limit Retries

To disable automatic retries and immediately raise on 429:

```python
client = Client(
    api_key="your-api-key",
    retry_on_rate_limit=False
)
```

## Error Handling Examples

### Basic Exception Handling

```python
from lago_python_client import Client
from lago_python_client.exceptions import LagoRateLimitError

client = Client(api_key="your-api-key")

try:
    customers = client.customers.find_all()
except LagoRateLimitError as e:
    # Handle rate limit specifically
    print(f"Rate limited until {e.reset} seconds from now")
except Exception as e:
    # Handle other errors
    print(f"Error: {e}")
```

### Custom Retry Logic

If you need custom retry behavior, disable automatic retries and implement your own:

```python
from lago_python_client import Client
from lago_python_client.exceptions import LagoRateLimitError
import time

client = Client(
    api_key="your-api-key",
    retry_on_rate_limit=False  # Disable automatic retries
)

def fetch_with_custom_retry(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except LagoRateLimitError as e:
            if attempt < max_attempts - 1:
                wait_time = e.reset or (2 ** attempt)  # Use header or exponential backoff
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

# Usage
customers = fetch_with_custom_retry(
    lambda: client.customers.find_all()
)
```

## Testing

The implementation includes comprehensive tests in `tests/test_rate_limit.py`:

- `TestRateLimitError`: Tests for the exception class and header parsing
- `TestRateLimitRetryConfig`: Tests for configuration behavior
- `TestClientRateLimitConfig`: Tests for client integration
- `TestRateLimitResponses`: Tests for actual 429 response handling

To run the tests:

```bash
pytest tests/test_rate_limit.py -v
```

## Backwards Compatibility

This implementation is fully backwards compatible:

- Existing code without rate limit awareness works unchanged
- Default behavior (max_retries=3) is sensible for most use cases
- All existing exception handling still works (LagoRateLimitError is a subclass of LagoApiError)
- No breaking changes to public API

## Performance Considerations

- Retry logic is non-blocking and uses standard Python `time.sleep()`
- For async applications, consider wrapping sleep in an async context
- Server-provided reset times are preferred over exponential backoff for efficiency

## Future Enhancements

Potential improvements for future versions:

1. Async/await support for retry logic
2. Callback hooks for custom retry behavior
3. Metrics collection (retry attempts, wait times)
4. Circuit breaker pattern for persistent rate limiting
5. Per-endpoint rate limit tracking
