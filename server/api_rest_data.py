#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, requests
import json 
import sqlite3 as lite
import sys
import os
from collections import Counter

def create_connection(db_name):
    #retirar a linha a seguir
    db_name = "subset_artist_term"
    con = lite.connect('database/' + db_name + '.db')
    return con

#enquanto o bd nao funciona, csv :)
def tags_by_state(state):
        path = os.path.dirname(os.path.realpath(__file__)).split("/")
        path = "/".join(path[:-1])
        
        state_siglas_arq = open("../database/state_siglas.csv")
        artist_mbtag_arq = open("../database/artist_mbtag.csv")
        
        ocorrencias = []

        #dispensa o cabeçalho
        state_siglas_arq.readline()
        artist_mbtag_arq.readline()
        
        state_lines = state_siglas_arq.readlines()
        artist_lines = artist_mbtag_arq.readlines()

        artista_do_state = []

        for linha in state_lines:
            if(linha.split(",")[1].replace("\n", "") == state.replace("'","")):
                artista_do_state.append(linha.split(",")[0])
        
        for linha in artist_lines:
            if(linha.split(",")[0] in artista_do_state):
                ocorrencias.append(linha.split(",")[1].replace("\n", ""))

        query_json = []
        
        return json.dumps(Counter(ocorrencias))

def tags_by_state_name(state_name):
        path = os.path.dirname(os.path.realpath(__file__)).split("/")
        path = "/".join(path[:-1])
        
        state_names_arq = open("../database/usa_artist_state_location.csv")
        artist_mbtag_arq = open("../database/artist_mbtag.csv")
        
        ocorrencias = []

        #dispensa o cabeçalho
        state_names_arq.readline()
        artist_mbtag_arq.readline()
        
        state_lines = state_names_arq.readlines()
        artist_lines = artist_mbtag_arq.readlines()

        artista_do_state = []

        for linha in state_lines: 
            if(linha.split(",")[3].replace("\n", "") == state_name.replace("'","")):
                artista_do_state.append(linha.split(",")[0])
        

        for linha in artist_lines:
            if(linha.split(",")[0] in artista_do_state):
                ocorrencias.append(linha.split(",")[1].replace("\n", ""))

        query_json = []
        
        return json.dumps(Counter(ocorrencias))

def states_by_tag(tag):
        path = os.path.dirname(os.path.realpath(__file__)).split("/")
        path = "/".join(path[:-1])
        
        "artist_mbtag, sigla"
        state_siglas_arq = open("../database/state_siglas.csv")
        "artist_id, mbtag"
        artist_mbtag_arq = open("../database/artist_mbtag.csv")
        
        ocorrencias = []

        #dispensa o cabeçalho
        state_siglas_arq.readline()
        artist_mbtag_arq.readline()
        
        state_lines = state_siglas_arq.readlines()
        artist_lines = artist_mbtag_arq.readlines()

        artista_da_tag = []

        for linha in artist_lines:
            linha_limpa = linha.split(",")[1].replace("\n", "")
            if(linha_limpa[1:len(linha_limpa)] == tag.replace("'","")):
                artista_da_tag.append(linha.split(",")[0])
        
        for linha in state_lines:
            if(linha.split(",")[0] in artista_da_tag):
                ocorrencias.append(linha.split(",")[1].replace("\n", ""))

        query_json = []
        
        return json.dumps(Counter(ocorrencias))

#enquanto o bd nao funciona, csv :)
def artist_id_by_state_location_csv(state):
    try:
        arq = open("../database/csv/usa_artist_state_location.csv")
        query_json = []

        #dispensa o cabeçalho
        arq.readline()
        
        lines = arq.readlines()
        for line in lines:
            split_line = line.split(",")
            if (split_line[3].lower().replace("\n","") == state.lower().replace("\n","")):
                tupl = {}
                tupl["artist_id"] = split_line[0].replace("\n","")
                tupl["state"] = split_line[3].lower().replace("\n","")
                query_json.append(tupl)

        return json.dumps(query_json)

    except lite.Error, e:
        return "Error %s:" % e.args[0]

#enquanto o bd nao funciona, csv :)
def tags_states():
    try:
        arq = open("../database/csv/usa_artist_state_location.csv")
        state_tags = []
        

        #dispensa o cabeçalho
        arq.readline()
        
        lines = arq.readlines()
        for line in lines:
            split_line = line.split(",")
            state = split_line[3]

            
            if (split_line[3].lower().replace("\n","") == state.lower().replace("\n","")):
                tupl = {}
                tupl["artist_id"] = split_line[0].replace("\n","")
                tupl["state"] = split_line[3].lower().replace("\n","")
                state_tags.append(tupl)

        return json.dumps(state_tags)

    except lite.Error, e:
        return "Error %s:" % e.args[0]


