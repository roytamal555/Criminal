from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin@123'
app.config['MYSQL_DATABASE_DB'] = 'crime'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_SSL_DISABLED'] = True
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)