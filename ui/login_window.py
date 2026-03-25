from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt

# Importamos la lógica y la ventana principal
from Logica.servicios.Servicios_usuarios.auth_usuarios import login
from ui.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acceso al Sistema - Supermarket")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        # --- FONDO DE LA VENTANA ---
        self.setStyleSheet("background-color: #f8f9fa;")  # Gris muy claro formal

        # ---------- Lógica de Diseño Centrado ---------- #
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(100, 50, 100, 50)
        layout_principal.setAlignment(Qt.AlignCenter)

        # Contenedor del formulario con estilo de "Tarjeta" blanca
        self.container_widget = QWidget()
        self.container_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #dcdde1;
                border-radius: 10px;
            }
        """)

        self.form_container = QVBoxLayout(self.container_widget)
        self.form_container.setContentsMargins(30, 40, 30, 40)
        self.form_container.setSpacing(15)

        # Título Formal
        self.lbl_title = QLabel("Iniciar sesión")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("""
            font-size: 22px; 
            font-weight: bold; 
            color: #2f3640; 
            border: none;
            margin-bottom: 10px;
        """)
        self.form_container.addWidget(self.lbl_title)

        # Estilo para los campos de texto (Inputs)
        estilo_inputs = """
            QLineEdit {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 8px;
                background-color: #ffffff;
                color: #2f3640;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """

        # Input Usuario
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Nombre de usuario")
        self.input_user.setMinimumHeight(40)
        self.input_user.setStyleSheet(estilo_inputs)
        self.form_container.addWidget(self.input_user)

        # Input Contraseña
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setMinimumHeight(40)
        self.input_pass.setStyleSheet(estilo_inputs)
        self.form_container.addWidget(self.input_pass)

        # Botón Entrar (Azul Corporativo)
        self.btn = QPushButton("Acceder")
        self.btn.setMinimumHeight(45)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """)
        self.btn.clicked.connect(self.on_login)
        self.form_container.addWidget(self.btn)

        # Agregamos la "tarjeta" al layout principal
        layout_principal.addWidget(self.container_widget)

        # Conexiones adicionales
        self.input_pass.returnPressed.connect(self.on_login)
        self.main = None

    def on_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text()

        if not username or not password:
            QMessageBox.warning(self, "Faltan datos", "Por favor, ingresa tus credenciales.")
            return

        sesion = login(username=username, password=password)

        if not sesion:
            QMessageBox.warning(self, "Error de acceso", "Usuario o contraseña incorrectos.")
            return

        self.main = MainWindow(sesion)
        self.main.show()
        self.close()