# chat conversation
import json
import pymysql
import requests
import http.client
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")
    usuario_id = str(request.json['usuario_id'])

    sql = '''
        SELECT id, usuario_id, hora_inicio, hora_fin, disponible, fecha
        FROM bloquesDisponibles 
        WHERE usuario_id ='''+usuario_id+''' 
        AND fecha BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);
    '''
    cursor.execute(sql)
    resp = cursor.fetchall()
    print(str(resp))

    arrayBloques=[]
    retorno = {
        "bloques":{}
    }
    
    for registro in resp:
        #print(str(registro[2]))
        #fechaini = datetime.strptime(str(registro[2]), '%H:%M:%S')
        #fechaFin = datetime.strptime(str(registro[3]), '%H:%M:%S')
        item={
            "id_bloque":registro[0],
            "usuario_id":registro[1],
            #"hora_inicio":fechaini.date(),
            #"hora_fin":fechaini.date(),
            "hora_inicio":str(registro[2]),
            "hora_fin":str(registro[3]),
            "disponible":registro[4],
            "fecha":registro[5]
        }
        arrayBloques.append(item)
        
    retorno['bloques'] = arrayBloques
    return retorno

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {           
    #        "detalle":"algo falló", 
    #        "validacion":False
    #    }
    #    return retorno

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')