import mysql.connector
from mysql.connector import errorcode
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('../properties.ini')

try:
    cnx = mysql.connector.connect(host=parser.get('aws-user-pw', 'host'),
                                  user=parser.get('aws-user-pw', 'user'),
                                  password=parser.get('aws-user-pw', 'password'))
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Incorrect User or Password")
    else:
        print(err)
else:
    print('connection successful')
    cnx.close()
