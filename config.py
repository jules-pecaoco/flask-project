import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

#REFER TO YOUR OWN DATABASE CONFIGURATIONS AND DRIVER

# PYODBC
DRIVER = 'SQL SERVER'
SERVER = 'NOT-A-LAPTOP'
DATABASE = 'CanAmazing'

#REFERS TO THE ADMIN TABLE IN YOUR DATABSE
TABLE_NAME = 'Admin' 

connection = pyodbc.connect(
  f"""
  DRIVER={{{DRIVER}}};
  SERVER={SERVER};
  DATABASE={DATABASE};
  TRUSTED_CONNECTION=YES
  """
)

cursor = connection.cursor()


# SQL ALCHEMY
engine = create_engine('mssql+pyodbc://@' + SERVER + '/' + DATABASE + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
conected = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
USER = Base.classes.get(f'{TABLE_NAME}')

Session = sessionmaker(bind=engine)
session = Session()