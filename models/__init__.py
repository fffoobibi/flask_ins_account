import pymysql

pymysql.install_as_MySQLdb()

from peewee import MySQLDatabase
from setting import MYSQL_SETTING

database = MySQLDatabase(MYSQL_SETTING["db_name"], **MYSQL_SETTING["config"])
