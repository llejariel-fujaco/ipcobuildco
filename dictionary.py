import logging
import pandas as pd

import textTools
import country

###############################################################################
## Module init
###############################################################################
logger=logging.getLogger(__name__)

###############################################################################
## Noise
###############################################################################
dico_noise=list(set([
    "PLEASE NOTE THAT TWNIC IS NOT AN ISP",
    "PLEASE NOTE THAT CNNIC IS NOT AN ISP",
    "FOR POLICY ABUSE ISSUES CONTACT",
    "ABUSE TEAM FOUNDATION",
    "UPDATED BECAUSE OLD COMPANY "
    ]))  
def isNoise(text):
    text=textTools.basicClean(text)
    for isp in dico_noise:
        if(isp in text):
            logger.info("{} isNoise".format(text))
            return(True)

    return(False)

###############################################################################
## ISP
###############################################################################
dico_isp=list(set([
    "GVA GABON",
    "TRUEINTERNET",
    "SPITFIRE NETWORK",
    "FREENET",
    "ER TELECOM",
    "UNITYMEDIA",
    "CHARTER COMMUNICATIONS",
    "BELGACOM",
    "MTN SA",
    "AT T ",
    "MCI COMMUNICATIONS",
    "TELKOM",
    "OOREDO",
    "COOL IDEAS SERVICE PROVIDER",
    "VODACOM",
    "AREEBA GUINEE SA",
    "T MOBILE ",
    "SPRINT COMMUNICATIONS",
    "UPC COMMUNICATIONS",
    "ORANGE CAMEROUN",
    "BT PUBLIC",
    "EMTEL",
    "CELL C",
    "VODAFONE",
    "BHARTI AIRTEL",
    "TELEFONICA",
    "MAURITIUS TELECOM",
    "MTN"
]))    
def isISP(text):
    text=textTools.basicClean(text)
    for isp in dico_isp:
        if(isp in text):
            print("Found ISP {0}".format(isp))
            logger.info("{0} isISP => {1}".format(text,isp))
            return(True)
    return(False)

###############################################################################
## Find tokens in a text (Search if some words from a list are contained in a text)
############################################################################### 
def extract_token_in_text(text, token_list):
    text=textTools.basicClean(text)
    result=[]

    # Loop over tokens
    for token in token_list:
        # Token starting text
        if (text.startswith(token+' ')):
            result.append(token)
        # Token in text
        if (text.find(' '+token+' ') >= 0):
            result.append(token)
        # Token finishing text
        if (text.endswith(' '+token)):
            result.append(token)
    
    # Remove duplicates and overlap
    for res in result:
        for cur in result:
            if (cur.find(res) > 0):
                result.remove(res)
    
    return(list(set(result)))

