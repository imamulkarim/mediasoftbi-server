from sklearn.preprocessing import OneHotEncoder
from numpy import array
from os.path import exists
import json



query = '''
  SELECT [PrdName] from [sale201801]
  UNION
  SELECT [PrdName] from [sale201802]
  UNION
  SELECT [PrdName] from [sale201803]
  UNION
  SELECT [PrdName] from [sale201804]
  UNION
  SELECT [PrdName] from [sale201805]
  UNION
  SELECT [PrdName] from [sale201806]
  UNION
  SELECT [PrdName] from [sale201807]
  UNION
  SELECT [PrdName] from [sale201808]
  UNION
  SELECT [PrdName] from [sale201809]
  UNION
  SELECT [PrdName] from [sale201810]
  UNION
  SELECT [PrdName] from [sale201811]
  UNION
  SELECT [PrdName] from [sale201812]
  
  UNION
  
  SELECT [PrdName] from [sale201901]
  UNION
  SELECT [PrdName] from [sale201902]
  UNION
  SELECT [PrdName] from [sale201903]
  UNION
  SELECT [PrdName] from [sale201904]
  UNION
  SELECT [PrdName] from [sale201905]
  UNION
  SELECT [PrdName] from [sale201906]
  UNION
  SELECT [PrdName] from [sale201907]
  UNION
  SELECT [PrdName] from [sale201908]
  UNION
  SELECT [PrdName] from [sale201909]
  UNION
  SELECT [PrdName] from [sale201910]
  UNION
  SELECT [PrdName] from [sale201911]
  UNION
  SELECT [PrdName] from [sale201912]

  UNION

  SELECT [PrdName] from [sale202001]
  UNION
  SELECT [PrdName] from [sale202002]
  UNION
  SELECT [PrdName] from [sale202006]
  UNION
  SELECT [PrdName] from [sale202009]
  UNION
  SELECT [PrdName] from [sale202107]
  UNION
  SELECT [PrdName] from [sale202108]
'''

def load_product_names(db_cursor):

  filename = "productnames_lavender.json"

  if exists(filename):
    print("Loading from json")

    with open(filename, 'r') as file:
      product_names = json.load(file)

    return product_names

  else:
    print("Loading from db and writing to json")

    db_cursor.execute(query)

    product_names = []

    for row in db_cursor:
      product_names.append(row[0])

    with open(filename, 'w') as file:
      json.dump(product_names, file)

    return product_names

def onehot_encoder_product_names(product_names):
  reshaped = array(product_names).reshape(-1,1)

  onehot_encoder = OneHotEncoder(handle_unknown='ignore')
  onehot_encoder.fit(reshaped)
  
  return onehot_encoder

def encode_columns(encoder, dataframe):
  pass

