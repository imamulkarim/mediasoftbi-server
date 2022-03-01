def get_total(db_cursor, tableName: str, columnName: str):
  
  results = []
  
  query = f'''
    SELECT SUM({columnName}) as TOTAL
    FROM {tableName}
  '''

  db_cursor.execute(query)

  for row in db_cursor:
    results.append(float(row[0]))
  
  return results


def generate_total_insight(db_cursor, tableName: str, columnName: str):

  total = get_total(db_cursor, tableName, columnName)[0]

  return {
    "description": f"Total sales",
    "total": "Tk.{:,.2f}".format(total)
  }