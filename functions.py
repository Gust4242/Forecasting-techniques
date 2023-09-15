import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from functools import reduce
from bizdays import Calendar

CAL = Calendar.load("ANBIMA")

def forecast_comparisson(df, product_col='Product', real_sales_col='Real_sales', forecast_col='Forecast'):

    """
    Plot a comparison between forecasted sales and real sales for each product.

    Parameters:
    -----------
    df : DataFrame
        The input DataFrame with the forecasted sales series and the actual sales series for each product.
    product_col : str, optional (default='Product')
        Name of the column in `df` with the product identifier.
    real_sales_col : str, optional (default='Real_sales')
        Name of the column in `df` with the actual sales values.
    forecast_col : str, optional (default='Forecast')
        Name of the column in `df` with the forecasted sales values.

    Returns:
    Plotly Figure: Plotly Figure with the forecasted sales and the real sales for each product
    """
    fig = go.Figure()
    df_grouped = df.groupby(product_col)[[real_sales_col, forecast_col]].sum().reset_index()
    fig.add_trace(go.Bar(x=df_grouped[product_col], y=df_grouped[real_sales_col], name='Vendas Reais'))
    fig.add_trace(go.Bar(x=df_grouped[product_col], y=df_grouped[forecast_col], name='Vendas Previstas'))
    fig.update_layout(barmode='group', xaxis_title='Product', yaxis_title='Sales')
    return fig.show()

def extract_date_features(df, date_column='date'):
    """
    Extracts features of a date column in a dataframe.

    Parameters:
    -----------
    df (pandas.DataFrame): The dataframe containing the date column.
    date_column (str): The name of the date column in the dataframe.

    Returns:
    pandas.DataFrame
    """

    # Convert the date column to a pandas datetime object
    
    df[date_column] = pd.to_datetime(df[date_column])
    df["year"]= df[date_column].dt.year
    df['month']= df[date_column].dt.month
    df['day']= df[date_column].dt.day
    df['day_of_week']= df[date_column].dt.dayofweek
    df['day_of_year']= df[date_column].dt.dayofyear
    df['week_of_year']= df[date_column].dt.isocalendar().week
    df['quarter']= df[date_column].dt.quarter
    df['is_leap_year']= df[date_column].dt.is_leap_year # year with 366 days
    df['is_month_start']= df[date_column].dt.is_month_start
    df['is_month_end']= df[date_column].dt.is_month_end
    df['is_holiday'] = np.where(df[date_column].isin(CAL.holidays),True,False)
    df['is_bizdays'] = df[date_column].apply(lambda x: CAL.isbizday(x))

    return df

def add_lags(df, lags=[1], date_column='Date', target_col='Amount', fillna=0):
    """
    Add lags to a dataframe.

    Parameters:
    -----------
    df (pandas.DataFrame): The dataframe containing the data.
    lags (list of int): Number of days the serie will be lagged
    date_column (str): Name of the column containing the date
    target_col (str): Name of the column with the values to be lagged
    fillna (int): Value to fill the NaNs

    Returns:
    pandas.DataFrame
    """
    df_lagged = df.copy()
    df_lagged = df_lagged.sort_values('Date')
    for i in lags:
        if i > 0:
            col_name = target_col + '_lag' + '_' + str(i)
        else:
            pass
        df_lagged[col_name] = df_lagged.groupby(date_column)[target_col].shift(i)
        df_lagged[col_name].fillna(fillna, inplace=True)
    return df_lagged