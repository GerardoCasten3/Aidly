import psycopg2 as pg

# Función para conectarse a la base de datos
def connect():
    try:
        conn = pg.connect(
        host="localhost",
        user="postgres",
        password="Casten4all_",
        database="Dtech")
        return conn
    except Exception as e:
        print("No se logró conectar, error: ", e)

# Función para desconectarse de la base de datos
def disconnect(conn):
    conn.close()

# Función para obtener los pedidos
def get_orders():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT p.id_pedido as ID_PEDIDO, a.descripcion_producto AS DESCRIPCION, e.descripcion_estado AS ESTADO, c.nombre_cliente AS CLIENTE, p.guia_pedido AS GUIA FROM pedidos p, clientes c, estado_pedido e, productos a WHERE p.id_producto = a.id_producto AND p.id_cliente = c.id_cliente AND p.id_estado = e.id_estado"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        print(f"ID_PEDIDO: {row[0]}, DESCRIPCION: {row[1]}, ESTADO: {row[2]}, CLIENTE: {row[3]}, GUIA: {row[4]}")
    disconnect(conn)

# Función para obtener los datos de un pedido
def get_data_orders(id_pedido):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT p.id_pedido as ID_PEDIDO, e.descripcion_estado AS ESTADO, c.nombre_cliente AS CLIENTE, p.guia_pedido AS GUIA FROM pedidos p, clientes c, estado_pedido e, productos a WHERE p.id_producto = a.id_producto AND p.id_cliente = c.id_cliente AND p.id_estado = e.id_estado AND p.id_pedido = {id_pedido}"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        lista = list(row)
    disconnect(conn)
    return (f"Hola {lista[2]}, tu pedido con ID {lista[0]} se encuentra en estado {lista[1]} y su guía es {lista[3]}, puedes consultar más detalles en 'https://www.dhl.com/mx-es/home/rastreo.html'")
    