###############################################################################
## Find company_tokens (ltd, sa ...)
############################################################################### 
company_token=list(set([
    "ASSOCIATES","AKTIEBOLAG","AB","AS","A S","B V","BV","CORPORATION",
    "CORP","COMPANY","COMPANIES","COMMUNICATION","COMMUNICATIONS",
    "CLINIC","CLINIQUE","ISP","INTERNET SERVICE","INC","CO","LTD",
    "BANK","BANQUE","BANCO","BANCA","NATIONAL","PARTNERSHIP","COOPERATIVE",
    "CREDIT","UNION","ASSOCIATION","ASSOCIES","BUSINESS","INDUSTRIES",
    "TRUST","PARTNERSHIPS","LP","L P","LIMITED PARTNERSHIP","LLP",
    "LIMITED LIABILITY PARTNERSHIP","LLLP","GROUP","GROUPE","GRUPO","GROUP L P",
    "LIMITED","LIMITED LIABILITY LIMITED PARTNERSHIP","LIMITED LIABILITY COMPANIES",
    "LLC","LC","LTD CO","LIMITED LIABILITY COMPANY","PLLC PROFESSIONAL LIMITED LIABILITY COMPANY",
    "CORPORATIONS","CORP","HOLDINGS","HOLDING","INC","INCORPORATED","PROFESSIONAL",
    "PC","P C","S P A","COMMONWEALTH","BANK","BANKING","BANKERS","TRUST COMPANY",
    "LIMITED LIABILITY COMPANY","LIMITED COMPANY","L L C","L C ","TRUSTEE",
    "CREDIT UNION","PROFESSIONAL CORPORATION","SOCIETA PER AZIONI","S P A ",
    "CLUB","FOUNDATION","FUND","INSTITUTE","SOCIETY","UNION","SYNDICATE","UNIVERSITY",
    "DOING BUSINESS AS","D B A","REGISTERED LIMITED LIABILITY PARTNERSHIP",
    "SERVICE CORPORATION","PROFESSIONAL CORPORATION","LIMITED LIABILITY LIMITED PARTNERSHIP",
    "BANK","BANQUE","BANKING","BANKER","CAPITAL","TRUST","COOPERATIVE ","CONSULTING",
    "CONSULTANT","CONSULTANTS","INDUSTRIAL","LOAN","SAVINGS","HOME","ASSOCIATION",
    "SOCIETY","COLLEGE","CHURCH","EMPLOYMENT","EMPLOI","SAFE DEPOSI","TRUSTEE",
    "HOMESTEAD","INSURANCE","REINSURANCE","CASUALTY","DISTRIBUTION","DISTRIBUTIE","DISTRIBUTING",
    "REDEVELOPMENT CORPORATION","ELECTRIC COOPERATIVE","ELECTRONICS","ELECTRONIC",
    "CHARTERED","COOPERATIVE","PROFESSIONAL ASSOCIATION","CHTD","BOARD OF TRADE",
    "STATE POLICE","URBAN DEVELOPMENT","CHAMBER OF COMMERCE","STATE TROOPER",
    "URBAN RELOCATION","COMMUNITY RENEWAL","TENANT RELOCATION","ACCEPTANCE",
    "ENDOWMENT","ANNUITY","GROCERY","FIDELITY","MORTGAGE","ASSURANCE","FINANCE",
    "SAVINGS","OY","OYJ","AGENCY","PTY LTD","L L L P","R L L L P","LLLP",
    "RLLLP","LEGAL","JURIDIQUE","FREELANCERS","CONTRACTORS","CONTRACTOR",
    "ENTREPRISE INDIVIDUELLE","INVESTMENT FUNDS","COMPANIES",
    "FCP","FOND COMMUN DE PLACEMENT","INVESTMENT","SOCIETE",
    "MATERNITY","PREVOYANCE","INVESTISSEMENT","INVESTORS","INVESTMENT TRUST",
    "SICAV","SOCIETE D INVESTISSEMENT A CAPITAL VARIABLE","ICVC","GIE",
    "GROUPEMENT D'NTERET ECONOMIQUE","SANITATION","SANITAIRE","SEP",
    "SOCIETE EN PARTICIPATION","SNC","SOCIETE EN NOM COLLECTIF","SCS",
    "SOCIETE EN COMMANDITE SIMPLE","SCA","SOCIETE EN COMMANDITE PAR ACTIONS",
    "SCI","SOCIETE CIVILE IMMOBILIERE","SOCIETE","SARL","SOCIETE A RESPONSABILITE LIMITEE",
    "EURL","ENTREPRISE UNIPERSONNELLE","ENTREPRISE","STOCK COMPANIES",
    "SA","S A","SOCIETE ANONYME","SOCIEDAD ANONIMA","SCOP","COOPERATIVE ",
    "SEM","SAS","SASU","EINZELUNTERNEHMEN","AGRICULTURE","FORESTRY",
    "KAUFMANN","PERSONENGESELLSCHAFTEN","GESELLSCHAFT MIT BESCHRAENKTER HAFTUNG",
    "GESELLSCHAFT M B H","GESELLSCHAFT MBH","GESELLSCHAFT BUGERLICHEN RECHTS ",
    "GBR","BGB","GESELLSCHAFT","OFFENE HANDELSGESELLSCHAFT","OHG",
    "KOMMANDITGESELLSCHAFT","KG","GGMBH","GMBH  CO","GMBH","AG CO KG","AG",
    "OHG","PARTNERSCHAFTSGESELLSCHAF","PROFESSIONAL","PARTNERSCHAFTSGESELLSCHAFT",
    "PARTGMBBH","PARTENREEDEREI","SOFTWARE","EINGETRAGENER VEREIN","EV",
    "E V","ALTRECHTLICHER VEREIN","VEREIN","KAPITALGESELLSCHAFTEN",
    "KGAA","KOMMANDITGESELLSCHAFT AUF AKTIEN","AG","GESELLSCHAFT MIT BESCHRANKTER HAFTUNG",
    "MBH","UNTERNEHMERGESELLSCHAFT","AKTIENGESELLSCHAFT ","EINGETRAGENE GENOSSENSCHAFT",
    "E G","STIFTUNG","CIC","COMMUNITY INTEREST COMPANY","CIO",
    "CHARITABLE INCORPORATED ORGANISATION","INDUSTRIAL","HARITY",
    "PARTNERSHIPS","GENERAL PARTNERSHIP","LLP",
    "LIMITED LIABILITY PARTNERSHIP","SCOTTISH LIMITED PARTNERSHIPS","LP","LIMITED PARTNERSHIP",
    "PARTNERS","PRIVATE LIMITED COMPANIES","PRIVATE COMPANY LIMITED",
    "PUBLIC LIMITED COMPANIES","PLC","PUBLIC LIMITED COMPANY",
    "PROPERTY","PROPERTIES","PTY LIMITED","UNLIMITED COMPANY","SOLE PROPRIETORSHIP",
    "ARTIGIANO","LAVORATORE AUTONOMO","LIBERO PROFESSIONISTA","S S","SOCIETA","S A U",
    "SERVICES","SERVICE","S N C","S A S","SOCIETA DI CAPITALI","S P A ",
    "S A P A","AZIONI","S C P A","S C A R L","S R L","S C R L","N V","NV"
]))

