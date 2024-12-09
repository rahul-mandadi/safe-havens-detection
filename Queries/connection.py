import sqlite3
import pandas as pd

# Connection class to connect to the database
class Connection:
    def __init__(self, conn):
        self.conn = conn
    
    def connect(self):
        return self.conn
    
    