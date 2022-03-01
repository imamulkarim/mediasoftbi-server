from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

from engine.connection import connection
from engine.ep_get_db_summary import get_db_summary
from engine.ep_get_table_column_names import get_table_column_names

from engine.generate_insights import generate_total_insight
from engine.generate_visualizations import generate_categorical_aggregate_barchart, generate_daily_total_sales_linechart

from engine.producttypes import load_product_names
from engine.product_categories_sales_prediction import make_prediction_api_formatted


###############
# Set up server
###############

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

cursor = connection.cursor()





########
# Routes
########

@app.get("/")
def index():
  return {
    "response": "Server running"
  }


@app.get("/getDBSummary")
def get_db_Summary():
  return get_db_summary(cursor)


@app.get("/getTableColumnNames")
def get_Table_column_names(tableName: str):
  return get_table_column_names(cursor, tableName)


class Active_Columns_Req_Body(BaseModel):
  tableName: str
  columnNames: List[str]


class Prediction_Columns_Req_Body(BaseModel):
  tableName: str
  categories: List[str]

@app.post("/setActiveColumns")
def set_active_columns(Active_Columns_Req_Body: Active_Columns_Req_Body):

  insights = []
  keyfigures = []

  linecharts = []
  barcharts = []


  if "TotalAmt" in Active_Columns_Req_Body.columnNames:
    total = generate_total_insight(cursor, Active_Columns_Req_Body.tableName, "TotalAmt")
    keyfigures.append(total)
    
    daily_sales = generate_daily_total_sales_linechart(cursor, Active_Columns_Req_Body.tableName)
    linecharts.append(daily_sales)
    
  
  if "PrdName" in Active_Columns_Req_Body.columnNames:
    barchart_by_product = generate_categorical_aggregate_barchart(cursor, Active_Columns_Req_Body.tableName, "PrdName", "TotalAmt")
    barcharts.append(barchart_by_product)
  
  if "SupName" in Active_Columns_Req_Body.columnNames:
    barchart_by_product = generate_categorical_aggregate_barchart(cursor, Active_Columns_Req_Body.tableName, "SupName", "TotalAmt")
    barcharts.append(barchart_by_product)
  
  if "GroupName" in Active_Columns_Req_Body.columnNames:
    barchart_by_product = generate_categorical_aggregate_barchart(cursor, Active_Columns_Req_Body.tableName, "GroupName", "TotalAmt")
    barcharts.append(barchart_by_product)
  
  if "BTName" in Active_Columns_Req_Body.columnNames:
    barchart_by_product = generate_categorical_aggregate_barchart(cursor, Active_Columns_Req_Body.tableName, "BTName", "TotalAmt")
    barcharts.append(barchart_by_product)

  return {
    "reports": {
      "insights": insights,
      "keyfigures": keyfigures,
      "visualizations": {
        "linecharts": linecharts,
        "barcharts": barcharts,
      }
    }
  }


@app.get("/getProductCategories")
def get_product_categories():
  return load_product_names(cursor)

@app.post("/selectProductCategoriesForPrediction")
def select_product_categories_for_prediction(Prediction_Columns_Req_Body: Prediction_Columns_Req_Body):
  selected_categories = Prediction_Columns_Req_Body.categories

  formatted_selected_categories = make_prediction_api_formatted(selected_categories, cursor)

  return formatted_selected_categories
