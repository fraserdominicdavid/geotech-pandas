"""Test if accessors are registered with their namespaces as expected."""

from functools import reduce

import pandas as pd
import pytest

import geotech_pandas  # noqa: F401
from geotech_pandas.accessor import GeotechDataFrameAccessor
from geotech_pandas.in_situ.in_situ import InSituDataFrameAccessor
from geotech_pandas.lab.lab import LabDataFrameAccessor
from geotech_pandas.layer import LayerDataFrameAccessor
from geotech_pandas.point import PointDataFrameAccessor


@pytest.fixture
def df():
    """Return default ``DataFrame`` for testing."""
    return pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
        }
    )


@pytest.mark.parametrize(
    ("namespaces", "accessor"),
    [
        (["geotech"], GeotechDataFrameAccessor),
        (["geotech", "in_situ"], InSituDataFrameAccessor),
        (["geotech", "lab"], LabDataFrameAccessor),
        (["geotech", "layer"], LayerDataFrameAccessor),
        (["geotech", "point"], PointDataFrameAccessor),
    ],
)
def test_dataframe_accessor(df, namespaces, accessor):
    """Test if the last element of ``namespace`` is a registered ``accessor`` in ``df``.

    The ``namespace`` list is reduced. This means that providing a list of ``["a", "b"]`` would mean
    that the attribute ``a`` would first be obtained from ``df``, then the attribute ``b`` would be
    obtained from ``a``. Where ``b`` would then be checked if it is an instance of ``accessor``.

    Parameters
    ----------
    df : DataFrame
        DataFrame checked for registered accessors.
    namespaces : list of str
        Namespaces or attributes to be reduced, with the last element checked for the equivalent
        accessor.
    accessor : class
        Equivalent accessor class of the given namespace.
    """
    assert isinstance(reduce(getattr, namespaces, df), accessor)
