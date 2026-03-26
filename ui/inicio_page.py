import os
import webbrowser
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QFrame, QScrollArea, QApplication
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class TarjetaFormal(QPushButton):
    """Clase personalizada para los botones grandes corporativos (Corregida)"""

    def __init__(self, texto, color_hex, icono_path):
        super().__init__()
        self.setText(texto)
        self.setFixedSize(220, 110)
        self.setCursor(Qt.PointingHandCursor)
        self.color_base = color_hex

        # Manejo de iconos (asegurando que la ruta exista)
        if os.path.exists(icono_path):
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

        # LINK
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
            btn_link.clicked.connect(lambda: webbrowser.open(url))
            layout.addWidget(btn_link)


class InicioPage(QWidget):
    def __init__(self, sesion: dict = None):  # Recibe la sesión para los permisos
        super().__init__()
        self.setStyleSheet("background-color: #f5f6fa;")

        # Si no se pasa sesión (para pruebas), creamos una por defecto
        self.usuario_actual = sesion if sesion else {"username": "Invitado", "rol": "cajero"}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 80, 40, 40)
        layout.setSpacing(30)

        # 1. LADO IZQUIERDO (Menú y Tarjetas)
        izq_layout = QVBoxLayout()
        izq_layout.addSpacing(20)

        # --- ENCABEZADO CON LOGO ---
        header_main_layout = QHBoxLayout()
        header_main_layout.setAlignment(Qt.AlignLeft)

        lbl_logo_principal = QLabel()
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/icons/logo.png"))
        if os.path.exists(logo_path):
            lbl_logo_principal.setPixmap(QIcon(logo_path).pixmap(QSize(40, 40)))

        lbl_logo_principal.setStyleSheet("border: none; background: transparent;")

        lbl_titulo_main = QLabel("Menú Principal")
        lbl_titulo_main.setStyleSheet("font-size: 28px; font-weight: bold; color: #2f3640; background: transparent;")

        header_main_layout.addWidget(lbl_logo_principal)
        header_main_layout.addWidget(lbl_titulo_main)
        izq_layout.addLayout(header_main_layout)

        # Mensaje de bienvenida personalizado
        lbl_bienvenida = QLabel(f"Bienvenido al sistema de gestión AsmoRoot Studio")
        lbl_bienvenida.setStyleSheet("font-size: 14px; color: gray; font-weight: 500; background: transparent;")
        izq_layout.addWidget(lbl_bienvenida)
        izq_layout.addSpacing(25)

        # --- GRID DE TARJETAS ---
        grid = QGridLayout()
        grid.setSpacing(20)

        # Calculamos la ruta base una sola vez para no repetir código
        base_path = os.path.dirname(os.path.abspath(__file__))

        self.menu_items = {
            "nueva_venta": TarjetaFormal("Nueva Venta", "#27ae60",
                                         os.path.join(base_path, "../assets/icons/ventas.svg")),
            "productos": TarjetaFormal("Productos", "#008080",
                                       os.path.join(base_path, "../assets/icons/inventario.svg")),
            "categorias": TarjetaFormal("Categorías", "#00acc1",
                                        os.path.join(base_path, "../assets/icons/categorias.svg")),
            "usuarios": TarjetaFormal("Usuarios", "#00acc1", os.path.join(base_path, "../assets/icons/usuarios.svg")),
            "registros": TarjetaFormal("Registros", "#2196f3",
                                       os.path.join(base_path, "../assets/icons/registros.svg")),
            "resumenes": TarjetaFormal("Resúmenes", "#1e88e5",
                                       os.path.join(base_path, "../assets/icons/resumenes.svg")),
            "ingresar_productos": TarjetaFormal("Ingresar Producto", "#43a047",
                                                os.path.join(base_path, "../assets/icons/ingresar producto.svg")),
            "configuracion": TarjetaFormal("Configuración", "#ffb300",
                                           os.path.join(base_path, "../assets/icons/configuracion.svg"))
        }

        # --- LÓGICA DE PERMISOS ---
        rol = self.usuario_actual.get("rol", "").lower()
        if rol not in ["creador", "admin"]:
            self.menu_items["usuarios"].hide()

        if rol == "cajero":
            self.menu_items["configuracion"].hide()

        # --- ACOMODO DEL GRID ---
        grid.addWidget(self.menu_items["nueva_venta"], 0, 0)
        grid.addWidget(self.menu_items["productos"], 0, 1)
        grid.addWidget(self.menu_items["categorias"], 0, 2)
        grid.addWidget(self.menu_items["usuarios"], 1, 0)
        grid.addWidget(self.menu_items["registros"], 1, 1)
        grid.addWidget(self.menu_items["resumenes"], 1, 2)
        grid.addWidget(self.menu_items["ingresar_productos"], 2, 0)
        grid.addWidget(self.menu_items["configuracion"], 2, 1)

        izq_layout.addLayout(grid)
        izq_layout.addStretch()

        # 2. SECCIÓN DERECHA (Novedades)
        container_novedades = QFrame()
        container_novedades.setFixedWidth(380)
        container_novedades.setStyleSheet(
            "QFrame { background-color: white; border: 1px solid #dfe4ea; border-radius: 15px; }")

        main_nov_layout = QVBoxLayout(container_novedades)
        main_nov_layout.setContentsMargins(15, 20, 15, 20)

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)

        lbl_icono = QLabel()
        # Se ajusta la ruta para que sea absoluta y se fuerza el renderizado del SVG
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/icons/campana.svg"))
        if os.path.exists(icon_path):
            lbl_icono.setPixmap(QIcon(icon_path).pixmap(QSize(24, 24)))
            lbl_icono.setStyleSheet("border: none; background: transparent;")
            lbl_icono.setScaledContents(True)  # Ajusta el contenido al label
            lbl_icono.setFixedSize(24, 24)  # Fija el tamaño para que no se deforme

        lbl_header = QLabel("Novedades")
        lbl_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2f3640; border: none;")
        header_layout.addWidget(lbl_icono)
        header_layout.addSpacing(10)  # Espacio entre el icono y el texto
        header_layout.addWidget(lbl_header)
        main_nov_layout.addLayout(header_layout)

        linea = QFrame();
        linea.setFixedHeight(2);
        linea.setStyleSheet("background-color: #f1f2f6; border: none;")
        main_nov_layout.addWidget(linea)
        main_nov_layout.addSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.nov_list_layout = QVBoxLayout(scroll_content)
        self.nov_list_layout.setSpacing(10)
        self.nov_list_layout.setAlignment(Qt.AlignTop)

        mis_noticias = [
            {"titulo": "Encuesta para usuarios", "fecha": "23 MAR 2026", "desc": "¿Cómo ha sido tu experiencia?",
             "link_txt": "Contestar aquí...", "url": "https://google.com"},
            {"titulo": "Nueva Versión 1.4.0", "fecha": "25 MAR 2026", "desc": "Optimización de tarjetas.",
             "link_txt": "Ver notas", "url": "https://github.com"},
            {"titulo": "Aviso Mantenimiento", "fecha": "10 MAR 2026", "desc": "Servidor en mantenimiento domingo.",
             "link_txt": None, "url": None}
        ]

        for n in mis_noticias:
            self.nov_list_layout.addWidget(
                TarjetaNovedad(n["titulo"], n["fecha"], n["desc"], n.get("link_txt"), n.get("url")))

        scroll.setWidget(scroll_content)
        main_nov_layout.addWidget(scroll)

        # ENSAMBLAJE FINAL
        layout.addSpacing(60)
        layout.addLayout(izq_layout, 3)
        layout.addStretch(1)
        layout.addSpacing(50)
        layout.addWidget(container_novedades, 1)
        layout.addSpacing(20)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # Prueba con rol admin para ver todas las opciones
    prueba_sesion = {"username": "Carlos", "rol": "admin"}
    ventana = InicioPage(prueba_sesion)
    ventana.resize(1200, 800)
    ventana.show()
    sys.exit(app.exec())