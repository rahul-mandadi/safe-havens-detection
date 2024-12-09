import sqlite3
import pandas as pd
from connection import Connection
from query import Queries

# This code will add the data into all tables of the database
conn_obj = sqlite3.connect('../safe-haven-detection.db')

conn = Connection(conn_obj).connect()

query = Queries(conn)
query.insert_data()
