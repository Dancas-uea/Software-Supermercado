import bcrypt

from Repositorios.usuarios.repositorio_usuarios import (
	crear_usuario,
	obtener_usuario_por_username,
)

ROLES_VALIDOS = {"creador", "gerente", "admin", "cajero", "inventario"}


def registrar_usuario(username: str, password: str, rol: str) -> int:
	"""Registra usuario. (El repo es quien genera bcrypt)"""
	rol = (rol or "").strip().lower()
	if rol not in ROLES_VALIDOS:
		raise ValueError("Rol inválido")

	return crear_usuario(username=username, password=password, rol=rol)


def login(username: str, password: str):
	fila = obtener_usuario_por_username(username)
	if not fila:
		return None

	id_, user_, password_hash, rol = fila

	# Evitar que el programa se caiga si el usuario fue guardado mal (texto plano, HASH_DEV, etc.)
	if not password_hash or not str(password_hash).startswith("$2"):
		return None

	try:
		ok = bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
	except ValueError:
		return None

	if not ok:
		return None

	return {"id": id_, "username": user_, "rol": rol}