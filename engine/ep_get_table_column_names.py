def get_table_column_names(db_cursor, tableName):
  column_names = []

  for row in db_cursor.columns(table=tableName):
    column_names.append({
      "name": row.column_name,
      "type": "unknown" 
    })
  
  return column_names