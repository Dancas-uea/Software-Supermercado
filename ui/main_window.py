from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt
from ui.usuarios_windows import UsuariosWindow


class MainWindow(QMainWindow):
    def __init__(self, sesion: dict):
        super().__init__()
        self.setWindowTitle("Supermarket - Sistema de Gestión")
        self.resize(1100, 700)

        self.usuario_actual = sesion

        # ------- WIDGET CENTRAL ----------- #
        central = QWidget()
        central.setStyleSheet("background-color: #f8f9fa;")
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # 1. FABRICACIÓN DEL NAVBAR
        self.navbar = QWidget()
        self.navbar.setFixedHeight(55)
        self.navbar.setStyleSheet("""
            QWidget {
                background-color: #ffffff; 
                border-bottom: 1px solid #dcdde1;
            }
       """)

        navbar_layout = QHBoxLayout(self.navbar)
        navbar_layout.setContentsMargins(20, 0, 20, 0)
        navbar_layout.setSpacing(5) # Espacio entre botones del nav

        # Estilo formal único para todos los botones del Navbar
        estilo_nav = """
            QPushButton {
                border: none;
                background-color: transparent;
                color: #2f3640;
                font-family: 'Segoe UI', Arial;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f1f2f6;
                color: #3498db;
            }
        """

        # --- DICCIONARIO DE BOTONES (Para no repetir código) ---
        # Creamos los botones en una lista para procesarlos todos de golpe
        self.nav_buttons = {
            "inicio": QPushButton("Inicio"),
            "productos": QPushButton("Productos"),
            "venta": QPushButton("Venta"),
            "registro": QPushButton("Registro"),
            "resumenes": QPushButton("Resúmenes"),
            "config": QPushButton("Configuración"),
            "ayuda": QPushButton("Ayuda"),
            "contacto": QPushButton("Contacto")
        }

        # Aplicamos estilo y agregamos al layout automáticamente
        for clave, btn in self.nav_buttons.items():
            btn.setStyleSheet(estilo_nav)
            btn.setCursor(Qt.PointingHandCursor)
            navbar_layout.addWidget(btn)

        navbar_layout.addStretch()
        layout_principal.addWidget(self.navbar)

        # 2. CONTENIDO INFERIOR
        cuerpo_sistema = QWidget()
        root = QHBoxLayout(cuerpo_sistema)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(15)
        layout_principal.addWidget(cuerpo_sistema)

        # --- MENÚ LATERAL ---
        menu_container = QWidget()
        menu = QVBoxLayout(menu_container)
        menu.setSpacing(10)
        menu.setContentsMargins(0, 0, 0, 0)

        lbl_user = QLabel(f"<b>Usuario:</b> {sesion['username']}\n<b>Rol:</b> {sesion['rol']}")
        lbl_user.setStyleSheet("""
          padding: 15px; 
          background-color: #2f3640; 
          color: white; 
          border-radius: 8px;
          font-size: 12px;
       """)
        menu.addWidget(lbl_user)

        estilo_menu_lateral = """
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #dcdde1;
                color: #2f3640;
                padding: 12px;
                border-radius: 6px;
                text-align: left;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3498db;
                color: white;
            }
       """

        self.btn_ventas = QPushButton("Ventas")
        self.btn_inventario = QPushButton("Inventario")
        self.btn_usuarios = QPushButton("Usuarios")
        self.btn_categorias = QPushButton("Categorías")
        self.btn_salir = QPushButton("Cerrar sesión")

        for btn in [self.btn_ventas, self.btn_inventario, self.btn_usuarios, self.btn_categorias, self.btn_salir]:
            btn.setStyleSheet(estilo_menu_lateral)
            btn.setCursor(Qt.PointingHandCursor)
            menu.addWidget(btn)

        menu.addStretch(1)
        root.addWidget(menu_container, 1)

        # --- STACK DE PANTALLAS ---
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #ffffff; border-radius: 8px; border: 1px solid #dcdde1;")
        root.addWidget(self.stack, 4)

        # Creación de Páginas
        self.page_ventas = QLabel("Pantalla: Ventas")
        self.page_inventario = QLabel("Pantalla: Inventario")
        self.page_categorias = QLabel("Pantalla: Categorías")
        self.page_usuarios = UsuariosWindow(self.usuario_actual)

        for p in [self.page_ventas, self.page_inventario, self.page_categorias]:
            p.setAlignment(Qt.AlignCenter)

        self.stack.addWidget(self.page_ventas)     # Index 0
        self.stack.addWidget(self.page_inventario) # Index 1
        self.stack.addWidget(self.page_usuarios)   # Index 2
        self.stack.addWidget(self.page_categorias) # Index 3

        # --- CONEXIONES ---
        # Conexiones Menú Lateral
        self.btn_ventas.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_ventas))
        self.btn_inventario.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_inventario))
        self.btn_usuarios.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_usuarios))
        self.btn_categorias.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_categorias))
        self.btn_salir.clicked.connect(self.cerrar_sesion)

        # Conexiones Navbar (Acceso rápido)
        self.nav_buttons["inicio"].clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.nav_buttons["productos"].clicked.connect(lambda: self.stack.setCurrentWidget(self.page_inventario))
        self.nav_buttons["venta"].clicked.connect(lambda: self.stack.setCurrentWidget(self.page_ventas))

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

    def cerrar_sesion(self):
        confirmacion = QMessageBox.question(
            self, "Cerrar Sesión", "¿Estás seguro de que quieres salir?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmacion == QMessageBox.Yes:
            self.close()