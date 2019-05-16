import textTools
import country

dico_noise=list(set(["PLEASE NOTE THAT TWNIC IS NOT AN ISP",
"PLEASE NOTE THAT CNNIC IS NOT AN ISP",
"FOR POLICY ABUSE ISSUES CONTACT","ABUSE TEAM FOUNDATION",
"UPDATED BECAUSE OLD COMPANY "]))  
def isNoise(text):
    text=textTools.basicClean(text)
    for isp in dico_noise:
        if(isp in text):
            return True
    return False

dico_isp=list(set(["GVA GABON","TRUEINTERNET","SPITFIRE NETWORK",
"FREENET","ER TELECOM","UNITYMEDIA","CHARTER COMMUNICATIONS",
"BELGACOM","MTN SA","AT T ","MCI COMMUNICATIONS",
"TELKOM","OOREDO","COOL IDEAS SERVICE PROVIDER",
"VODACOM","AREEBA GUINEE SA","T MOBILE ","SPRINT COMMUNICATIONS",
"UPC COMMUNICATIONS","ORANGE CAMEROUN","BT PUBLIC",
"EMTEL","CELL C","VODAFONE","BHARTI AIRTEL","TELEFONICA",
"MAURITIUS TELECOM","MTN"]))    


def isISP(text):
    text=textTools.basicClean(text)
    for isp in dico_isp:
        if(isp in text):
            print("Founded ISP {0}".format(isp))
            return True
    return False

# Trouver les domaines
def extractDomainFromEmail():
    pass
    
# Couper les chaines apres certains tokens (CO, LTD...)
company_word_end_words=list(set(["LTD","PTY LTD","SA","SAS"]))    
def extractProbableCompanyName(text,founded_token_list):
    if(len(founded_token_list)==0):
        return text
    text=textTools.basicClean(text)
    min_token_index=9999999999
    for key_word in founded_token_list:
        current_min_token_index=text.find(key_word)    
        if(current_min_token_index<min_token_index and current_min_token_index>0):
            min_token_index=current_min_token_index+len(key_word)
    return(str.strip(text[0:min_token_index]))


# Search if some words from a list are contained in a text 
def doesTextContainsTokenFromList(text,list_Tokens):
    text=textTools.basicClean(text)
    results=[]
    
    for key_word in list_Tokens:
        # Search word as a middle token
        if(" "+key_word+" " in text):
            results.append(key_word)
        # Search word as a starting token
        if(key_word+" " in text and text.find(key_word)==0):
            results.append(key_word)
        # Search word as a end token
        if(" "+key_word in text and text.find(key_word)==(len(text)-len(key_word))):
            results.append(key_word)
            
    # Sometimes some tokens are included into other tokens. Only keep the biggest:
    if(len(results)>1):
        for token in results:
            # Removing current token from the list
            results.remove(token)
            flag_is_included=False
            for token_2 in results:
                if token in token_2:
                    # if current token is included in other token, we will keep the list as is
                    flag_is_included=True
            # After checking all tokens, if token is NOT included into other token, we re-add it in result list        
            if flag_is_included == False :
                results.append(token)
            
        
        
    return list(set(results))

# Search company word in a text
def containsCompanyWord(text):
    results=doesTextContainsTokenFromList(text,company_words)    
    return list(set(results))

# Search activity tag in a text
def containsActivityTag(text):
    results=doesTextContainsTokenFromList(text,activity_tags)    
    return list(set(results))

# Search company word in a text
def containsCompanyTag(text):
    results=doesTextContainsTokenFromList(text,company_tags)    
    return list(set(results))

# Search company word in a text
def containsCountry(text):
    results=doesTextContainsTokenFromList(text,country.getCountryList())  
    return list(set(results))


# Analyze what can be found in a text based on dictionnaries:
# ex     :  analyzeText('SMART ADVERTISING COMPANY FR')
# return : {'activity': ['ADVERTISING'], 'company': ['COMPANY'], 'country': ['FR']}
def analyzeText(text):
    result={}
    activity_tags_list=containsActivityTag(text)
    result['activity']=activity_tags_list
    company_tags_list=containsCompanyTag(text)
    result['company']=company_tags_list
    countries_list=containsCountry(text)
    result['country']=countries_list
    return result
  
    