def extract_company_tokens(text):
    result=extract_token_in_text(text,company_token)    
    return list(set(result))

###############################################################################
## Find activity_tokens (ltd, sa ...)
############################################################################### 
activity_token=list(set([
    "AVIATION","AIRPORT","AEROPORT","AIRCRAFT","AID","AIDS",
    "AUDIO","ALIMENTATION","ALIMENTACION","ASSET MANAGEMENT",
    "ARCHITECTURAL","ARCHITECTURE","BREWERY","BEVERAGE","BEER","BREWERIES",
    "CASINOS","CASINO","CONSTRUCTORS","CONSTRUCTION",
    "COOPERATIVA ","AGRICULTURE","AEROSPACE","AEROSPATIAL","AEROSPATIALE",
    "ADVERTISING","PUBLICITE","SCHOOL","UNIVERSITY","UNIVERSITE",
    "HUNTING","FACILITIES","FABRICS","FABRIC","FABRIQUE","FORESTRY",
    "FARMING","FARMS","FARM","FOODS","FOOD","ALIMENTATION","ALIMENTAIRE","GROCERS",
    "FERME","VETERINARY","VETERINAIRE","GARDENING","HORTICULTURE","HEALTH CARE","HEALTHCARE","HEALTH",
    "HUNTING","IARD","INN","HOTEL","MOTEL","CHASSE","DENTAL","DENTAIRE","FISHING",
    "PISCICULTURE","MINING","QUARRYING","ENERGY","ENERGIE","ENERGIA","INVESTMENT","INVESTMENTS",
    "LODGING","PACKING","PETROLEUM","PETROLE","PETROLIFERA","PETROLS","PETROLIERS",
    "PETROLIER","MINING","GAS","GAZ","GRILL","MANUFACTURING","HOME","MANUFACTURE","MUSIC","MUSIQUE",
    "FOOD","ALIMENT","ALIMENTAIRE","BEVERAGES","FOUNDRY","FONDERIE","TABAC","TOBACCO","OILS",
    "OIL","FRUIT","VEGETABLES","MECHANICAL","LEGUMESS","STORES","STORE","MAGASIN","FISH",
    "TEXTILES","TEXTILE","TELECOM","TELECOMMUNICATIONS","TRUCKING","TRUCK","VETEMENT","LEATHER",
    "WEAR","FOOTWEAR","FINANCIERE","FINANCE","FINANCIERA","CLOTHES","APPAREL","DRESSING",
    "MATERIALS","FASHION","FUELS","FUEL","MODE","WOOD","BOIS","PUBLISHING","PRINTING",
    "POULTRY","EDITION","EDITRICE","EDITIONS","GAMING","NEWS","MEDIA","IMPRESSION",
    "NUCLEAR","NUCLEAIRE","NURSERY","PRODUCTS","PRODUITS","FUEL","ESSENCE","CHEMICAL","CHEMICALS","CHIMIQUES","CHIMIQUE",
    "PHARMA","PHARMACEUTICALS","PHARMACEUTICAL","MEDICINAL","MEDICAL","MEDECINS","MEDECIN",
    "MERCHANDISE","MARCHANDISE","MECHANICAL","MECANIQUE","BOTANICAL","CHIMIQUE","PLASTIC","METALLIC",
    "MINERAL","MUSEUM","MUSEE","MACHINERY","EQUIPMENT","TRANSPORT","TRANSPORTATION","FURNITURE","MEUBLE",
    "MEUBLES","RENTALS","RENTAL","LOCATION","RECYCLING","ELECTRICITY","ELECTRICIDAD","ELECTRICITE","ELECTRICAL","ELECTRICA","ELECTRIC",
    "GAS","WATER","SUPPLY","SUPPLIES","BANK","BANKING","BANKER","TRUST","LOGISTICS","LOGISTIC","LOGISTIQUE",
    "LOAN","SAVINGS","LOAN","OUTDOOR","COLLEGE","CHURCH","LABORATORIES","LABORATORY","LABORATOIRE",
    "LABORATOIRES","TRUSTEE","HOMESTEAD","HOSPITALITY","HOPITAUX","HOPITAL","HOSPITAL","HOSPITALS","INSURANCE",
    "CONSTRUCTION","COSTRUTTORI","CONSTRUCCIONES","CONTRACTING","ENGINEERING","INGENIERIE","WHOLESALE","RETAIL",
    "TRADE","TRANSIT","TRADING","REPAIR","MOTOR","VEHICLES","VOITURE","AUTO","CARS","CAR",
    "AUTOMOBILE","AUTOMOTIVE","AUTOMOVEIS","AUTOCYCLE","AUTOMOVILES","MOTORCYCLES","MOTORS","MOTOR","HOTELS",
    "HOTEL","RESTAURANTS","RESTAURANT","BARS","BAR","RESTAURANT","RESTAURANTS","TRANSPORT","STORAGE",
    "COMMUNICATION","AIR","RAIL","AIRLINE","TRAVE","VOYAGE","TOURIST","TOURISM","TOURISTIK","TOURISME",
    "FINANCIAL","FIDUCIAIRE","BANKING","INSURANCE","PENSION","SHORTAGE","COUTIER","COURTAGE","IMMOBILIER",
    "IMMOBILIERE","REAL ESTATE","ESTATE","RENTING","RENT","LOCATION","ADMINISTRATION",
    "SUPERMARCHE","SUPER MARKET","SUPERMARKET","SUPERMERCADO","MERCADO","MARKET","PACKAGING",
    "EDUCATION","ECOLE","COMMUNITY SCHOOL","COMMUNITY SCHOOLS","SCHOOLS","SCHOOL","COLLEGE","LYCEE","UNIVERSITE",
    "UNIVERSITY","LAUNDRY","VIDEO","RADIO","ENTERTAINMENT","DIVERTISSEMENT","NEWS","AGENCY","LIBRAIRIE",
    "LIBRARY","MUSEUMS","MUSEE","CULTURAL","CULTURE","SPORTING ",
    "SECURITY","SECURITE","SEGURIDAD","RECREATIONAL"
]))

