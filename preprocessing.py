import pandas as pd

def excel_to_df(excel):
    # Read the excel file
    data = pd.read_excel(excel)
    
    # fill with Zeros all NaN
    data.fillna(value=0, inplace=True)
    
    # Define indexes
    IS_index = data[data['Data provided by SimFin'] == 'Profit & Loss statement'].index.values.astype(int)[0]
    BS_index = data[data['Data provided by SimFin'] == 'Balance Sheet'].index.values.astype(int)[0]
    CF_index = data[data['Data provided by SimFin'] == 'Cash Flow statement'].index.values.astype(int)[0]
    
    #Income Statement
    IS_data = data.iloc[IS_index+1:BS_index-1]
    IS_data.set_index(['Unnamed: 1'], inplace=True)
    IS_data.columns = IS_data.iloc[0]

    IS_data.drop([IS_data.columns[0]], axis=1, inplace = True)
    IS_data.drop(['in million USD'], inplace=True)
    IS_data.index.name='Year'
    #Balance Sheet
    BS_data = data.iloc[BS_index+1: CF_index-1]
    BS_data.set_index(['Unnamed: 1'], inplace=True)
    BS_data.columns = BS_data.iloc[0]

    BS_data.drop([BS_data.columns[0]], axis=1, inplace = True)
    BS_data.drop(['in million USD'], inplace=True)
    BS_data.index.name='Year'
    #Cash Flow
    CF_data = data.iloc[CF_index+1:]
    CF_data.set_index(['Unnamed: 1'], inplace=True)
    CF_data.columns = CF_data.iloc[0]
    CF_data.drop([CF_data.columns[0]], axis=1, inplace = True)
    CF_data.drop(['in million USD'], inplace=True)
    CF_data.index.name='Year'	
	
    return IS_data.T, BS_data.T, CF_data.T