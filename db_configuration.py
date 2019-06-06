from app import app
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt

mysql = MySQL()
bcrypt = Bcrypt(app)

#MySQL configuration settings

app.config['MYSQL_DATABASE_USER'] = 'webserver'
app.config['MYSQL_DATABASE_PASSWORD'] = 'testpw'
app.config['MYSQL_DATABASE_DB'] = 'loginsystem'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
