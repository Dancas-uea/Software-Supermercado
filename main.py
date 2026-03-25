import sys
from PySide6.QtWidgets import QApplication

# Ventana de login
from ui.login_window import LoginWindow

# Estilo (opcional)
try:
	from ui.styles import MIDNIGHT_STYLE
except Exception:
	MIDNIGHT_STYLE = None


def main():
	app = QApplication(sys.argv)

	if MIDNIGHT_STYLE:
		app.setStyleSheet(MIDNIGHT_STYLE)

	w = LoginWindow()
	w.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()