def montaJson(spamreader, col):
        response = []
        colunas = col
        i = 0
        for row in spamreader:
                celulas = {}
                for indexColumns in range(0,len(colunas)):
                        celulas[colunas[indexColumns]] = row[indexColumns]
                response.append(celulas)
                i = i + 1;
        return response

#busca o estado relacionado a banda
def state_location_by_artist_id(artist_id):
    try:
        cnxn = create_connection("NOME_DO_BD")
        cursor = cnxn.cursor()

        #uma simples consulta para ver se o db funciona
        query = "SELECT * FROM artist_mbtag;"
        
        #esta é a consulta que deve ser realizada quando o bd estiver funcionando
        #query = "SELECT id, state FROM usa_artist_state_locatio WHERE id =" + id + ";"

        cursor.execute(query)
        rows = cursor.fetchall()
        cnxn.close()
        lista_tuplas = []
        for tupla in rows:
           lista_tuplas.append(tupla)
        col = ["artist_id", "state"]
        response = montaJson(lista_tuplas, col)
        return json.dumps(response).encode("utf-8")

    except lite.Error, e:
        return "Error %s:" % e.args[0]

#busca as bandas relacionadas ao estado
def artist_id_by_state_location(state):
    try:
        cnxn = create_connection()
        cursor = cnxn.cursor()
        
        #uma simples consulta para ver se o db funciona
        query = "SELECT * FROM artist_mbtag WHERE artist_id ='AR00A6H1187FB5402A';"
        
        #esta é a consulta que deve ser realizada quando o bd estiver funcionando
        #query = "SELECT id, state FROM usa_artist_gps_location WHERE state =" + state + ";"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        cnxn.close()
        lista_tuplas = []
        for tupla in rows:
           lista_tuplas.append(tupla)
        col = ["artist_id", "state"]
        response = montaJson(lista_tuplas, col)
        return json.dumps(response).encode("utf-8")
    
    except lite.Error, e:
        return "Error %s:" % e.args[0]

def state_to_abbreviation(state):
    states = {'north dakota': 'ND', 'washington': 'WA', 'rhode island': 'RI', 'tennessee': 'TN', 'wisconsin': 'WI', 'nevada': 'NV', 'maine': 'ME', 'mississippi': 'MS', 'south dakota': 'SD', 'new jersey': 'NJ', 'oklahoma': 'OK', 'wyoming': 'W', 'minnesota': 'MN', 'north carolina': 'NC', 'illinois': 'IL', 'new york': 'NY', 'indiana': 'IN', 'maryland': 'MD', 'louisiana': 'LA', 'idaho': 'ID', 'iowa': 'IA', 'west virginia': 'WV', 'michigan': 'MI', 'kansas': 'KS', 'utah': 'UT', 'virginia': 'VA', 'oregon': 'OR', 'montana': 'MT', 'massachusetts': 'MA', 'vermont': 'VT', 'georgia': 'GA', 'pennsylvania': 'PA', 'hawaii': 'HI', 'kentucky': 'KY', 'nebraska': 'NE', 'new hampshire': 'NH', 'texas': 'TX', 'missouri': 'MO', 'south carolina': 'SC', 'ohio': 'OH', 'new mexico': 'NM'}
    return states[state]

def state_info():
    return {'Mississippi': 'MS', 'Oklahoma': 'OK', 'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ', 'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT', 'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV', 'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI', 'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY', 'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX', 'Nevada': 'NV', 'Maine': 'ME'}

def get_state_main_tag():
    info = state_info()
    states = info.values()
    main_tag = {}

    for state in states:
        tags = json.loads(tags_by_state(state))
        if len(tags.values()) != 0:
            main = max(tags, key = tags.get)
            main_tag[state] = {"fillKey": str(main.strip()), "gender" :  str(main.strip())}

            
    return json.dumps(main_tag)

def timeseries():
    a = open('../database/mainDados.csv', 'r')
    b = a.readlines()
    country = ['country', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    jazz = ['jazz', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pop = ['pop', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rock = ['rock', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    reggae = ['reggae', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    anos = [1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

    for linha in b:
        partes = linha.split(',')
        if partes[1] == 'country':
            country[int(partes[0])-1954]+=1
        elif partes[1] == 'jazz':
            jazz[int(partes[0])-1954]+=1
        elif partes[1] == 'pop':
            pop[int(partes[0])-1954]+=1
        elif partes[1] == 'rock':
            rock[int(partes[0])-1954]+=1
        elif partes[1] == 'reggae':
            reggae[int(partes[0])-1954]+=1

    return json.dumps([country, jazz, pop, rock, reggae])
