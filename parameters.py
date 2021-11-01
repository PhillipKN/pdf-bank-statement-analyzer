
"""Like me, do you always wonder where your money goes each month
 and would like to get some insights into your spending? Here's how.
 Using Python, you can go from a PDF bank statement to a spend
 insight dashboard built using Panel and Plotly.

 Before trying tabula-py, check your environment via tabula-py environment_info() function,
 which shows Python version, Java version, and your OS environment.

 check java version: !java -version

 Run this command to install tabula:
 !pip install -q tabula-py
"""


################################################################################
# Only execute the code if the script is ran and not if it is imported         #
################################################################################
#if __name__ == "__main__":
import numpy as np                        # Numerical Python package
import tabula                             # PDF table extra package
import numpy as np
import pandas as pd
import os
import re,string
import sys
from dateutil.parser import parse # Fixing the dates

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# The path to the PDF bank statement
filepath = '~/Documents/2021/02_Projects/Bank_Statement/62598492420 2016-07-15.pdf'


############################################################################
# Function to clean the transaction description column                     #
############################################################################
def clean_trns_desc(text):
    text = text.lower()
    # removing anything within square brackets
    text = re.sub('\[.*?\]', '', text) #TODO: Ensure this is not excluding stuff
    # if any of these punctuation marks in (string.punctuation) get rid of it
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    # Getting rid of all numbers
    text = re.sub('\d+', '', text)
    # get rid of the word purch
    text = re.sub('purch', '', text)
    # Get rid of the word annkp
    text = re.sub('aankp', '', text)
    text = re.sub('puchc', '', text)
    text = re.sub('aankg', '', text)
    return text

round1 = lambda x: clean_trns_desc(x)


