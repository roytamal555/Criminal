import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request

#To report a crime
@app.route('/report_crime', methods=['POST'])
def report_crime():
    try:        
        _json = request.json
        _useridtype = _json['useridtype']
        _userid_no = _json['userid_no']
        _crime_name = _json['crime_name']
        _pin_code = _json['pin_code']
        _description = _json['description']
        if _useridtype and _userid_no and _crime_name and _pin_code and _description and request.method == 'POST':
            with mysql.connect() as conn:
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = "INSERT INTO report_crime(useridtype, userid_no, crime_name, pin_code, description) VALUES (%s, %s, %s, %s, %s)"
                bindData = (_useridtype, _userid_no, _crime_name, _pin_code, _description)
                cursor.execute(sqlQuery, bindData)
                conn.commit()
            with mysql.connect() as conn:
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT report_id from report_crime where userid_no = %s", _userid_no)
                report_id = cursor.fetchone()
                respone = jsonify(message=f'Your entry has been successfully entered.\n To check the status, Enter your report ID :\n {report_id}')
                respone.status_code = 200
            return respone
        else:
            return 0
    except:
        return showMessage()

#To find the station details
@app.route('/station_details')
def station_details():
    try:
        with mysql.connect() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("select sc.id as pin_code, sd.area as station_area, d.deputy_email as deputy_email, d.phonenumber as Phone from station_code sc join station_details sd on sc.station_id = sd.id join deputy_details d on sd.deputy_id = d.id")
                empRows = cursor.fetchall()
                respone = jsonify(empRows)
                respone.status_code = 200
                return respone
    except:
        return showMessage()
    
#To find my reported crime
@app.route('/report_crime/<int:report_id>', methods = ["GET"])
def reported_crime(report_id):
    try:
        with mysql.connect() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * from report_crime where report_id =%s", report_id)
                empRows = cursor.fetchone()
                respone = jsonify(empRows)
                respone.status_code = 200
                return respone
    except:
        return showMessage()

#To find one specific station_detail
@app.route('/station_details/<int:station_code>', methods = ["GET"])
def station_detail(station_code):
    try:
        with mysql.connect() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select sc.id as pin_code, sd.area as station_area, d.deputy_email as deputy_email, d.phonenumber as Phone from station_code sc join station_details sd on sc.station_id = sd.id join deputy_details d on sd.deputy_id = d.id where sc.id =%s", station_code)
            empRow = cursor.fetchone()
            respone = jsonify(empRow)
            respone.status_code = 200
            return respone
    except:
        return showMessage()

#To change an existing entry in the report_crime table
@app.route('/change_reported_crime', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _userid_no = _json['userid_no']
        _crime_name = _json['crime_name']
        _description = _json['description']
        _pin_code = _json['pin_code']        
        _json = request.json
        if _userid_no and _crime_name and _description and _pin_code and request.method == 'PUT':            
            sqlQuery = "UPDATE report_crime SET crime_name=%s, description=%s, pin_code=%s WHERE userid_no=%s"
            bindData = (_crime_name, _description, _pin_code, _userid_no)
            with mysql.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                respone = jsonify('Given criminal has been updated successfully')  
                respone.status_code = 200
                return respone
        else:
            return ("LOL")
    except:
        return showMessage()

#To delete an entry in the report_crime table.
@app.route('/delete_reported_crime/<int:report_id>', methods=['DELETE'])
def delete_emp(report_id):
    try:
        with mysql.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM report_crime WHERE report_id =%s", (report_id,))
            conn.commit()
            respone = jsonify('The record of the suspect has been deleted successfully!')
            respone.status_code = 200
            return respone
    except:
        return showMessage()

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Please check the url, request type and the json body: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response
        
if __name__ == "__main__":
    app.run(debug=True, port=5001)