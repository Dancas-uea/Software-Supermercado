from dotenv import load_dotenv
import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parents[1] / "Variables de entorno" / ".env"
load_dotenv(dotenv_path=dotenv_path)


def obtener_variable(nombre: str) -> str:
	valor = os.getenv(nombre)
	if not valor:
		raise RuntimeError(f"Falta la variable de entorno: {nombre}")
	return valor

def main():
	conn = psycopg2.connect(
		host=obtener_variable("DB_HOST"),
		port=obtener_variable("DB_PORT"),
		dbname=obtener_variable("DB_NAME"),
		user=obtener_variable("DB_USER"),
		password=obtener_variable("DB_PASSWORD"),
	)
	try:
		with conn.cursor() as cur:
			cur.execute("SELECT 1;")
			print("Conexión OK. Resultado SELECT 1 =", cur.fetchone()[0])
	except Exception as e:
		print("Error de conexión:", e)
		raise
	finally:
		conn.close()

if __name__ == "__main__":
	main()