# FNB Bank Statement
def main_func(file_input):
    # Move this into the function below
    try:
        df_list = tabula.read_pdf(filepath,stream=True,guess=True,pages='all',
                            multiple_tables=True,
                            pandas_options={
                                'header':None}
                            )
    except Exception as e:
        print('The Error is',e)

    ### Clean up each page before joining them together
    df = []
    for dfs in df_list:
        dfs = dfs[dfs.columns[dfs.isnull().mean() < 0.8]]
        # Drop rows with any empty cells
        dfs.dropna(axis=0,how='any',thresh=2,subset=None,inplace=True)
        # dfs['Description'] = dfs.iloc[:,1].str.cat(dfs.iloc[:,2],sep=" ")
        if dfs.shape[1] > 5:
            dfs.drop(dfs.columns[-1],axis=1,inplace=True)
            df.append(dfs)
        else:
            df.append(dfs)

    # Join individual dataframes into one
    df_fin = pd.concat([df[1],df[2],df[3],df[4]], axis=0, sort=False) #FIX: make this part dynamic!
    df_fin = df_fin[~df_fin.iloc[:,0].str.contains("Date")]
    df_fin.columns = ['date',"trns_desc_1",'trns_desc_2','trns_desc_3','amount','balance']

    # Get the statement start and end date
    p_s, p_e = df_fin.iloc[0][0], df_fin.iloc[-1][0]

    # Feature Engineering
    #df_fin['month_year'] = df_fin['date'].str.extract(pat = '([A-Z].{2})')
    df_fin['date'] = df_fin['date'].str.strip(" ").astype(str)
    df_fin['trns_date'] = pd.to_datetime(df_fin['date'].apply(parse))
    df_fin['month_year'] = df_fin['trns_date'].dt.strftime('%Y-%m')#.astype('category')
    df_fin['month_year'] = df_fin['month_year'].astype('category')
    #df_fin['month_year_two'] = df_fin['month_year'].astype('str')

    df_fin['cr_dr_ind'] = np.nan

    lst = [df_fin]
    # FIX: Build in an indicator for bank charges
    for col in lst:
        col.loc[col['amount'].str.contains('Cr'), 'cr_dr_ind'] = 'CR'
        col.loc[~col['amount'].str.contains('Cr'), 'cr_dr_ind'] = 'DR'

    # clean amount and balance
    # FIX: add more general strings
    df_fin['amount_cleaned'] = df_fin['amount'].replace(to_replace=['Cr',','], value='', regex=True)
    df_fin['balance_cleaned'] = df_fin['balance'].replace(to_replace=['Cr',','], value='', regex=True)

    df_fin['amount_cleaned'] = pd.to_numeric(df_fin['amount_cleaned'],errors='coerce')
    df_fin['balance_cleaned'] = pd.to_numeric(df_fin['balance_cleaned'],errors='coerce')

    # Get the statement opening and closing balances
    bal_s, bal_e = df_fin['balance_cleaned'].head(1)[0], df_fin['balance_cleaned'].tail(1).tolist()[0]

    # Remove Fees
    df_fin = df_fin[~df_fin['trns_desc_1'].str.startswith('#')]

    # Create column to allow for easier summing
    df_fin['Count'] = 1

    # Get first two words of column 1
    df_fin['trns_type'] = df_fin['trns_desc_1'].str.split(' ').str[0] +' '+ df_fin['trns_desc_1'].str.split(' ').str[1].astype('str')

    df_fin['merchant'] = df_fin['trns_desc_2'].apply(round1).str.strip(" ")

    df_fin['merchant_category'] = np.nan

    lst = [df_fin]

    # Manual process to classify individual transactions
    for col in lst:
        col.loc[(col['merchant'].str.contains(r'\bwoolworths\b|\bok foods\b|\bmetro\b|\bhypersave\b|\bfood lovers\b|\bspar\b|\bsuperspar\b|\bcheckers\b|\bshoprite\b|\bu save|usave\b|\bpick n pay\b|\bpick a pay\b|\bpick  pay\b|\bpnp\b|\bpick npay\b|\bchoppies\b',regex=True)),'merchant_category'] = 'Groceries'
        col.loc[(col['merchant'].str.contains(r'\buber\b|\blefa\b|\bcab\b|\bfuel\b|\bpetro\b',regex=True)),'merchant_category'] = 'Transport/Fuel'
        col.loc[(col['merchant'].str.contains(r'\bbuco\b|\bbuild it\b|\bbuildit\b|\bcashbuild\b|\bctm\b|\bcymot\b|\bgame discount world\b|\bpupkewitz\b',regex=True)),'merchant_category'] = 'Construction'
        col.loc[(col['merchant'].str.contains(r'\bairtime\b',regex=True)),'merchant_category'] = 'Airtime'
        col.loc[(col['merchant'].str.contains(r'\bsavings\b|\bsaving\b|\binvest\b|\binvestment\b',regex=True)),'merchant_category'] = 'Savings & Investments'
        col.loc[(col['merchant'].str.contains(r'\bpizza\b|\bkfc\b|\bhungry lion\b|\bchicken licken\b|\bfishaways\b|\bsteers\b|\bgrill addicts\b|\brocomamas\b|\bspur\b|\bwing it\b|\bjoes beerhouse\b|\bwimpy\b|\bbeer barrel\b|\bchicken inn\b|\bfast food\b',regex=True)),'merchant_category'] = 'Fast Food'
        col.loc[(col['merchant'].str.contains(r'salary|payrol|\bsal\b',regex=True)),'merchant_category'] = 'Salary'
        col.loc[(col['merchant'].str.contains(r'\babc pharmacy\b|\bauas valley pharmacy\b|\bclicks\b|\bdischem\b|\bklein windhoek pharm\b|\bklein windhoek aptee\b|\bvictoria pharmacy\b|\bmedicine world\b|\bpharmacy\b|\bgym\b|\bvirgin active\b|\bnucleus\b|\bcrossfit\b',regex=True)),'merchant_category'] = 'Health & Fitness'
        col.loc[(col['merchant'].str.contains(r'\bairtime\b',regex=True)),'merchant_category'] = 'Airtime'
        col.loc[(col['merchant'].str.contains(r'ocean basket|cappello',regex=True)),'merchant_category'] = 'Restaurant/Bars'

    # 'Other' category
    df_fin['merchant_category'].fillna('Other',inplace=True)

    # Count the number of unpaids
    df_fin['unpaid_ind'] = np.nan

    lst_unpaid = [df_fin]

    for col in lst_unpaid:
        col.loc[(col['merchant'].str.contains(r'\bunpaid\b',regex=True)),'unpaid_ind'] = 1

    df_fin['unpaid_ind'].fillna(0,inplace=True)
    return df_fin, p_s, p_e, bal_s, bal_e

df, p_s, p_e, bal_s, bal_e = main_func(filepath)

# Get the total volume and value of debits and credits
vol_val_table = df.groupby(['month_year','cr_dr_ind']).agg({'Count':'sum','amount_cleaned':'sum'}).reset_index()
vol_val_table = vol_val_table.style.format({"amount_cleaned":"N${:20,.0f}"})\
                 .hide_index()\
                 .bar(subset=["Count",], color='#ee1f5f')\
                 .bar(subset=["amount_cleaned"], color='lightgreen')
#vol_val_table.style.bar(subset=['Count', 'amount_cleaned'], align='mid', color=['#d65f5f', '#5fba7d'])
#print(df)
