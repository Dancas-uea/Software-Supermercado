from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QInputDialog, QLineEdit, QLabel
)
from PySide6.QtCore import Qt

from Repositorios.usuarios.repositorio_usuarios import (
    listar_usuarios, crear_usuario, eliminar_usuario,
    cambiar_password, actualizar_rol)


class UsuariosWindow(QWidget):
    def __init__(self, sesion: dict):
        super().__init__()
        self.sesion = sesion or {}

        self.setWindowTitle("Usuarios")
        self.setMinimumWidth(700)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        lbl = QLabel(f"Usuarios — sesión: {self.sesion.get('username')} ({self.sesion.get('rol')})")
        layout.addWidget(lbl)

        btns = QHBoxLayout()
        self.btn_refrescar = QPushButton("Refrescar")
        self.btn_agregar = QPushButton("Agregar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_password = QPushButton("Cambiar clave")
        self.btn_rol = QPushButton("Cambiar rol")

        btns.addWidget(self.btn_refrescar)
        btns.addWidget(self.btn_agregar)
        btns.addWidget(self.btn_eliminar)
        btns.addWidget(self.btn_password)
        btns.addWidget(self.btn_rol)
        layout.addLayout(btns)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["id", "username", "rol", "fecha_creacion"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.btn_refrescar.clicked.connect(self.cargar)
        self.btn_agregar.clicked.connect(self.on_agregar)
        self.btn_eliminar.clicked.connect(self.on_eliminar)
        self.btn_password.clicked.connect(self.on_cambiar_password)
        self.btn_rol.clicked.connect(self.on_cambiar_rol)

        self.aplicar_permisos()
        self.cargar()

    def aplicar_permisos(self):
        rol = (self.sesion.get("rol") or "").lower()
        permitidos = {"admin", "gerente", "creador"}
        puede = rol in permitidos
        self.btn_agregar.setEnabled(puede)
        self.btn_eliminar.setEnabled(puede)
        self.btn_password.setEnabled(puede)
        self.btn_rol.setEnabled(puede)

    def cargar(self):
        try:
            rows = listar_usuarios()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", str(e))
            return

        self.table.setRowCount(0)
        for r in rows:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for c, val in enumerate(r):
                item = QTableWidgetItem("" if val is None else str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_idx, c, item)

    def _get_selected_username(self):
        sel = self.table.selectionModel().selectedRows()
        if not sel:
            return None
        row = sel[0].row()
        item = self.table.item(row, 1)
        return item.text() if item else None

    def on_agregar(self):
        username, ok = QInputDialog.getText(self, "Nuevo usuario", "Username:")
        if not ok or not username.strip():
            return

        password, ok = QInputDialog.getText(self, "Nuevo usuario", "Password:", QLineEdit.Password)
        if not ok or not password:
            return

        rol, ok = QInputDialog.getItem(
            self, "Nuevo usuario", "Rol:",
            ["cajero", "inventario", "admin", "gerente", "creador"], 0, False
        )
        if not ok or not rol:
            return

        try:
            crear_usuario(username=username.strip(), password=password, rol=rol)
            QMessageBox.information(self, "OK", "Usuario creado")
            self.cargar()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_eliminar(self):
        username = self._get_selected_username()
        if not username:
            QMessageBox.warning(self, "Atención", "Selecciona un usuario")
            return

        if username == self.sesion.get("username"):
            QMessageBox.warning(self, "Atención", "No puedes eliminar tu usuario activo")
            return

        resp = QMessageBox.question(self, "Confirmar", f"¿Eliminar '{username}'?")
        if resp != QMessageBox.Yes:
            return

        try:
            n = eliminar_usuario(username=username)
            QMessageBox.information(self, "OK", "Usuario eliminado" if n else "No se eliminó")
            self.cargar()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_cambiar_password(self):
        username = self._get_selected_username()
        if not username:
            QMessageBox.warning(self, "Atención", "Selecciona un usuario")
            return

        new_pass, ok = QInputDialog.getText(
            self, "Cambiar clave", f"Nueva clave para {username}:", QLineEdit.Password
        )
        if not ok or not new_pass:
            return

        try:
            n = cambiar_password(username=username, new_password=new_pass)
            QMessageBox.information(self, "OK", "Clave actualizada" if n else "No se actualizó")
            self.cargar()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_cambiar_rol(self):
        username = self._get_selected_username()
        if not username:
            QMessageBox.warning(self, "Atención", "Selecciona un usuario")
            return

        rol, ok = QInputDialog.getItem(
            self, "Cambiar rol", f"Nuevo rol para {username}:",
            ["cajero", "inventario", "admin", "gerente", "creador"], 0, False
        )
        if not ok or not rol:
            return

        try:
            n = actualizar_rol(username=username, rol=rol)
            QMessageBox.information(self, "OK", "Rol actualizado" if n else "No se actualizó")
            self.cargar()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
