from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.ardl import ARDL, ardl_select_order

def adfTest(series, dtype):
    result = adfuller(series)
    # print(dtype, ": ADF Statistic = ", result[0], ", p-value = ", result[1])
    if result[1] < 0.05:
        return True
    else:
        return False
    
def getStationaryVariables(transformedData):
    stationaryVars = []
    nonstationaryVars = []
    errorList = []
    for idx, dtype in enumerate(transformedData):
        try:
            stationarity = adfTest(transformedData[dtype], dtype)
            if stationarity:
                stationaryVars.append(dtype)
            else:
                nonstationaryVars.append(dtype)
        except:
            errorList.append(dtype)
    # print("Stationary variables: ", stationaryVars)
    # print("Nonstationary variables: ", nonstationaryVars)
    # print("Error testing for stationarity: ", errorList)
    return stationaryVars, nonstationaryVars, errorList

def ardl_model(y, X, max_lags):
    """
    Fit an ARDL model to the data.
    
    Parameters:
    - date_range: pd.DatetimeIndex or list of dates
    - frame: pd.DataFrame containing the time series data
    - dependent_var: str, name of the dependent variable
    - independent_vars: list of str, names of independent variables
    - max_lags: int, maximum number of lags to consider for the ARDL model
    
    Returns:
    - ARDL model fit object
    """
    # Decrement endogenous max_lags until ardl_select_order works
    while max_lags > 0:
        try:
            ardl_order_selection = ardl_select_order(y, maxlag=max_lags, exog=X, maxorder=max_lags)
            print(f"Optimal lags with max_lags={max_lags}.")
            break
        except Exception as e:
            # print(f"Error with max_lags={max_lags}: {e}")
            max_lags -= 1

    # Fit the ARDL model
    ardl = ARDL(endog=y, lags=max_lags, exog=X)
    ardl_fit = ardl.fit()

    print(ardl_fit.summary())

    return ardl_fit
