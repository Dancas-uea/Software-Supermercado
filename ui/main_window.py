from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QMessageBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import os

# Importamos tus clases personalizadas
from ui.usuarios_windows import UsuariosWindow
from ui.inicio_page import InicioPage


class MainWindow(QMainWindow):
    def __init__(self, sesion: dict):
        super().__init__()
        self.setWindowTitle("AsmoRoot Studio - Sistema de Gestión")
        self.resize(1200, 800)
        self.usuario_actual = sesion

        # --- WIDGET CENTRAL ÚNICO ---
        central = QWidget()
        central.setStyleSheet("background-color: #f8f9fa;")
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # 1. NAVBAR SUPERIOR (Ahora incluye Cerrar Sesión)
        self.navbar = QWidget()
        self.navbar.setFixedHeight(55)
        self.navbar.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #dcdde1;")

        navbar_layout = QHBoxLayout(self.navbar)
        navbar_layout.setContentsMargins(20, 0, 20, 0)
        navbar_layout.setSpacing(5)

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

        self.nav_buttons = {
            "inicio": QPushButton("Inicio"),
            "productos": QPushButton("Productos"),
            "venta": QPushButton("Venta"),
            "registro": QPushButton("Registro"),
            "resumenes": QPushButton("Resúmenes"),
            "config": QPushButton("Configuración"),
            "salir": QPushButton("Cerrar Sesión")  # Reubicado aquí
        }

        for clave, btn in self.nav_buttons.items():
            btn.setStyleSheet(estilo_nav)
            btn.setCursor(Qt.PointingHandCursor)
            # Estilo especial para el botón de salir
            if clave == "salir":
                btn.setStyleSheet(estilo_nav + "QPushButton { color: #e74c3c; } QPushButton:hover { color: #c0392b; }")
            navbar_layout.addWidget(btn)

        navbar_layout.addStretch()

        # Etiqueta de usuario en el Navbar (Sustituye la imagen 2 del lateral)
        lbl_user_nav = QLabel(f"👤 {sesion['username']} ({sesion['rol']})")
        lbl_user_nav.setStyleSheet("color: #7f8c8d; font-size: 12px; font-weight: bold; margin-right: 10px;")
        navbar_layout.addWidget(lbl_user_nav)

        layout_principal.addWidget(self.navbar)

        # 2. CUERPO DEL SISTEMA (Sin Menú Lateral)
        cuerpo_sistema = QWidget()
        root = QHBoxLayout(cuerpo_sistema)
        root.setContentsMargins(0, 0, 0, 0)  # Eliminamos márgenes para que sea pantalla completa
        root.setSpacing(0)
        layout_principal.addWidget(cuerpo_sistema)

        # --- STACK DE PANTALLAS ---
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #ffffff; border: none;")
        root.addWidget(self.stack)

        # --- CREACIÓN DE PÁGINAS ---
        self.page_inicio = InicioPage(self.usuario_actual)
        self.page_ventas = QLabel("Pantalla: Ventas")
        self.page_inventario = QLabel("Pantalla: Inventario")
        self.page_categorias = QLabel("Pantalla: Categorías")
        self.page_usuarios = UsuariosWindow(self.usuario_actual)

        # Estilo temporal para páginas no desarrolladas
        for p in [self.page_ventas, self.page_inventario, self.page_categorias]:
            p.setAlignment(Qt.AlignCenter)
            p.setStyleSheet("font-size: 24px; color: gray; background-color: white;")

        # AGREGAR AL STACK
        self.stack.addWidget(self.page_inicio)  # Index 0
        self.stack.addWidget(self.page_ventas)  # Index 1
        self.stack.addWidget(self.page_inventario)  # Index 2
        self.stack.addWidget(self.page_usuarios)  # Index 3
        self.stack.addWidget(self.page_categorias)  # Index 4

        # --- CONEXIONES ---

        # Conexión de las TARJETAS de InicioPage
        self.page_inicio.menu_items["nueva_venta"].clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_ventas))
        self.page_inicio.menu_items["productos"].clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_inventario))
        self.page_inicio.menu_items["categorias"].clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_categorias))
        self.page_inicio.menu_items["usuarios"].clicked.connect(lambda: self.stack.setCurrentWidget(self.page_usuarios))

        # Conexiones Navbar
        self.nav_buttons["inicio"].clicked.connect(lambda: self.stack.setCurrentWidget(self.page_inicio))
        self.nav_buttons["productos"].clicked.connect(lambda: self.stack.setCurrentWidget(self.page_inventario))
        self.nav_buttons["venta"].clicked.connect(lambda: self.stack.setCurrentWidget(self.page_ventas))
        self.nav_buttons["salir"].clicked.connect(self.cerrar_sesion)

        self.aplicar_permisos()

    def aplicar_permisos(self):
        # Como las tarjetas ya se ocultan en InicioPage, aquí solo aseguramos
        # que si un cajero entra, no sea redirigido a una página prohibida.
        rol = (self.usuario_actual.get("rol") or "").strip().lower()
        if rol not in ("creador", "admin"):
            if self.stack.currentWidget() == self.page_usuarios:
                self.stack.setCurrentWidget(self.page_inicio)

    def cerrar_sesion(self):
        confirmacion = QMessageBox.question(
            self, "Cerrar Sesión", "¿Estás seguro de que quieres salir del sistema?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmacion == QMessageBox.Yes:
            self.close()