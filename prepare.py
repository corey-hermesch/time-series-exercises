# IMPORTS
import pandas as pd
import acquire as a

# defining a function to acquire and prepare ts_superstore dataframe
def get_superstore_df(filename='ts_superstore.csv'):
    """
    This function will
    - accept a file name of a csv stored locally, default is ts_superstore.csv
    - read the csv into a dataframe
    - convert the sales_date column to a datetime datatype
    - set sales_date as the index and sort the index
    - remove three repeated columns ('store', 'item', 'item_upc12')
    - add three columns: 
        - 'month' in format 'January'
        - 'day' in format 'Monday'
        - 'sales_total' which is sale_amount (total_items) * item_price
    - reorder the dataframe columns
    - return the prepared df
    """
    
    # read in dataframe from csv
    df = pd.read_csv(filename, index_col=0)
    
    # format sale_date and change it from a string to a datetime
    df.sale_date = df.sale_date.str.replace(' 00:00:00 GMT', '')
    # using this code and sending in the format argument made it run a LOT faster
    df.sale_date = pd.to_datetime(df.sale_date, format= '%a, %d %b %Y')
    df = df.set_index('sale_date')
    df = df.sort_index()
    
    # drop item, store, item_upc12 and keep item_id, store_id, item_upc14
    df = df.drop(columns=['item', 'store', 'item_upc12'])
    
    # add 3 columns for exploration
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    
    # reorder columns
    cols = ['sale_amount', 'item_price', 'sales_total', 'month', 'day_of_week', 'item_id'
            , 'store_id', 'sale_id', 'item_name', 'item_brand', 'item_upc14'
            , 'store_address', 'store_city', 'store_state', 'store_zipcode']
    df = df[cols]
    
    return df

# defining a function to prepare german power data
def prepare_german_df(df):
    """
    This function will
    - accept a dataframe from get_german_power_df()
    - rename columns
    - fill nulls in wind and solar with 0
    - recalculate wind_and_solar column because it wasn't right
    - change date column to datetime64 data type, set it as the index, and sort index
    - add two columns:
        - 'month' in form 'January'
        - 'year' in form 2006
    """
    
    # lower case and rename columns
    df.columns = df.columns.str.lower()
    df = df.rename(columns={'wind+solar': 'wind_and_solar'})
    
    # filling nulls in wind and solar to be 0 & recalculating wind_and_solar
    df.wind = df.wind.fillna(0)
    df.solar = df.solar.fillna(0)
    df.wind_and_solar = df.wind + df.solar
    
    # make pandas time aware
    df.date = df.date.astype('datetime64')
    df = df.set_index('date')
    df = df.sort_index()
    
    # adding month and year columns
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    
    return df

# defining a function to wrangle german_power_df
def wrangle_german_power_df(filename='opsd_germany_daily.csv'):
    """
    This function will
    - call get_german_power_df to acquire the data
    - call prepare_german_df to prepare it
    - return prepared df
    """
    
    df = a.get_german_power_df(filename)
    df = prepare_german_df(df)
    
    return df