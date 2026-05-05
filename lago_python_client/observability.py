"""
Optional observability helpers for Lago rate limits.

Provides ready-to-use ``on_rate_limit_info`` callbacks so callers can opt into
rate limit observability without writing one themselves.

Example:
    from lago_python_client import Client
    from lago_python_client.observability import LoggingRateLimitObserver

    client = Client(
        api_key="...",
        on_rate_limit_info=LoggingRateLimitObserver(),
    )
"""

import logging
from typing import Optional, Sequence

from .services.rate_limit import RateLimitInfo

DEFAULT_THRESHOLDS: Sequence[float] = (0.80, 0.90, 0.95)


class LoggingRateLimitObserver:
    """
    Emits a log line each time rate limit usage crosses a configured threshold.

    Stateless across calls: every response that lands above any threshold logs.
    If you want one-shot crossings, wrap it with your own state.

    Args:
        thresholds: Usage fractions (0.0 - 1.0) that should produce a log line.
            Defaults to 80%, 90%, 95%.
        logger: Logger to emit on. Defaults to ``lago_python_client.rate_limit``.
        level: Log level used when a threshold is crossed. Defaults to WARNING.
    """

    def __init__(
        self,
        thresholds: Sequence[float] = DEFAULT_THRESHOLDS,
        logger: Optional[logging.Logger] = None,
        level: int = logging.WARNING,
    ) -> None:
        # Sort descending so we report the highest matching threshold first.
        self.thresholds = tuple(sorted(thresholds, reverse=True))
        self.logger = logger or logging.getLogger("lago_python_client.rate_limit")
        self.level = level

    def __call__(self, info: RateLimitInfo) -> None:
        pct = info.usage_pct
        if pct is None:
            return

        for threshold in self.thresholds:
            if pct >= threshold:
                self.logger.log(
                    self.level,
                    "Lago rate limit at %.0f%% (limit=%s, remaining=%s, reset=%ss, %s %s)",
                    pct * 100,
                    info.limit,
                    info.remaining,
                    info.reset,
                    info.method,
                    info.url,
                )
                return
