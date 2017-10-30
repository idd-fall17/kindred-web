from flask import Flask, request
from flask_mysqldb import MySQL

import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'kindred'
mysql = MySQL(app)

@app.route("/")
def hello():
    return "Hello World!"


# get or post profile
# TODO: error handling of any kind
@app.route("/profile/<student_name>/<profile_type>")
def getProfile(student_name, profile_type):
    student_id = getStudent(student_name)[0]    

    # get all devices
    devices = getStudentDevicesByProfile(student_id, profile_type)

    return "Getting Student Profile!"


@app.route("/device", methods=["POST"])
def addDevice():

    # student name
    data = json.loads(request.data)
    student_name = data["student_name"]
    profile_type = data["profile_type"]
    device_id = data["device_id"]
    service_id = data["service_id"]
    read_msg = data["read_msg"]

    # create student
    student = getStudent(student_name) 
    print(student)
    if student is None:
        addStudent(student_name);
        student = getStudent(student_name) 
        print(student)
    student_id = student[0]
    print(student_id);

    # create device
    device_profile = getDeviceProfile(device_id, profile_type);
    if(not device_profile):
        addDeviceProfile(device_id, service_id, profile_type, read_msg);
        device_profile = getDeviceProfile(device_id, profile_type);
    device_profile_id = device_profile[0] 
 
    # add to student_devices
    addStudentDevice(student_id, device_profile_id);
    
    return "DONE!";
 
def getStudent(student_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE student_name = '%s'" % student_name)
    return cur.fetchone()

def getDeviceProfile(device_id, profile):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM device_profiles WHERE device_id = '%s' AND profile = '%s'" % (device_id, profile))
    return cur.fetchone()

def getStudentDevicesByProfile(student_id, profile):
    cur = mysql.connection.cursor()
    sql_statement = "select * from student_devices, device_profiles where student_devices.student_id = %s and student_devices.device_profile_id = device_profiles.id and device_profiles.profile = '%s'" % (student_id, profile);
    cur.execute(sql_statement)
    return cur.fetchall()

def addStudent(student_name):
    conn = mysql.connection
    cur = conn.cursor()
    sql_statement = "INSERT INTO students (student_name) VALUES ('%s')" % student_name;
    cur.execute(sql_statement)
    conn.commit()

def addDeviceProfile(device_id, service_id, profile, read_msg):
    conn = mysql.connection
    cur = conn.cursor()
    sql_statement = "INSERT INTO device_profiles (device_id, service_id, profile, read_msg)VALUES ('%s', '%s', '%s', '%s')" % (device_id, service_id, profile, read_msg);
    cur.execute(sql_statement); 
    conn.commit()

def addStudentDevice(student_id, device_profile_id):
    conn = mysql.connection
    cur = conn.cursor()
    sql_statement = "INSERT INTO student_devices (student_id, device_profile_id) VALUES ('%s', '%s')" % (student_id, device_profile_id);
    cur.execute(sql_statement); 
    conn.commit()

    
    
