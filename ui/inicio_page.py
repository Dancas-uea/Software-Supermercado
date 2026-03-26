from PySide6.QtWidgets import QWidget, QGraphicsColorizeEffect, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, \
    QLabel, QFrame, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import os


class TarjetaFormal(QPushButton):
    """Clase personalizada para los botones grandes corporativos (Corregida)"""
    def __init__(self, texto, color_hex, icono_path):
        super().__init__()
        self.setText(texto)
        self.setFixedSize(220, 110)
        self.setCursor(Qt.PointingHandCursor)
        self.color_base = color_hex
        self.setIcon(QIcon(icono_path))
        self.setIconSize(QSize(40, 40))

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_hex};
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                text-align: center;
                padding-top: 10px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: #f1f2f6; 
                color: {color_hex};       
                border: none;              
            }}
            QPushButton:pressed {{
                background-color: #dfe4ea;
                padding-top: 12px;
            }}
        """)


import webbrowser # No olvides importar esto al inicio del archivo

class TarjetaNovedad(QFrame):
    def __init__(self, titulo, fecha, descripcion, texto_link=None, url=None):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
                margin-bottom: 5px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 10)

        # Fecha
        lbl_fecha = QLabel(fecha)
        lbl_fecha.setStyleSheet("color: #95a5a6; font-size: 10px; font-weight: bold; border: none;")
        layout.addWidget(lbl_fecha)

        # Título
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setWordWrap(True)
        lbl_titulo.setStyleSheet("color: #2c3e50; font-size: 14px; font-weight: bold; border: none;")
        layout.addWidget(lbl_titulo)

        # Descripción
        lbl_desc = QLabel(descripcion)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #7f8c8d; font-size: 12px; border: none;")
        layout.addWidget(lbl_desc)

        # LINK (Solo se crea si hay texto de link)
        if texto_link and url:
            btn_link = QPushButton(texto_link)
            btn_link.setCursor(Qt.PointingHandCursor)
            btn_link.setStyleSheet("""
                QPushButton {
                    color: #3498db; 
                    font-size: 11px; 
                    font-weight: bold; 
                    border: none; 
                    text-align: left; 
                    background: transparent;
                    padding: 0px;
                    margin-top: 5px;
                }
                QPushButton:hover {
                    color: #2980b9;
                    text-decoration: underline;
                }
            """)
            # Conectamos el clic para abrir la web
            btn_link.clicked.connect(lambda: webbrowser.open(url))
            layout.addWidget(btn_link)


import os
import webbrowser
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QFrame, QScrollArea, QApplication
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class InicioPage(QWidget):
    def __init__(self):
        super().__init__()
        # 1. Fondo gris formal para toda la página
        self.setStyleSheet("background-color: #f5f6fa;")

        # Creamos el layout principal horizontal
        layout = QHBoxLayout(self)

        # AJUSTE DE POSICIÓN: Bajamos el contenido y damos margen derecho
        layout.setContentsMargins(5, 80, 40, 40)
        layout.setSpacing(30)

        # --- CREACIÓN DE CONTENEDORES (Primero se crean, luego se añaden al layout) ---

        # 1. LADO IZQUIERDO (Menú y Tarjetas)
        izq_layout = QVBoxLayout()
        izq_layout.addSpacing(20)  # Espacio extra arriba para bajar el título

        # --- ENCABEZADO CON LOGO ---
        header_main_layout = QHBoxLayout()
        header_main_layout.setAlignment(Qt.AlignLeft)

        lbl_logo_principal = QLabel()
        logo_path = os.path.join("../assets/icons/logo.png")
        lbl_logo_principal.setPixmap(QIcon(logo_path).pixmap(QSize(40, 40)))
        lbl_logo_principal.setStyleSheet("border: none; background: transparent;")

        lbl_titulo_main = QLabel("Menú Principal")
        lbl_titulo_main.setStyleSheet("font-size: 28px; font-weight: bold; color: #2f3640; background: transparent;")

        header_main_layout.addWidget(lbl_logo_principal)
        header_main_layout.addWidget(lbl_titulo_main)
        izq_layout.addLayout(header_main_layout)

        lbl_bienvenida = QLabel("Bienvenido al sistema de gestión AsmoRoot Studio")
        lbl_bienvenida.setStyleSheet("font-size: 14px; color: gray; font-weight: 500; background: transparent;")
        izq_layout.addWidget(lbl_bienvenida)
        izq_layout.addSpacing(25)

        # --- GRID DE TARJETAS ---
        grid = QGridLayout()
        grid.setSpacing(20)

        self.menu_items = {
            "nueva_venta": TarjetaFormal("Nueva Venta", "#27ae60", "../assets/icons/ventas.svg"),
            "productos": TarjetaFormal("Productos", "#008080", "../assets/icons/inventario.svg"),
            "categorias": TarjetaFormal("Categorías", "#00acc1", "../assets/icons/categorias.svg"),
            "registros": TarjetaFormal("Registros", "#2196f3", "../assets/icons/registros.svg"),
            "resumenes": TarjetaFormal("Resúmenes", "#1e88e5", "../assets/icons/resumenes.svg"),
            "ingresar_productos": TarjetaFormal("Ingresar Producto", "#43a047",
                                                "../assets/icons/ingresar producto.svg"),
            "configuracion": TarjetaFormal("Configuración", "#ffb300", "../assets/icons/configuracion.svg")
        }

        grid.addWidget(self.menu_items["nueva_venta"], 0, 0)
        grid.addWidget(self.menu_items["productos"], 0, 1)
        grid.addWidget(self.menu_items["categorias"], 0, 2)
        grid.addWidget(self.menu_items["registros"], 1, 0)
        grid.addWidget(self.menu_items["resumenes"], 1, 1)
        grid.addWidget(self.menu_items["ingresar_productos"], 1, 2)
        grid.addWidget(self.menu_items["configuracion"], 2, 1)

        izq_layout.addLayout(grid)
        izq_layout.addStretch()

        # 2. SECCIÓN DERECHA (Novedades)
        container_novedades = QFrame()
        container_novedades.setFixedWidth(380)
        container_novedades.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #dfe4ea;
                border-radius: 15px;
            }
        """)

        main_nov_layout = QVBoxLayout(container_novedades)
        main_nov_layout.setContentsMargins(15, 20, 15, 20)

        # Encabezado Novedades
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)
        lbl_icono = QLabel()
        icon_path = os.path.join("../assets/icons/campana.svg")
        lbl_icono.setPixmap(QIcon(icon_path).pixmap(QSize(24, 24)))
        lbl_icono.setStyleSheet("border: none; background: transparent;")
        lbl_header = QLabel("Novedades")
        lbl_header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2f3640; border: none; background: transparent;")
        header_layout.addWidget(lbl_icono)
        header_layout.addWidget(lbl_header)
        main_nov_layout.addLayout(header_layout)

        linea_titulo = QFrame()
        linea_titulo.setFixedHeight(2)
        linea_titulo.setStyleSheet("background-color: #f1f2f6; border: none;")
        main_nov_layout.addWidget(linea_titulo)
        main_nov_layout.addSpacing(10)

        # Área de Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.nov_list_layout = QVBoxLayout(scroll_content)
        self.nov_list_layout.setSpacing(10)
        self.nov_list_layout.setAlignment(Qt.AlignTop)

        # Datos de noticias
        mis_noticias = [
            {"titulo": "Encuesta para usuarios", "fecha": "23 MAR 2026",
             "desc": "¿Cómo ha sido tu experiencia con AsmoRoot Studio? Ayúdanos a mejorar.",
             "link_txt": "Contestar encuesta aquí...", "url": "https://google.com"},
            {"titulo": "Nueva Versión 1.4.0", "fecha": "25 MAR 2026",
             "desc": "Se optimizaron las animaciones de las tarjetas y se corrigió el error de iconos.",
             "link_txt": "Ver notas de actualización", "url": "https://github.com"},
            {"titulo": "Aviso de Mantenimiento", "fecha": "10 MAR 2026",
             "desc": "El servidor de base de datos estará en mantenimiento el domingo.", "link_txt": None, "url": None}
        ]

        for n in mis_noticias:
            noticia = TarjetaNovedad(n["titulo"], n["fecha"], n["desc"], n.get("link_txt"), n.get("url"))
            self.nov_list_layout.addWidget(noticia)

        scroll.setWidget(scroll_content)
        main_nov_layout.addWidget(scroll)

        # --- ENSAMBLAJE FINAL PARA MOVER A LA IZQUIERDA ---

        # 1. Quitamos el Stretch del principio o lo ponemos con valor 0
        layout.addSpacing(60)  # Un pequeño margen fijo para que no toque el borde físico

        # 2. Añadimos el Menú (ahora aparecerá primero a la izquierda)
        layout.addLayout(izq_layout, 3)

        # 3. Añadimos el Stretch AQUÍ (Esto empujará el menú a la izquierda y las novedades a la derecha)
        layout.addStretch(1)  # <-- Este espacio vacío ahora queda en el centro

        # 4. Espacio y Novedades
        layout.addSpacing(50)
        layout.addWidget(container_novedades, 1)

        # 5. Margen final
        layout.addSpacing(20)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ventana_prueba = InicioPage()
    ventana_prueba.resize(1200, 800)
    ventana_prueba.show()
    sys.exit(app.exec())
