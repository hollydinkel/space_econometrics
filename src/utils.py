from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import VECM

def adf_test(series, name):
    result = adfuller(series)
    # print('ADF Statistic:', result[0])
    # print('p-value:', result[1])
    if result[1] < 0.05:
        print(f'{name} is stationary')
    else:
        print(f'{name} is non-stationary')
    
def johansen_vecm(date_range, frame):
    # Perform Johansen cointegration test
    johansen_result = coint_johansen(frame, 0, 1)
    # print('Eigenvalues:', johansen_result.eig)
    # print('Trace Statistic:', johansen_result.lr1)
    # print('Critical Values:', johansen_result.cvt)

    # Determine the optimal lag length
    model = VAR(frame)
    lag_order = model.select_order()

    # Choose an available criterion, e.g., 'aic', 'bic', 'hqic'
    if 'aic' in lag_order.selected_orders:
        chosen_lag = lag_order.selected_orders['aic']
    elif 'bic' in lag_order.selected_orders:
        chosen_lag = lag_order.selected_orders['bic']
    elif 'hqic' in lag_order.selected_orders:
        chosen_lag = lag_order.selected_orders['hqic']
    else:
        raise ValueError("No valid criterion found in the selected orders.")

    print(f'Chosen lag length based on available criterion: {chosen_lag}')

    # coint_rank is number of non-zero eigenvalues minus 1
    vecm = VECM(frame, k_ar_diff=chosen_lag, coint_rank=1, dates=date_range)
    vecm_fit = vecm.fit()
    return vecm_fit