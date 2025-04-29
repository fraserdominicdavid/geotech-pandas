"""Common base class used throughout the geotech-pandas package."""

import pandas as pd


class GeotechPandasBase:
    """Base class with common validation methods for :external:class:`~pandas.DataFrame` objects."""

    def __init__(self, accessor) -> None:
        self._accessor = accessor
        self._obj: pd.DataFrame = accessor._obj

        self._validate_columns()
        self._validate_monotony()
        self._validate_duplicates()

    def _validate_columns(self, columns: list[str] | None = None) -> None:
        """
        Validate if the :external:class:`~pandas.DataFrame` contains the columns from a provided
        list.

        If the validation list is not provided, the method defaults to checking if the ``point_id``
        and ``bottom`` columns are present in the :external:class:`~pandas.DataFrame`. If any of the
        columns in the validation list are not found in the :external:class:`~pandas.DataFrame`, the
        method raises an ``AttributeError`` and lists the missing columns in the error message.

        Parameters
        ----------
        columns : list of str, optional, default ["point_id", "bottom"]
            List of column names to be validated.

        Raises
        ------
        AttributeError
            When any of the columns in the validation list are not found in the DataFrame.
        """  # noqa: D205
        if columns is None:
            columns = ["point_id", "bottom"]

        missing_columns = [column for column in columns if column not in self._obj.columns]

        if len(missing_columns) > 0:
            raise AttributeError(
                f"The DataFrame must have: {', '.join(missing_columns)} "
                f"column{'s' if len(missing_columns) > 1 else ''}."
            )

    def _validate_monotony(self) -> None:
        """
        Validate if the ``bottom`` of each ``point_id`` group is monotonically increasing.

        Raises
        ------
        AttributeError
            When ``bottom`` is not monotonically increasing in one or more ``point_id``.
        """
        g = self._obj.groupby("point_id")
        check_df = pd.Series(g["bottom"].is_monotonic_increasing).to_frame().reset_index()
        check_list = check_df[~check_df["bottom"]]["point_id"].to_list()
        if ~check_df["bottom"].all():
            raise AttributeError(
                f"Elements in the bottom column must be monotonically increasing for:"
                f" {', '.join(check_list)}."
            )

    def _validate_duplicates(self) -> None:
        """
        Validate the :external:class:`~pandas.DataFrame` for duplicate value pairs in the
        ``point_id`` and ``bottom`` columns.

        Raises
        ------
        AttributeError
            When duplicate value pairs in the ``point_id`` and ``bottom`` columns are detected.
        """  # noqa: D205
        duplicate_list = self._obj[self._obj[["point_id", "bottom"]].duplicated()][
            "point_id"
        ].to_list()
        if len(duplicate_list) > 0:
            raise AttributeError(
                "The DataFrame contains duplicate point_id and bottom:"
                f" {', '.join(duplicate_list)}."
            )

    def _validate_column_values(self, column: str, valid_values: list) -> None:
        """Validate that all non-NA values in a column are within the valid list of values.

        Parameters
        ----------
        column : str
            The name of the column to validate.
        valid_values : list
            A list of valid values for the column.

        Raises
        ------
        ValueError
            If any value in the column is not in the valid list of values.
        """
        validation_mask = self._obj[column].dropna().isin(valid_values)
        if not validation_mask.all():
            invalid_values = self._obj[column].dropna()[~validation_mask].unique().tolist()
            raise ValueError(
                f"Invalid value{'s' if len(invalid_values) > 1 else ''} found in '{column}': "
                f"{invalid_values}. Valid value{'s are' if len(valid_values) > 1 else ' is'}: "
                f"{valid_values}"
            )
