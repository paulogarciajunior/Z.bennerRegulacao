# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:19:59 2019

@author: paulo
"""

import unicodedata
import unidecode
from unidecode import unidecode
import pprint
import pandas as pd
import json
import datetime
from bson.objectid import ObjectId
import requests
import pymysql

from datetime import datetime
from datetime import timedelta 

#d1 = datetime(2019, 3, 26)
#d2 = datetime(1969, 9, 12)

days_in_year = 365.2425    



def conectarMysql(server):
    mysql_host='ls-435b3683f207e58e58caae8fc7c88b6f0c688ffa.cetfmntu2ycs.us-east-1.rds.amazonaws.com' 
    mysql_port=3306 
    mysql_user='dbmasteruser' 
    mysql_password='paulo.garcia.junior' 
    mysql_db='benner' 
    mysql_charset = 'utf8'

    conexao = pymysql.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        db=mysql_db,
        charset=mysql_charset,
        port=mysql_port,
        cursorclass=pymysql.cursors.DictCursor)
    return conexao




def autorizar():
    def dateToStr(o):

        if isinstance(o, datetime):
            return o.__str__()
    
    DT = dateToStr(datetime.now())
    
    host  = "http://34.201.213.20"
    port  = ":8085"
    server= '/kie-server'
    app   = 'Regulacao_1.0.0-SNAPSHOT'
    processo = 'Regulacao.Elegibilidade'
    path  = '/services/rest/server/containers/{v_app}/processes/{v_processo}/instances'.format(
            v_app=app,
            v_processo=processo)

    print (path)
    
    #Está inserindo corretamente - neste caso as tabelas estão relacionadas.
    conteudo = {
        "guia":{
            "com.benner.regulacao.guia":{                    
                "id":1,
                "anexoclinico":False,
                "observacao":"OBSERVACAO"+DT,
                "CBOS":"OBSERVACAO"+DT,
                "registro_Ans":"REGISTRO_ANS"+DT,
            }
        }
    }
            
    url = host + port + server + path
    parametros = json.dumps(conteudo,default=str)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=parametros, headers=headers,auth=('wbadmin', 'wbadmin'))
    return [response.status_code,response.text,conteudo]

print (autorizar())