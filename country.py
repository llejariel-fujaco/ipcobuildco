from pandas import pandas as pd
import textTools as textTools

df_country=pd.read_csv('./data/IP2LOCATION-COUNTRY-MULTILINGUAL/IP2LOCATION-COUNTRY-MULTILINGUAL.CSV')

# Only Taking some languages in consideration (+ZZ is custom !)
df_country=df_country.loc[df_country['LANG'].isin(['FR','EN','IT','DE','ES','ZZ'])]

# Cleaning countries name
df_country['COUNTRY_NAME']=df_country['COUNTRY_NAME'].apply(textTools.basicClean)


country_list=df_country['COUNTRY_NAME'].tolist()

def getCountryList():
    return country_list


def countryCodeAssociatedToACountryName(countryName):
    countryName=textTools.basicClean(countryName)
    
    print(df_country.loc[df_country['COUNTRY_NAME'].isin([countryName])])
    # TODO Renvoyer valeur distincte

def iterateOverCountriesName():
    for index, row in df_country.iterrows():
        print(row['COUNTRY_NAME'])
