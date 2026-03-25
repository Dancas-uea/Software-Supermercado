from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt

from Logica.servicios.Servicios_usuarios.auth_usuarios import login
from ui.main_window import MainWindow


class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Login - Supermarket")
		self.setMinimumWidth(360)

		layout = QVBoxLayout(self)
		layout.setSpacing(10)

		title = QLabel("Iniciar sesión")
		title.setAlignment(Qt.AlignCenter)
		layout.addWidget(title)

		self.input_user = QLineEdit()
		self.input_user.setPlaceholderText("Usuario")
		layout.addWidget(self.input_user)

		self.input_pass = QLineEdit()
		self.input_pass.setPlaceholderText("Contraseña")
		self.input_pass.setEchoMode(QLineEdit.Password)
		layout.addWidget(self.input_pass)

		btn = QPushButton("Entrar")
		btn.clicked.connect(self.on_login)
		layout.addWidget(btn)

		self.input_pass.returnPressed.connect(self.on_login)

		self.main = None

	def on_login(self):
		username = self.input_user.text().strip()
		password = self.input_pass.text()

		if not username or not password:
			QMessageBox.warning(self, "Faltan datos", "Ingresa usuario y contraseña")
			return

		sesion = login(username=username, password=password)
		if not sesion:
			QMessageBox.warning(self, "Error", "Usuario o contraseña incorrecta")
			return

		self.main = MainWindow(sesion)
		self.main.show()
		self.close()