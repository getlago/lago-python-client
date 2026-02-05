class _UnsetType:
    """Singleton representing an unset value."""

    def __repr__(self):
        return "<UNSET>"


UNSET = _UnsetType()
