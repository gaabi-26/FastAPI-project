# Este fichero es el encargado de gestionar la conexion a la DB

from pymongo import MongoClient

db_client = MongoClient() # Por defecto se conecta al localhost