def extract_activity_tokens(text):
    result=extract_token_in_text(text,activity_token)    
    return list(set(result))

###############################################################################
## Find company and activity tokens (ltd, sa ...) + activity
############################################################################### 
company_activity_token=list(set(company_token+activity_token))

def extract_company_activity_tokens(text):
    result=extract_token_in_text(text,company_activity_token)    
    return list(set(result))

###############################################################################
## Find country tokens
## From country file
## Only given languages
## Clean country name (no accents ...)
############################################################################### 
df_country=pd.read_csv('./data/IP2LOCATION-COUNTRY-MULTILINGUAL/IP2LOCATION-COUNTRY-MULTILINGUAL.CSV',keep_default_na=False)
df_country=df_country.loc[df_country['LANG'].isin(['FR','EN','IT','DE','ES','ZZ'])]
df_country['COUNTRY_NAME']=df_country['COUNTRY_NAME'].apply(textTools.basicClean)

country_name_list=df_country['COUNTRY_NAME'].tolist()
country_code_list=df_country['COUNTRY_ALPHA2_CODE'].tolist() + df_country['COUNTRY_ALPHA3_CODE'].tolist()

def extract_country_tokens(text):
    result=extract_token_in_text(text,country_name_list)   
    return list(set(result))

def extract_country_code_tokens(text):
    country_code_list
    result=extract_token_in_text(text,country_code_list)   
    return list(set(result))

############################################################################### 
## Analyze what can be found in a text based on dictionnaries:
## ex     :  get_all_tokens('SMART ADVERTISING COMPANY FR')
## return : {'activity': ['ADVERTISING'], 'company': ['COMPANY'], 'country': ['FR']}
############################################################################### 
def get_all_tokens(text):
    result={}
    activity_list=extract_activity_tokens(text)
    result['activity']=activity_list
    company_list=extract_company_tokens(text)
    result['company']=company_list
    country_list=extract_country_tokens(text)
    result['country']=country_list
    country_code_list=extract_country_code_tokens(text)
    result['country_code']=country_code_list
    return result

############################################################################### 
## Get company canonical name (Simplified to retrieve meaning)
############################################################################### 
def get_company_canonical(text):
    # Build token dict from company_name
    token_dict=get_all_tokens(text)

    # Count words in company name
    clean_cname=textTools.basicClean(text)
    canonical_cname=clean_cname

    for t in token_dict['company']:
        canonical_cname=textTools.removeToken(t,canonical_cname)
    for t in token_dict['activity']:
        canonical_cname=textTools.removeToken(t,canonical_cname)
    for t in token_dict['country']:
        canonical_cname=textTools.removeToken(t,canonical_cname)
    for t in token_dict['country_code']:
        canonical_cname=textTools.removeToken(t,canonical_cname)
    
    if (textTools.countWords(canonical_cname)==0):
        return(clean_cname)
    else:
        return(canonical_cname)

