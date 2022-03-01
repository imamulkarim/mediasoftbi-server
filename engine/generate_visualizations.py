def get_categorical_aggregates(db_cursor, tableName: str, category_columnName: str, total_columnName: str):
  query = f'''
    SELECT
      {category_columnName},
      SUM({total_columnName}) AS Total
    FROM
      {tableName}
    GROUP BY
      {category_columnName}
    ORDER BY
      Total DESC
  '''

  results = []

  db_cursor.execute(query)

  for row in db_cursor:
    results.append({
      category_columnName: row[0],
      "Total": float(row[1])
    })
  
  return results[:5]


def get_daily_total_sales(db_cursor, tableName: str):
  query = f'''
    SELECT
      [SaleDT],
      SUM([TotalAmt]) as "Total"
    FROM
      {tableName}
    GROUP BY
      [SaleDT]
  '''

  results = []

  db_cursor.execute(query)

  for row in db_cursor:
    results.append({
      "Date": row[0],
      "Total": float(row[1]),
    })

  return results


def generate_categorical_aggregate_barchart(db_cursor, tableName: str, category_columnName: str, total_columnName: str):
  return {
    "description": f"Totals by {category_columnName}",
    "data": get_categorical_aggregates(db_cursor, tableName, category_columnName, total_columnName),
    "xAxisKey": category_columnName,
    "dataKey": "Total",
  }


def generate_daily_total_sales_linechart(db_cursor, tableName: str):
  return {
    "description": "Daily total sales",
    "data": get_daily_total_sales(db_cursor, tableName),
    "xAxisKey": "Date",
    "dataKey": "Total",
  }

