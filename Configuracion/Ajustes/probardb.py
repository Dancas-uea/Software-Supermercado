import sys
from pathlib import Path

# Permite importar el proyecto cuando ejecutas este script directamente
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
sys.path.append(str(RAIZ_PROYECTO))

from Configuracion.Ajustes.db import cursor_db


def main():
	with cursor_db() as cur:
		cur.execute("SELECT current_database();")
		bd = cur.fetchone()[0]

		cur.execute("SELECT current_user;")
		usuario = cur.fetchone()[0]

	print("BD actual:", bd)
	print("Usuario actual:", usuario)


if __name__ == "__main__":
	main()