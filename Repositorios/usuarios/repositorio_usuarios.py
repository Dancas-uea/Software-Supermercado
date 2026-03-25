import bcrypt

from Configuracion.Ajustes.db import cursor_db

ROLES_VALIDOS = {"creador", "gerente", "Admin", "cajero", "inventario"}


def crear_usuario(username: str, password: str, rol: str) -> int:
	"""Crea usuario guardando password_hash (bcrypt)"""
	rol = (rol or "").strip().lower()
	if rol not in ROLES_VALIDOS:
		raise ValueError("Rol inválido")

	password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

	query = """INSERT INTO usuarios (username, password_hash, rol) VALUES (%s, %s, %s) RETURNING id;"""
	with cursor_db() as cur:
		cur.execute(query, (username, password_hash, rol))
		return cur.fetchone()[0]


def obtener_usuario_por_username(username: str):
	query = "SELECT id, username, password_hash, rol FROM usuarios WHERE username = %s;"
	with cursor_db() as cur:
		cur.execute(query, (username,))
		return cur.fetchone()  # None si no existe


def listar_usuarios():
	query = """
		SELECT id, username, rol, fecha_creacion
		FROM usuarios
		ORDER BY id ASC;
	"""
	with cursor_db() as cur:
		cur.execute(query)
		return cur.fetchall()


def eliminar_usuario(username: str) -> int:
	query = "DELETE FROM usuarios WHERE username = %s;"
	with cursor_db() as cur:
		cur.execute(query, (username,))
		return cur.rowcount


def cambiar_password(username: str, new_password: str) -> int:
	password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
	query = "UPDATE usuarios SET password_hash = %s WHERE username = %s;"
	with cursor_db() as cur:
		cur.execute(query, (password_hash, username))
		return cur.rowcount


def actualizar_rol(username: str, rol: str) -> int:
	rol = (rol or "").strip().lower()
	if rol not in ROLES_VALIDOS:
		raise ValueError("Rol inválido")
	query = "UPDATE usuarios SET rol = %s WHERE username = %s;"
	with cursor_db() as cur:
		cur.execute(query, (rol, username))
		return cur.rowcount