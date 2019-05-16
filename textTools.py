#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 22:32:55 2019

@author: decafeinato
"""
import re,string

def basicClean(stringValue):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    stringValue=regex.sub(' ',stringValue )
    
    
    conversion_dict = {"\n":" ","ä": "a", "ö": "o", "ü": "u","Ä": "A", "Ö": "O", "Ü": "U",
                   "á": "a", "à": "a", "â": "a", "é": "e", "è": "e", "ê": "e","Ë":"E",
                   "î":"i","ï":"i","Ï":"I","Î":"I","Ç":"C",
                   "ú": "u", "ù": "u", "û": "u", "ó": "o", "ò": "o", "ô": "o",
                   "Á": "A", "À": "A", "Â": "A", "É": "E", "È": "E", "Ê": "E",
                   "Ú": "U", "Ù": "U", "Û": "U", "Ó": "O", "Ò": "O", "Ô": "O","ß": "s"}  
                   
    for key,Value in conversion_dict.items():
        stringValue=stringValue.replace(key,Value)            
    
    stringValue=stringValue.replace('  ',' ')
    stringValue=str.strip(str.upper(stringValue))
    
    return stringValue

def countWords(text):
    _re_word_boundaries = re.compile(r'\b')
    return len(_re_word_boundaries.findall(text)) >> 1


def removeToken(token,text):
    # middle token
    text=text.replace(" "+token+" "," ")
    # starting token
    if(text.find(token+" ")==0):
        text=text[len(token+" "):len(text)]
    # end token
    if text[len(text)-len(' '+token):len(text)]  == ' '+token :
        text=text[0:len(text)-len(' '+token)]

    return text