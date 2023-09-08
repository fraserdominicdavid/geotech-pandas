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

    @staticmethod
    def validate_monotony(df: pd.DataFrame) -> None:
        """
        Validate if the ``Bottom`` of each ``PointID`` group is monotonically increasing.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe to be validated.

        Raises
        ------
        AttributeError
            When ``Bottom`` is not monotonically increasing in one or more ``PointID``.
        """
        g = df.groupby("PointID")
        check_df = pd.Series(g["Bottom"].is_monotonic_increasing).to_frame().reset_index()
        check_list = check_df[~check_df["Bottom"]]["PointID"].to_list()
        if ~check_df["Bottom"].all():
            raise AttributeError(
                f"Elements in the Bottom column must be monotonically increasing for:"
                f" {', '.join(check_list)}."
            )

    @staticmethod
    def validate_duplicates(df: pd.DataFrame) -> None:
        """
        Validate the dataframe for duplicate value pairs in the ``PointID`` and ``Bottom`` columns.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe to be validated.

        Raises
        ------
        AttributeError
            When duplicate value pairs in the ``PointID`` and ``Bottom`` columns are detected.
        """
        duplicate_list = df[df[["PointID", "Bottom"]].duplicated()]["PointID"].to_list()
        if len(duplicate_list) > 0:
            raise AttributeError(
                "The dataframe contains duplicate PointID and Bottom:"
                f" {', '.join(duplicate_list)}."
            )
