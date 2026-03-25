import psycopg2
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.params = {
            "host": "localhost",
            "database": "Supermarket",
            "user": "postgres",
            "password": "TU_CONTRASEÑA",  # <--- Pon tu clave real aquí
            "port": "5432"
        }

    def _conectar(self):
        return psycopg2.connect(**self.params)

    # === ESTA ES LA FUNCIÓN QUE TE FALTA ===
    def verificar_usuario(self, username, password):
        """Busca al usuario para el Login."""
        conn = None
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            # Buscamos el ID, el nombre y el ROL
            query = "SELECT id, username, rol FROM usuarios WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone()  # Devuelve (id, nombre, rol) o None
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return None
        finally:
            if conn: conn.close()

    # --- SECCIÓN: DASHBOARD (Para que no de error al abrir) ---
    def obtener_resumen_ventas(self):
        conn = None
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            hoy = datetime.now().date()
            cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE DATE(fecha_venta) = %s", (hoy,))
            total_hoy = cursor.fetchone()[0]

            cursor.execute("""
                           SELECT p.nombre, SUM(dv.cantidad) as cant
                           FROM detalle_ventas dv
                                    JOIN productos p ON dv.producto_id = p.id
                           GROUP BY p.nombre
                           ORDER BY cant DESC LIMIT 5
                           """)
            top = cursor.fetchall()
            return {'total_hoy': float(total_hoy), 'top_productos': top}
        except:
            return {'total_hoy': 0.0, 'top_productos': []}
        finally:
            if conn: conn.close()

    def listar_inventario_tabla(self):
        conn = None
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo_barras, nombre, precio_venta, stock FROM productos")
            return cursor.fetchall()
        finally:
            if conn: conn.close()