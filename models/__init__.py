import pymysql

pymysql.install_as_MySQLdb()

from peewee import MySQLDatabase
from setting import MYSQL_SETTING, MD_MYSQL_SETTINGS

database = MySQLDatabase(MYSQL_SETTING["db_name"], **MYSQL_SETTING["config"])
md_database = MySQLDatabase(MD_MYSQL_SETTINGS["db_name"], **MD_MYSQL_SETTINGS["config"])
