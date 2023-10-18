"""Internal utilities."""


class SubAccessor:
    """A property-like object for both classes and class instances.

    This is required for sphinx autodoc to work correctly on subaccessors.
    """

    def __init__(self, accessor) -> None:
        self._accessor = accessor

    def __get__(self, obj, cls):
        if obj is None:
            return self._accessor

        return self._accessor(obj)
