from database.db_manager import DatabaseManager

db = DatabaseManager()
print("Configurando base de datos de AsmoRoot POS...")
db.insertar_datos_maestros()