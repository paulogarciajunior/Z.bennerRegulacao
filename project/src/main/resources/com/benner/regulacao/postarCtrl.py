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

days_in_year = 365.2425    

def conectarMysql():
    mysql_host='ls-435b3683f207e58e58caae8fc7c88b6f0c688ffa.cetfmntu2ycs.us-east-1.rds.amazonaws.com' 
    mysql_port=3306 
    mysql_user='neobe' 
    mysql_password='neobe' 
    mysql_db='neobeORIG' 
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

def autorizar(conteudo):

    host  = "http://34.201.213.20"
    port  = ":8085"
    server= '/kie-server'
    app   = 'Regulacao_1.0.2-SNAPSHOT'
    #processo = 'Regulacao.Elegibilidade'
    processo = 'Regulacao.Triagem_Inicial_e_SLA'
    path  = '/services/rest/server/containers/{v_app}/processes/{v_processo}/instances'.format(
            v_app=app,
            v_processo=processo)

    url = host + port + server + path
    parametros = json.dumps(conteudo,default=str)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=parametros, headers=headers,auth=('wbadmin', 'wbadmin'))
    return [response.status_code,response.text,conteudo]

def docs():
    host  = "http://34.201.213.20"
    port  = ":8085"
    server= '/kie-server'
    #app   = 'Regulacao_1.0.2-SNAPSHOT'
    #processo = 'Regulacao.Elegibilidade'
    #processo = 'Regulacao.email_teste'
    path  = '/services/rest/server/documents'
    url = host + port + server + path
    conteudo = ''
    parametros = json.dumps(conteudo,default=str)
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, headers=headers,auth=('wbadmin', 'wbadmin'))
    print(response.status_code,response.text)

def email():

    host  = "http://34.201.213.20"
    port  = ":8085"
    server= '/kie-server'
    app   = 'Regulacao_1.0.2-SNAPSHOT'
    #processo = 'Regulacao.Elegibilidade'
    processo = 'Regulacao.email_teste'
    path  = '/services/rest/server/containers/{v_app}/processes/{v_processo}/instances'.format(
            v_app=app,
            v_processo=processo)

    url = host + port + server + path
    conteudo = {}
    parametros = json.dumps(conteudo,default=str)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=parametros, headers=headers,auth=('wbadmin', 'wbadmin'))
    return [response.status_code,response.text,parametros]

def send_email_gk2():
    import smtplib
    user='jbpm@triopropaganda.com.br'
    pwd='jbpm.1969'
    recipient='paulo@triopropaganda.com' 
    subject='teste de email jbpm' 
    body='teste de email do jbpm ' + str(datetime.now())

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("mail.triopropaganda.com.br", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

def lerGuias():
    
    def dateToStr(o):
        if isinstance(o, datetime):
            return o.__str__()
    def getControle(guia,
        operadora,
        carateratendimento,
        situacao_original
        ):
        return {'guia':guia,
                'registro_ans':operadora,
                'carater_atendimento':carateratendimento,
                'situacao_original':situacao_original, 
                'sla':'24h',
        		'negativa_cadastral':False,
        		'excecao':True,
        		'urg_emerg_confirmada':False,
        		'prestador_fora_domicilio':False,
                #'operadora_negativas_revertidas':1,
                'exigedocumentacao':False,
                #'documentacaook':True,
                #'documentacafornecida':False,
                'eh_opme':False,
                'eh_oncologica':False,
                'eh_dut_alta_complexidade_cirurgico':True,
                'tipo_sadt':'TERAPIA',
                'tipo_guia':'SP/SADT',
                'reprocessar':False,
        }
            
        
    sql = 'select * from neobeORIG.guia where id = 4'
    cnx = conectarMysql()
    cursor=cnx.cursor()
#    cursor.execute('delete from neobeDES.guiaeventos')
#    cursor.execute('delete from neobeDES.guia')
    cnx.commit()
    cursor.execute(sql)
    guias = cursor.fetchall()
    contador = 1
    for guia in guias:
        print ('guia',guia["id"])
        for campo in guia:
            if type(guia[campo]) is datetime:
                guia[campo]=guia[campo].isoformat()
        conteudo = {
            'controle':{
                'com.benner.regulacao.controle':{
                    'guia_id':guia['id'],
                    'registro_ans':guia['registroans'],
                    'carater_atendimento':guia['carateratendimento'],
                    'situacao_original':guia['regulsituacao'], 
                    'sla':'24h',
            		'negativa_cadastral':False,
            		'excecao':True,
            		'urg_emerg_confirmada':False,
            		'prestador_fora_domicilio':False,
                    'operadora_negativas_revertidas':1,
                    'exigedocumentacao':False,
                    'documentacaook':True,
                    'documentacafornecida':False,
                    'eh_opme':False,
                    'eh_oncologica':False,
                    'eh_dut_alta_complexidade_cirurgico':False,
                    'tipo_sadt':'HOME-CARE',
                    'tipo_guia':guia['regultipoguia'],
                    'reprocessar':False,
                }
            }
        }
        print (json.dumps(conteudo, indent=4, sort_keys=True))        
        resposta = autorizar(conteudo)
        print ('contador:',contador,'code:',resposta[0],'Process id:',resposta[1])
        contador +=1
        if contador > 4:
            break
#print (email())
lerGuias()
#docs()
