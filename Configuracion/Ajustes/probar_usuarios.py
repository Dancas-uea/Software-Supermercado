import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
sys.path.append(str(RAIZ_PROYECTO))

from Logica.servicios.Servicios_usuarios.auth_usuarios import registrar_usuario, login


def main():
	username = "creador"
	password = "1234"
	rol = "creador"

	print("--- Registro ---")
	try:
		user_id = registrar_usuario(username=username, password=password, rol=rol)
		print("Usuario creado con id =", user_id)
	except Exception as e:
		print("No se pudo crear (posible usuario duplicado):", e)

	print("\n--- Login OK ---")
	sesion = login(username=username, password=password)
	print("Resultado:", sesion)

	print("\n--- Login FAIL (clave incorrecta) ---")
	sesion_fail = login(username=username, password="mala_clave")
	print("Resultado:", sesion_fail)


if __name__ == "__main__":
	main()