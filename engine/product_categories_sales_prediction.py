from email.utils import format_datetime
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from os.path import exists
import pickle
from engine.producttypes import load_product_names, onehot_encoder_product_names
from datetime import date, timedelta


def query_prdname_test_201901_train_201801():
  query_test_set = '''
    SELECT
      [SaleDT],
      [PrdName],
      SUM([TotalAmt]) as "TotalAmt"
    FROM
      [sale201901]
    GROUP BY
      [SaleDT],
      [PrdName]        
    ORDER BY
      [SaleDT]
    '''
  
  query_training_set = '''
    SELECT
      [SaleDT],
      [PrdName],
      SUM([TotalAmt]) as "TotalAmt"
    FROM
      [sale201801]
    GROUP BY
      [SaleDT],
      [PrdName]
    ORDER BY
      [SaleDT]
    '''

  return query_test_set, query_training_set

def load_training_data(db_cursor, onehot_encoder):
  print('Loading training data')
  
  _, query_training_set = query_prdname_test_201901_train_201801()
  training_data = db_cursor.execute(query_training_set).fetchall()

  training_data_split_columns = []
  for row in training_data:
    training_data_split_columns.append([*row])
  
  training_data_onehot = []

  for row in training_data_split_columns:
    saleDT = row[0]
    category = row[1]
    totalAmt = float(row[2])

    onehot_row = [totalAmt, saleDT.year, saleDT.month, saleDT.day, saleDT.weekday(), *onehot_encoder.transform([[category]]).toarray().tolist()]
    onehot_row = [*onehot_row[:-1], *onehot_row[-1]]

    training_data_onehot.append(onehot_row)

  return training_data_onehot

def load_testing_data(db_cursor, onehot_encoder):
  print('Loading test data')

  query_test_set, _ = query_prdname_test_201901_train_201801()
  test_data = db_cursor.execute(query_test_set).fetchall()

  test_data_split_columns = []
  for row in test_data:
    test_data_split_columns.append([*row])
  
  test_data_onehot = []

  for row in test_data_split_columns:
    saleDT = row[0]
    category = row[1]
    totalAmt = float(row[2])

    onehot_row = [totalAmt, saleDT.year, saleDT.month, saleDT.day, saleDT.weekday(), *onehot_encoder.transform([[category]]).toarray().tolist()]
    onehot_row = [*onehot_row[:-1], *onehot_row[-1]]

    test_data_onehot.append(onehot_row)
  
  return test_data_onehot

def filter_data_by_category(dataset, category, encoder):
  category_index = np.where(encoder.categories_[0] == category)[0][0]
  filtered = dataset[dataset[:,category_index+5] > 0]
  return filtered

def load_by_category_model(db_cursor, onehot_encoder):
  saved_model_filename = 'by_category_model_v1'

  if exists(saved_model_filename):
    print('Loading saved model')

    infile = open(saved_model_filename, 'rb')
    model = pickle.load(infile)
    infile.close()

  else:
    print('No model saved, creating new model')

    training_data_product = np.array(load_training_data(db_cursor, onehot_encoder))

    training_sales_total = training_data_product[:, 0]
    training_features = training_data_product[:, 1:]

    model = DecisionTreeRegressor().fit(training_features, training_sales_total)

    outfile = open(saved_model_filename, 'wb')
    pickle.dump(model, outfile)
    outfile.close()
  
  return model

def create_prediction_date_range():
  days = []
  days_after = 15
  today = date.today()

  for i in range(days_after + 1):
    day = today + timedelta(days=i)
    days.append(day)

  return days

def create_past_data_date_range():
  days = []
  days_before = 15
  today = date.today()

  for i in range(days_before, 0, -1):
    day = today - timedelta(days=i)
    days.append(day)

  return days

def create_prediction_table(regressionModel, db_cursor, onehot_encoder):
  saved_prediction_filename = 'by_category_predictions_v3'

  if exists(saved_prediction_filename):
    print('Loading saved predictions')

    infile = open(saved_prediction_filename, 'rb')
    prediction_by_category = pickle.load(infile)
    infile.close()
  
  else:
    print('No predictions saved, making new predictions')

    # TODO: Make a table with each item on each day
    # Example: Butter each day for day 1 - day 31, Detergent each day, etc
    # Fill month and year column for following month

    days = create_prediction_date_range()
    
    features_prediction_table = []

    for day_of_month in days:
      for category in onehot_encoder.categories_[0]:
        features_prediction_row = [day_of_month.year, day_of_month.month, day_of_month.day, day_of_month.weekday(), *onehot_encoder.transform([[category]]).toarray().tolist()]
        features_prediction_row = [*features_prediction_row[:4], *features_prediction_row[-1]]
        features_prediction_table.append(features_prediction_row)

    features_prediction_table = np.array(features_prediction_table)

    prediction_sales_totals = np.array(regressionModel.predict(features_prediction_table))
    prediction_sales_totals = prediction_sales_totals.reshape(-1,1)
    prediction_by_category = np.concatenate((prediction_sales_totals, features_prediction_table), axis=1)

    outfile = open(saved_prediction_filename, 'wb')
    pickle.dump(prediction_by_category, outfile)
    outfile.close()

  return prediction_by_category

def filter_prediction_by_category(fullPrediction, categoryName, onehot_encoder):
  prediction_by_category = filter_data_by_category(fullPrediction, categoryName, onehot_encoder)
  prediction_sales_by_category = prediction_by_category[:, 0]
  return prediction_sales_by_category

# TODO: Just one category
def make_prediction_api_formatted(categories, db_cursor):
  product_names = load_product_names(db_cursor)
  onehot_encoder = onehot_encoder_product_names(product_names)

  model = load_by_category_model(db_cursor, onehot_encoder)
  prediction = create_prediction_table(model, db_cursor, onehot_encoder)

  prediction_selected_categories_api_formatted = []
  
  for category in categories:
    prediction_category_only_amounts = filter_prediction_by_category(prediction, category, onehot_encoder).tolist()

    prediction_for_category = {
      "category": category,
      "amounts": prediction_category_only_amounts
    }

    prediction_selected_categories_api_formatted.append(prediction_for_category)
 

  past_data_dates_formatted = list(map(
                        lambda date: date.strftime("%d/%m"),
                        create_past_data_date_range()
                        ))

  prediction_dates_formatted = list(map(
                        lambda date: date.strftime("%d/%m"),
                        create_prediction_date_range()
                        ))

  api_formatted = []

  for index, date in enumerate(past_data_dates_formatted):
    formatted_row = {}
    formatted_row["date"] = date
    formatted_row["past data"] = 10_000
    
    api_formatted.append(formatted_row)

  for index, date in enumerate(prediction_dates_formatted):
    formatted_row = {}
    formatted_row["date"] = date

    for category in prediction_selected_categories_api_formatted:
      category_name = category["category"]
      sale_amount = category["amounts"][index]
      
      formatted_row[category_name] = sale_amount
    
    api_formatted.append(formatted_row)
    

  # api_formatted = {
  #   "dates": dates_formatted,
  #   "predictions": prediction_selected_categories_api_formatted,
  # }

  return api_formatted

