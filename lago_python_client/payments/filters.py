from collections.abc import Mapping

from ..services.request import QueryPairs

PAYMENT_ARRAY_FILTERS = {
    "payment_status",
    "payment_statuses",
    "payment_provider_type",
    "payment_method_type",
    "payment_type",
    "payable_type",
}


def payment_filter_options(options: QueryPairs = None) -> QueryPairs:
    """Encode payment arrays with Rails brackets without mutating the caller's options."""
    pairs = options.items() if isinstance(options, Mapping) else options or []
    result = []
    for key, value in pairs:
        if isinstance(value, (list, tuple)):
            name = f"{key}[]" if key in PAYMENT_ARRAY_FILTERS else key
            result.extend((name, item) for item in value)
        else:
            result.append((key, value))
    return result
