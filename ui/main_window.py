from PySide6.QtWidgets import (
	QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
	QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt

from ui.usuarios_windows import UsuariosWindow


class MainWindow(QMainWindow):
	def __init__(self, sesion: dict):
		super().__init__()
		self.setWindowTitle("Supermarket")
		self.resize(1000, 600)

		self.usuario_actual = sesion  # {id, username, rol}

		central = QWidget()
		self.setCentralWidget(central)
		root = QHBoxLayout(central)

		menu = QVBoxLayout()
		menu.setSpacing(10)

		lbl_user = QLabel(f"<b>Usuario:</b> {sesion['username']}\n<b>Rol:</b> {sesion['rol']}")
		lbl_user.setStyleSheet(
			"padding: 10px; background-color: #2c3e50; color: white; border-radius: 5px;"
		)
		menu.addWidget(lbl_user)

		self.btn_ventas = QPushButton("Ventas")
		self.btn_inventario = QPushButton("Inventario")
		self.btn_usuarios = QPushButton("Usuarios")
		self.btn_salir = QPushButton("Cerrar sesión")

		menu.addWidget(self.btn_ventas)
		menu.addWidget(self.btn_inventario)
		menu.addWidget(self.btn_usuarios)
		menu.addStretch(1)
		menu.addWidget(self.btn_salir)

		root.addLayout(menu, 1)

		self.stack = QStackedWidget()
		root.addWidget(self.stack, 4)

		self.page_ventas = QLabel("Pantalla: Ventas")
		self.page_ventas.setAlignment(Qt.AlignCenter)

		self.page_inventario = QLabel("Pantalla: Inventario")
		self.page_inventario.setAlignment(Qt.AlignCenter)

		self.page_usuarios = UsuariosWindow(self.usuario_actual)

		self.stack.addWidget(self.page_ventas)
		self.stack.addWidget(self.page_inventario)
		self.stack.addWidget(self.page_usuarios)

		self.btn_ventas.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_ventas))
		self.btn_inventario.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_inventario))
		self.btn_usuarios.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_usuarios))
		self.btn_salir.clicked.connect(self.cerrar_sesion)

		self.aplicar_permisos()

	def aplicar_permisos(self):
		rol = (self.usuario_actual.get("rol") or "").strip().lower()

		if rol in ("creador", "admin"):
			return

		elif rol == "cajero":
			self.btn_usuarios.setVisible(False)
			self.stack.setCurrentWidget(self.page_ventas)

		elif rol == "inventario":
			self.btn_ventas.setVisible(False)
			self.btn_usuarios.setVisible(False)
			self.stack.setCurrentWidget(self.page_inventario)

		elif rol == "gerente":
			self.btn_usuarios.setVisible(False)

		else:
			QMessageBox.warning(self, "Acceso", f"El rol '{rol}' tiene acceso limitado.")

	def cerrar_sesion(self):
		confirmacion = QMessageBox.question(
			self, "Cerrar Sesión", "¿Estás seguro de que quieres salir?",
			QMessageBox.Yes | QMessageBox.No
		)
		if confirmacion == QMessageBox.Yes:
			self.close()