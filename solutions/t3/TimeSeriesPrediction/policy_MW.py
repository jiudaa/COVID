import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

def diff(col):
    colout = np.zeros(len(col))
    col = col.to_numpy()
    for i in range(len(col)-1):
        temp = col[i+1]-col[i]
        colout[i] = temp
    return colout

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def policy_MW(data):
    # data = pd.read_csv('../covid-policy-tracker/data/OxCGRT_latest.csv',low_memory=False)
    # Preview the first 5 lines of the loaded data
    Germany = data[data['CountryName']=='Malawi']
    colomn = Germany['ConfirmedCases']# ConfirmedDeaths
    colout = diff(colomn)
    colout = moving_average(colout,7)
    figure(figsize=(16, 8), dpi=80)
    plt.plot(colout)

    schoolc = Germany['C1_School closing']
    schoolc_diff = diff(schoolc)
    restrict = schoolc_diff > 0
    x = np.argwhere(restrict)
    up = 1000
    down = 0
    plt.vlines(x,down,up,colors='k')

    loos = schoolc_diff < 0
    x = np.argwhere(loos)
    plt.vlines(x,down,up,colors='k',linestyles = 'dashed')

    schoolc = Germany['C2_Workplace closing']
    schoolc_diff = diff(schoolc)
    restrict = schoolc_diff > 0
    x = np.argwhere(restrict)
    plt.vlines(x,down,up,colors='r')

    loos = schoolc_diff < 0
    x = np.argwhere(loos)
    plt.vlines(x,down,up,colors='r',linestyles = 'dashed')
    plt.legend(['Confirmed cases per day', 'School closing', 'Relax School closing', 'Workplace closing', 'Relax Workplace closing'])
    plt.title('Malawi')
    plt.xlabel('Day', fontsize=14)
    plt.ylabel('Confirmed Cases per day', fontsize=14)
    plt.savefig('Malawi_SchoolWorkplacePolicies', dpi=80)
    # plt.show()