# Transform company name to canonicalForm , enriched with what was found.
def companyCanonicalForm(text,analysis_dict,verbose=False):
    # Clean text
    cleaned_text=textTools.basicClean(text)
    
    # Get number of tokens
    nb_tokens=textTools.countWords(cleaned_text)
    
    # Get number of tokens covered by founded keywords
    allWords=[]
    nb_tokens_country=0
    nb_tokens_company=0
    nb_tokens_activity=0
    
    if(analysis_dict.get('country')!=None):
        allWords=allWords+ analysis_dict.get('country')
        for w in analysis_dict.get('country'):
            nb_tokens_country=nb_tokens_country+textTools.countWords(w)
    
    if(analysis_dict.get('company')!=None):
        allWords=allWords+analysis_dict.get('company')
        for w in analysis_dict.get('company'):
            nb_tokens_company=nb_tokens_company+textTools.countWords(w)
    if(analysis_dict.get('activity')!=None):
        allWords=allWords+analysis_dict.get('activity')
        for w in analysis_dict.get('activity'):
            nb_tokens_activity=nb_tokens_activity+textTools.countWords(w)
    
    nb_tokens_covered_by_keywords=0
    for w in allWords:
        nb_tokens_covered_by_keywords=nb_tokens_covered_by_keywords+textTools.countWords(w)
    
    if verbose:
        print(" * Analysis : {0} ".format(analysis_dict))
        print(" * country {0} company {1} activity {2}".format(nb_tokens_country,nb_tokens_company,nb_tokens_activity))
        print(" * Coverage by keywords {0}/{1}".format(nb_tokens_covered_by_keywords,nb_tokens))
        print(allWords)
    
    # Get Canonical Form
    canonical_form=""
    # If All tokens are keyword, do nothin : Ex BANK OF CHINA
    if(nb_tokens_covered_by_keywords==nb_tokens):
        canonical_form=cleaned_text
    else:
        canonical_form=cleaned_text
        for w in allWords:
            canonical_form=textTools.removeToken(w,canonical_form)
        canonical_form=textTools.basicClean(canonical_form)
        
    return canonical_form


