# Finance
Tools for analyzing financial statements.

## Preprocessing
A preprocessing file that converts the downloaded .xlsx files (BS, IS and CF) in the good format for processing.

## Valuation Methods: DCF
Discounted Cash Flow methodology for analyzing a company intrinsic value.
''' def DCF_valuation_method(BS, IS, CF, shares_out, g_perp, market_cap, beta, ret_des, interest_expense, own=True) '''
It takes as INPUTS:
- BS: balance sheet
- IS: income statement
- CF: cash flow
- shares_out: shares outstanding
- g_perp: perpetual growth of general market
- market_cap: market capitalization
- beta: market dependency beta
- ret_des: desired return rate
- interest_expense of the company

## Company class
A company class that uses an existing API for the yahoo finance to gather informations and make analysis.

