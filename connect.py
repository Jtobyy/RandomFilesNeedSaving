import json
import mysql.connector

from flask import Flask, request, jsonify
from mysql.connector import Error

app = Flask(__name__)
connection = mysql.connector.connect(host='localhost',
                                         database='voipswitch',
                                         user='root')

@app.route("/follow_me")                                         
def add_followMe_entry():
    status = ""
    message = ""
    data = json.loads(request.data.decode('utf-8'))    

    try:
        number = data['number']
        client_type = data['client_type']
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            # get records
            # cursor.execute("SELECT * FROM redirectphones;")
            # record = cursor.fetchone()
            # print("You're connected to database: ", record)
            
            default_rule = """
                <answering_rule>
                    <action type=\"Voicemail\">
                        <forward_to>2348161883639</forward_to>
                    </action>
                </answering_rule>"""
            new_rule = """
                <answering_rule>
                    <action type=\"forward\">
                        <forward_to>{}</forward_to>
                    </action>
                </answering_rule>""".format(number)
            cursor.execute("INSERT INTO redirectphones (follow_me_number) VALUES (:number) WHERE id_client=? AND client_type=:type", (new_rule, client_type))
            connection.commit()
            status = "successful"
            message = "Write was successfule"
            

    except Error as e:
        print("Error while connecting to MySQL", e)
        status = "failed"
        message = "Write was successfule"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        return jsonify({'status': status, 'message': message})