# company_words is the full list of COMPANY TAG (SA,CORP,SCRL...)  +  ACTIVITY TAG (ENERGY,BANK...)
company_tags=list(set(["ASSOCIATES","AKTIEBOLAG","AB","AS","A S","B V","BV","CORPORATION",
"CORP",
"COMPANY",
"COMPANIES",
"COMMUNICATION",
"COMMUNICATIONS",
"CLINIC","CLINIQUE",
"ISP",
"INTERNET SERVICE",
"INC",
"CO",
"LTD",
"BANK","BANQUE","BANCO","BANCA",
"NATIONAL",
"PARTNERSHIP",
"COOPERATIVE",
"CREDIT",
"UNION",
"ASSOCIATION","ASSOCIES",
"BUSINESS","INDUSTRIES",
"TRUST",
"PARTNERSHIPS",
"LP","L P",
"LIMITED PARTNERSHIP",
"LLP",
"LIMITED LIABILITY PARTNERSHIP",
"LLLP",
"GROUP","GROUPE","GRUPO","GROUP L P",
"LIMITED",
"LIMITED LIABILITY LIMITED PARTNERSHIP",
"LIMITED LIABILITY COMPANIES",
"LLC",
"LC",
"LTD CO",
"LIMITED LIABILITY COMPANY",
"PLLC PROFESSIONAL LIMITED LIABILITY COMPANY",
"CORPORATIONS",
"CORP",
"HOLDINGS",
"HOLDING",
"INC",
"INCORPORATED",
"PROFESSIONAL",
"PC",
"P C",
"S P A",
"COMMONWEALTH",
"BANK",
"BANKING",
"BANKERS",
"TRUST COMPANY",
"LIMITED LIABILITY COMPANY",
"LIMITED COMPANY",
"L L C",
"L C ",
"LLC",
"LC",
"TRUSTEE",
"CREDIT UNION",
"PROFESSIONAL CORPORATION",
"SOCIETA PER AZIONI",
"S P A ",
"CLUB",
"FOUNDATION",
"FUND",
"INSTITUTE",
"SOCIETY",
"UNION",
"SYNDICATE",
"UNIVERSITY",
"DOING BUSINESS AS",
"D B A",
"REGISTERED LIMITED LIABILITY PARTNERSHIP",
"SERVICE CORPORATION",
"PROFESSIONAL CORPORATION",
"LIMITED LIABILITY LIMITED PARTNERSHIP",
"BANK","BANQUE",
"BANKING",
"BANKER",
"CAPITAL",
"TRUST",
"COOPERATIVE ",
"CONSULTING","CONSULTANT","CONSULTANTS",
"INDUSTRIAL",
"LOAN",
"SAVINGS",
"LOAN",
"HOME",
"ASSOCIATION",
"SOCIETY",
"COLLEGE",
"CHURCH","EMPLOYMENT","EMPLOI",
"SAFE DEPOSI",
"TRUSTEE",
"HOMESTEAD",
"INSURANCE","REINSURANCE",
"CASUALTY",
"DISTRIBUTION","DISTRIBUTIE","DISTRIBUTING",
"REDEVELOPMENT CORPORATION",
"ELECTRIC COOPERATIVE",
"ELECTRONICS","ELECTRONIC",
"CHARTERED",
"COOPERATIVE",
"PROFESSIONAL ASSOCIATION",
"CHTD",
"BOARD OF TRADE",
"STATE POLICE",
"URBAN DEVELOPMENT",
"CHAMBER OF COMMERCE",
"STATE TROOPER",
"URBAN RELOCATION",
"COMMUNITY RENEWAL",
"TENANT RELOCATION",
"ACCEPTANCE",
"ENDOWMENT",
"ANNUITY",
"GROCERY",
"FIDELITY",
"MORTGAGE",
"ASSURANCE",
"FINANCE",
"SAVINGS",
"OY",
"OYJ",
"AGENCY",
"PTY LTD",
"L L L P",
"R L L L P",
"LLLP",
"RLLLP",
"LEGAL","JURIDIQUE",
"FREELANCERS",
"CONTRACTORS",
"CONTRACTOR",
"ENTREPRISE INDIVIDUELLE",
"INVESTMENT FUNDS",
"COMPANIES",
"FCP",
"FOND COMMUN DE PLACEMENT",
"INVESTMENT",
"SOCIETE",
"MATERNITY","PREVOYANCE",
"INVESTISSEMENT","INVESTORS",
"INVESTMENT TRUST",
"SICAV",
"SOCIETE D INVESTISSEMENT A CAPITAL VARIABLE",
"ICVC",
"GIE",
"GROUPEMENT D'NTERÊT ECONOMIQUE",
"SANITATION","SANITAIRE",
"SEP",
"SOCIETE EN PARTICIPATION",
"SNC",
"SOCIETE EN NOM COLLECTIF",
"SCS",
"SOCIETE EN COMMANDITE SIMPLE",
"SCA",
"SOCIETE EN COMMANDITE PAR ACTIONS",
"SCI",
"SOCIETE CIVILE IMMOBILIERE",
"SOCIETE",
"SARL",
"SOCIETE A RESPONSABILITE LIMITEE",
"EURL",
"ENTREPRISE UNIPERSONNELLE",
"ENTREPRISE",
"STOCK COMPANIES",
"SA","S A",
"SOCIETE ANONYME","SOCIEDAD ANONIMA",
"SCOP",
"COOPERATIVE ",
"SEM",
"SAS",
"SASU",
"EINZELUNTERNEHMEN",
"AGRICULTURE",
"FORESTRY",
"KAUFMANN",
"PERSONENGESELLSCHAFTEN",
"GESELLSCHAFT MIT BESCHRAENKTER HAFTUNG",
"GESELLSCHAFT M B H",
"GESELLSCHAFT MBH",
"GESELLSCHAFT BUGERLICHEN RECHTS ",
"GBR",
"BGB",
"GESELLSCHAFT",
"OFFENE HANDELSGESELLSCHAFT",
"OHG",
"KOMMANDITGESELLSCHAFT",
"KG",
"GGMBH",
"GMBH  CO",
"GMBH",
"AG CO KG",
"AG",
"OHG",
"PARTNERSCHAFTSGESELLSCHAF",
"PROFESSIONAL",
"PARTNERSCHAFTSGESELLSCHAFT",
"PARTGMBBH",
"PARTENREEDEREI",
"SOFTWARE",
"EINGETRAGENER VEREIN",
"EV",
"E V"
"ALTRECHTLICHER VEREIN",
"VEREIN",
"KAPITALGESELLSCHAFTEN",
"KGAA",
"KOMMANDITGESELLSCHAFT AUF AKTIEN",
"AG",
"GESELLSCHAFT MIT BESCHRANKTER HAFTUNG",
"MBH",
"UNTERNEHMERGESELLSCHAFT",
"AKTIENGESELLSCHAFT ",
"EINGETRAGENE GENOSSENSCHAFT",
"E G",
"STIFTUNG",
"CIC",
"COMMUNITY INTEREST COMPANY",
"CIO",
"CHARITABLE INCORPORATED ORGANISATION",
"INDUSTRIAL",
"HARITY",
"PARTNERSHIPS",
"GENERAL PARTNERSHIP",
"LLP",
"LIMITED LIABILITY PARTNERSHIP",
"SCOTTISH LIMITED PARTNERSHIPS",
"LP",
"LIMITED PARTNERSHIP",
"PARTNERS",
"PRIVATE LIMITED COMPANIES",
"PRIVATE COMPANY LIMITED",
"PUBLIC LIMITED COMPANIES",
"PLC",
"PUBLIC LIMITED COMPANY",
"PROPERTY","PROPERTIES",
"PTY LIMITED",
"UNLIMITED COMPANY",
"SOLE PROPRIETORSHIP",
"ARTIGIANO",
"LAVORATORE AUTONOMO",
"LIBERO PROFESSIONISTA",
"S S",
"SOCIETA",
"S A U",
"SERVICES","SERVICE",
"S N C",
"S A S",
"SOCIETA DI CAPITALI",
"S P A ",
"S A P A",
"AZIONI",
"S C P A",
"S C A R L",
"S R L",
"S C R L",
"N V","NV"
]))


