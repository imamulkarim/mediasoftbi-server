import pyodbc 

driver = '{ODBC Driver 17 for SQL Server}'
server = '192.168.1.8\\SQL2008'
database = 'ShopLavender'
uid = 'sa'
pwd = 'data'


# FIXME: transfer to env file


###########
# Load Data
###########

connection = pyodbc.connect(f'Driver={driver}; \
                              Server={server}; \
                              Database={database}; \
                              UID={uid}; \
                              PWD={pwd}')


