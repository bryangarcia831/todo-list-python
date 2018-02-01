import mysql.connector
from mysql.connector import errorcode
from ConfigParser import SafeConfigParser, NoSectionError

parser = SafeConfigParser()
parser.read('../properties.ini')

try:
    cnx = mysql.connector.connect(host=parser.get('aws-user-pw', 'host'),
                                  user=parser.get('aws-user-pw', 'user'),
                                  password=parser.get('aws-user-pw', 'password'))
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Incorrect user or password")
    else:
        print(err)
except NoSectionError as err:
    print('You need the correct Properties file in your root directory')
else:
    print('Connection successful')
    cnx.close()
