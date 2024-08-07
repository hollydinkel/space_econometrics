from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import VECM, select_order

def adfTest(series):
    result = adfuller(series)
    # print('ADF Statistic:', result[0])
    # print('p-value:', result[1])
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
    # print("Error in testing for stationarity, ", f"{dtype}: ", transformedData[dtype])
    # print("Stationary variables: ", stationaryVars)
    # print("Nonstationary variables: ", nonstationaryVars)
    # print("Error testing for stationarity: ", errorList)
    return stationaryVars, nonstationaryVars, errorList
    
def johansenVECM(dateRange, frame):
    # Perform Johansen cointegration test
    johansenResult = coint_johansen(frame, 0, 1)
    countZeros = sum([1 for x in johansenResult.eig if x == 0])
    rank = len(johansenResult.eig) - countZeros - 1
    # print('Trace Statistic:', johansen_result.lr1)
    # print('Critical Values:', johansen_result.cvt)

    # Determine the optimal lag length
    lagOrder = select_order(frame, maxlags=5)

    # Choose an available criterion, e.g., 'aic', 'bic', 'hqic'
    if 'aic' in lagOrder.selected_orders:
        chosenLag = lagOrder.selected_orders['aic']
    elif 'bic' in lagOrder.selected_orders:
        chosenLag = lagOrder.selected_orders['bic']
    elif 'hqic' in lagOrder.selected_orders:
        chosenLag = lagOrder.selected_orders['hqic']
    else:
        raise ValueError("No valid criterion found in the selected orders.")

    print(f'Chosen lag length based on available criterion: {chosenLag}')

    # coint_rank is number of non-zero eigenvalues minus 1
    vecm = VECM(frame, k_ar_diff=chosenLag, coint_rank=rank, dates=dateRange)
    VECMfit = vecm.fit()
    return VECMfit