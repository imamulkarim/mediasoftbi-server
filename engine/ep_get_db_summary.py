def get_db_summary(db_cursor):
  db_name = "ShopLavender"
  table_names = []

  for row in db_cursor.tables():
    if "sale" in row.table_name or "summary" in row.table_name:
      table_names.append({
        "name": row.table_name,
        "description": row.table_name
      })

  payload = {
    "dbName": db_name,
    "tables": table_names
  }

  return payload