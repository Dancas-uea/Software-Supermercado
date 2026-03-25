from dotenv import load_dotenv
import os
import psycopg2
from contextlib import contextmanager
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / "Variables de entorno" / ".env")

def _env(nombre: str) -> str:
	valor = os.getenv(nombre)
	if not valor:
		raise RuntimeError(f"Falta la variable de entorno: {nombre}")
	return valor

def crear_conexion():
	return psycopg2.connect(
		host=_env("DB_HOST"),
		port=_env("DB_PORT"),
		dbname=_env("DB_NAME"),
		user=_env("DB_USER"),
		password=_env("DB_PASSWORD"),
	)

@contextmanager
def cursor_db():
	"""Abre conexión, entrega cursor y asegura commit/rollback + cierre."""
	conn = crear_conexion()
	try:
		cur = conn.cursor()
		yield cur
		conn.commit()
	except Exception:
		conn.rollback()
		raise
	finally:
		try:
			cur.close()
		except Exception:
			pass
		conn.close()

