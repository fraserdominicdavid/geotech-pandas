"""A module containing a common class used throughout the geotech-pandas package."""

import pandas as pd


class GeotechPandasBase:
    """A base class with common validation methods for dataframes."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._obj = df

    @staticmethod
    def validate_columns(df: pd.DataFrame, columns: list[str] | None = None) -> None:
        """
        Validate the dataframe if it contains the columns from a provided list.

        The `validate_columns` method is a static method that is used to validate the columns of a
        given dataframe. The method takes in a dataframe and a list of columns to be validated. If
        the validation list is not provided, the method defaults to checking if the ``PointID`` and
        ``Bottom`` columns are present in the dataframe. If any of the columns in the validation
        list are not found in the dataframe, the method raises an `AttributeError` and lists the
        missing columns in the error message.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe to be validated.
        columns : list of str, optional, default ["PointID", "Bottom"]
            List of column names to be validated.

        Raises
        ------
        AttributeError
            When any of the columns in the validation list are not found in the dataframe.
        """
        if columns is None:
            columns = ["PointID", "Bottom"]

        missing_columns = []
        for column in columns:
            if column not in df.columns:
                missing_columns.append(column)

        if len(missing_columns) > 0:
            raise AttributeError(
                f"The dataframe must have: {', '.join(missing_columns)} "
                f"column{'s' if len(missing_columns) > 1 else ''}."
            )
