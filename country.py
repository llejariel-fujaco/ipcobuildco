from pandas import pandas as pd
import textTools as textTools

###############################################################################
## Read country list from file
###############################################################################
df_country=pd.read_csv('./data/IP2LOCATION-COUNTRY-MULTILINGUAL/IP2LOCATION-COUNTRY-MULTILINGUAL.CSV')

# Filter on languages
df_country=df_country.loc[df_country['LANG'].isin(['FR','EN','IT','DE','ES','ZZ'])]

# Clean country names
df_country['COUNTRY_NAME']=df_country['COUNTRY_NAME'].apply(textTools.basicClean)
country_list=df_country['COUNTRY_NAME'].tolist()

###############################################################################
## Get country list
###############################################################################
def get_country_list():
    return country_list

###############################################################################
###############################################################################

def countryCodeAssociatedToACountryName(countryName):
    countryName=textTools.basicClean(countryName)
    
    print(df_country.loc[df_country['COUNTRY_NAME'].isin([countryName])])
    # TODO Renvoyer valeur distincte

def iterateOverCountriesName():
    for index, row in df_country.iterrows():
        print(row['COUNTRY_NAME'])
