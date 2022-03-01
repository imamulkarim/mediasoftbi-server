from main import cursor
from engine.product_categories_sales_prediction import make_prediction_api_formatted
import json

categories = ['BUTTER', 'DETERGENT']
prediction = make_prediction_api_formatted(categories, cursor)

print(json.dumps(prediction, indent=2))