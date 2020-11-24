
import pandas as pd
import numpy as np

def DCF_valuation_method(BS, IS, CF, shares_out, g_perp, market_cap, beta, ret_des, margin_saf, interest_expense, own=True):
    CF_OA = CF['Cash from Operating Activities']
    CAPEX = CF['Change in Fixed Assets & Intangibles']
    REVENUE = IS['Revenue']
    NET_INCOME = CF['Net Income/Starting Line']
    
    # Create DataFrame
    data = {'Cash Flow from OA':CF_OA, 'CAPEX': CAPEX, 'FCF to Equity': CF_OA+CAPEX, 'Net Income': NET_INCOME, \
        'Net Income margin': NET_INCOME/REVENUE, 'Revenue':REVENUE}
    df = pd.DataFrame(data)
    
    # Define Growth rate
    df['Growth Rate'] = df['Revenue'].pct_change(1)
    
    # FORECASTING for the next 10 years
    # FCF/Net Income
    coef_FCF_NET_Inco = df['FCF to Equity']/df['Net Income']

    for year in range(1,11):
         l = len(df['Growth Rate'])
         if df['Growth Rate'][l-1] < 0 and year ==1:
             min_g = df['Growth Rate'].abs().min()
             rev_est = df['Revenue'][l-1]*(1+min_g)
             net_inc_est = df['Revenue'][l-1]*df['Net Income margin'].mean()
             fcf_est = net_inc_est*coef_FCF_NET_Inco.min()
             row = pd.Series(data = {'FCF to Equity': fcf_est, 'Net Income': net_inc_est, 'Revenue': rev_est, 'Growth Rate': min_g}, name ='Est '+str(year))
             df = df.append(row)                
         else: 
             gr_est = df['Growth Rate'][l-1]*(1 + df['Growth Rate'].mean())
             rev_est = df['Revenue'][l-1]*(1+gr_est)
             net_inc_est = df['Revenue'][l-1]*df['Net Income margin'].mean()
             fcf_est = net_inc_est*coef_FCF_NET_Inco.min()
             row = pd.Series(data = {'FCF to Equity': fcf_est, 'Net Income': net_inc_est, 'Revenue': rev_est, 'Growth Rate': gr_est}, name ='Est '+str(year))
             df = df.append(row)
    
    
    # Debt rate rd
    # interest_expense to define # np.abs(nvdaIS['Income Tax (Expense) Benefit, net'][-1])
    debt = BS['Total Liabilities'][-1]
    rd = interest_expense/debt

    # Tax rate t
    income_tax_exp = np.abs(IS['Income Tax (Expense) Benefit, net'][-1])
    income_bef_tax = IS['Pretax Income (Loss)'][-1]
    t = income_tax_exp/income_bef_tax

    # CAPM for re
    Rf = 0.23
    Rm = 0.10
    re = Rf - beta*(Rm - Rf)

    # Weights
    Wd = debt/(market_cap+debt)
    We = market_cap/(market_cap+debt)

    # WACC model r_wacc = Wd*rd*(1-t) + We*re
    r_wacc = Wd*rd*(1-t) + We*re
    
    
    # Terminal Value
    FCF_n = df['FCF to Equity'][-1]
    V0 = FCF_n*(1 + g_perp)/(r_wacc-g_perp)

    #  Discount factor
    if own:
        DF = 1 + ret_des
    else:
        DF = 1+ r_wacc
    

    # Fair value of equity
    today_value = 0
    for year in range(1,11):
         today_value = today_value + df.loc['Est '+str(year)]['FCF to Equity']/DF**year
    
    today_value = today_value + V0
    fair_value = today_value/shares_out
    buy_price = fair_value*margin_saf
    return fair_value, buy_price