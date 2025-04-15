"""General helper methods."""

import pandas as pd
import statsmodels.api as sm


def _get_linear_forecast(
    group: pd.DataFrame,
    x_col_name: str,
    y_col_name: str,
    x_target: float | int,
) -> float:
    """Return a linear regression forecast for a given target value.

    This method fits a linear regression model to the provided data and predicts the target value
    based on the input target.

    Parameters
    ----------
    group : pd.DataFrame
        The DataFrame group containing the data for the regression.
    x_col_name : str
        The name of the column in the DataFrame to be used as the independent variable.
    y_col_name : str
        The name of the column in the DataFrame to be used as the dependent variable.
    x_target : float or int
        The target value for which the forecast is to be made.

    Returns
    -------
    float
        The predicted value based on the linear regression model.

    Notes
    -----
    This method uses the statsmodels library to perform the linear regression. It drops any rows
    with NaN values in the specified columns before fitting the model.

    Examples
    --------
    >>> df = pd.DataFrame(
    ...     {
    ...         "x": [1, 2, 3, 4],
    ...         "y": [2, 3, 5, 6],
    ...     }
    ... )
    >>> _get_linear_forecast(df, "x", "y", 5)
    np.float64(7.499999999999997)
    """
    group = group.dropna(subset=[x_col_name, y_col_name])
    x = group[x_col_name].astype(float)
    y = group[y_col_name].astype(float)
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    target = [1, x_target]
    forecast = model.predict(target)

    return forecast[0]
