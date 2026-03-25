from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt

# Importamos la lógica y la ventana principal
from Logica.servicios.Servicios_usuarios.auth_usuarios import login
from ui.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Supermarket")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        # ---------- Lógica de Diseño Centrado ---------- #

        # Layout principal que abarca toda la ventana
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(100, 50, 100, 50)
        layout_principal.setAlignment(Qt.AlignCenter)

        # Contenedor vertical para los elementos del formulario
        self.form_container = QVBoxLayout()
        self.form_container.setSpacing(15)

        # Título
        self.lbl_title = QLabel("Iniciar sesión")  # Lo definimos como self.lbl_title
        self.lbl_title.setAlignment(Qt.AlignCenter)
        # Aplicamos un estilo rápido para que resalte
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00D1FF;")
        self.form_container.addWidget(self.lbl_title)

        # Input Usuario
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Usuario")
        self.input_user.setMinimumHeight(35)  # Un poco más alto para que sea fácil clickear
        self.form_container.addWidget(self.input_user)

        # Input Contraseña
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setMinimumHeight(35)
        self.form_container.addWidget(self.input_pass)

        # Botón Entrar
        self.btn = QPushButton("Entrar")
        self.btn.setMinimumHeight(40)
        self.btn.clicked.connect(self.on_login)
        self.form_container.addWidget(self.btn)

        # Agregamos el contenedor del formulario al layout principal centrado
        layout_principal.addLayout(self.form_container)

        # Conexiones adicionales
        self.input_pass.returnPressed.connect(self.on_login)
        self.main = None

    def on_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text()

        if not username or not password:
            QMessageBox.warning(self, "Faltan datos", "Ingresa usuario y contraseña")
            return

        # Llamada a tu lógica de autenticación
        sesion = login(username=username, password=password)

        if not sesion:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrecta")
            return

        # Si el login es exitoso, abrimos la MainWindow
        self.main = MainWindow(sesion)
        self.main.show()
        self.close()