# TODO Il manque des langues 
activity_tags=list(set(["AVIATION","AIRPORT","AEROPORT","AIRCRAFT",
"AID","AIDS",
"AUDIO",
"ALIMENTATION","ALIMENTACION","ASSET MANAGEMENT",
"ARCHITECTURAL","ARCHITECTURE",
"BREWERY","BEVERAGE","BEER","BREWERIES",
"CASINOS","CASINO",
"CONSTRUCTORS","CONSTRUCTION",
"COOPERATIVA ",
"AGRICULTURE",
"AEROSPACE","AEROSPATIAL","AEROSPATIALE",
"ADVERTISING","PUBLICITE",
"SCHOOL",
"UNIVERSITY",
"UNIVERSITE",
"HUNTING",
"FACILITIES",
"FABRICS","FABRIC","FABRIQUE",
"FORESTRY",
"FARMING","FARMS","FARM",
"FOODS","FOOD","ALIMENTATION","ALIMENTAIRE","GROCERS",
"FERME",
"VETERINARY",
"VETERINAIRE",
"GARDENING",
"HORTICULTURE",
"HEALTH CARE","HEALTHCARE","HEALTH",
"HUNTING",
"IARD",
"INN","HOTEL","MOTEL",
"CHASSE",
"DENTAL","DENTAIRE",
"FISHING",
"PISCICULTURE",
"MINING",
"QUARRYING",
"ENERGY",
"ENERGIE","ENERGIA",
"INVESTMENT","INVESTMENTS",
"LODGING",
"PACKING",
"PETROLEUM",
"PETROLE","PETROLIFERA",
"PETROLS",
"PETROLIERS",
"PETROLIER",
"MINING",
"GAS",
"GAZ",
"GRILL",
"MANUFACTURING",
"HOME",
"MANUFACTURE",
"MUSIC","MUSIQUE",
"FOOD",
"ALIMENT",
"ALIMENTAIRE",
"BEVERAGES",
"FOUNDRY","FONDERIE",
"TABAC",
"TOBACCO",
"OILS",
"OIL",
"FRUIT",
"VEGETABLES","MECHANICAL",
"LEGUMESS",
"STORES","STORE","MAGASIN",
"FISH",
"TEXTILES",
"TEXTILE",
"TELECOM",
"TELECOMMUNICATIONS",
"TRUCKING","TRUCK",
"VETEMENT",
"LEATHER",
"WEAR",
"FOOTWEAR","FINANCIERE","FINANCE","FINANCIERA",
"CLOTHES",
"APPAREL",
"DRESSING",
"MATERIALS",
"FASHION",
"FUELS","FUEL",
"MODE",
"WOOD",
"BOIS",
"PUBLISHING",
"PRINTING",
"POULTRY",
"EDITION","EDITRICE",
"EDITIONS",
"GAMING",
"NEWS",
"MEDIA",
"IMPRESSION",
"NUCLEAR","NUCLEAIRE",
"NURSERY",
"PRODUCTS","PRODUITS",
"FUEL",
"ESSENCE",
"CHEMICAL","CHEMICALS","CHIMIQUES","CHIMIQUE",
"PHARMA",
"PHARMACEUTICALS",
"PHARMACEUTICAL",
"MEDICINAL","MEDICAL","MEDECINS","MEDECIN",
"MERCHANDISE","MARCHANDISE",
"MECHANICAL","MECANIQUE",
"BOTANICAL",
"CHIMIQUE",
"PLASTIC",
"METALLIC",
"MINERAL","MUSEUM","MUSEE",
"MACHINERY",
"EQUIPMENT",
"TRANSPORT","TRANSPORTATION",
"FURNITURE",
"MEUBLE",
"MEUBLES",
"RENTALS","RENTAL","LOCATION",
"RECYCLING",
"ELECTRICITY","ELECTRICIDAD","ELECTRICITE","ELECTRICAL","ELECTRICA","ELECTRIC",
"GAS",
"WATER",
"SUPPLY","SUPPLIES",
"BANK",
"BANKING",
"BANKER",
"TRUST",
"LOGISTICS","LOGISTIC","LOGISTIQUE",
"LOAN",
"SAVINGS",
"LOAN",
"OUTDOOR",
"COLLEGE",
"CHURCH",
"LABORATORIES","LABORATORY","LABORATOIRE","LABORATOIRES",
"TRUSTEE",
"HOMESTEAD","HOSPITALITY","HOPITAUX","HOPITAL","HOSPITAL","HOSPITALS",
"INSURANCE",
"CONSTRUCTION","COSTRUTTORI","CONSTRUCCIONES",
"CONTRACTING",
"ENGINEERING",
"INGENIERIE",
"WHOLESALE",
"RETAIL",
"TRADE",
"TRANSIT",
"TRADING",
"REPAIR",
"MOTOR",
"VEHICLES",
"VOITURE",
"AUTO","CARS","CAR",
"AUTOMOBILE","AUTOMOTIVE","AUTOMOVEIS",
"AUTOCYCLE","AUTOMOVILES",
"MOTORCYCLES","MOTORS","MOTOR",
"HOTELS",
"HOTEL",
"RESTAURANTS",
"RESTAURANT",
"BARS",
"BAR",
"RESTAURANT",
"RESTAURANTS",
"TRANSPORT",
"STORAGE",
"COMMUNICATION",
"AIR",
"RAIL",
"AIRLINE",
"TRAVE",
"VOYAGE",
"TOURIST",
"TOURISM","TOURISTIK",
"TOURISME",
"FINANCIAL",
"FIDUCIAIRE",
"BANKING",
"INSURANCE",
"PENSION",
"SHORTAGE",
"COUTIER",
"COURTAGE",
"IMMOBILIER",
"IMMOBILIERE",
"REAL ESTATE","ESTATE",
"RENTING",
"RENT",
"LOCATION",
"ADMINISTRATION",
"SUPERMARCHE","SUPER MARKET","SUPERMARKET","SUPERMERCADO","MERCADO","MARKET",
"PACKAGING",
"EDUCATION",
"ECOLE",
"COMMUNITY SCHOOL","COMMUNITY SCHOOLS",
"SCHOOLS","SCHOOL",
"COLLEGE",
"LYCEE",
"UNIVERSITE",
"UNIVERSITY",
"LAUNDRY",
"VIDEO",
"RADIO",
"ENTERTAINMENT",
"DIVERTISSEMENT",
"NEWS",
"AGENCY",
"LIBRAIRIE",
"LIBRARY",
"MUSEUMS",
"MUSEE",
"CULTURAL",
"CULTURE",
"SPORTING ",
"SECURITY","SECURITE","SEGURIDAD",
"RECREATIONAL"
]))

company_words=list(set(company_tags+activity_tags))
# DICO COUNTRY",

