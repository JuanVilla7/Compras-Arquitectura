ENCABEZADO = ["PRSUC", "PRCOD", "PRFEC", "PRPROV", "PRCANT", "PRPRE"]


def parsear_linea(linea):
    partes = [c.strip() for c in linea.strip().split(",")]

    if len(partes) != 6:
        raise ValueError(f"Fila invalida (se esperaban 6 columnas): {linea!r}")

    sucursal, producto, fecha, proveedor, cantidad_str, precio_str = partes

    if not sucursal or not producto:
        raise ValueError(f"Sucursal o producto vacios: {linea!r}")

    try:
        cantidad = int(cantidad_str)
    except ValueError:
        raise ValueError(f"Cantidad no es un entero: {cantidad_str!r}")

    try:
        precio = float(precio_str)
    except ValueError:
        raise ValueError(f"Precio no es un numero: {precio_str!r}")

    if cantidad < 0:
        raise ValueError(f"Cantidad negativa: {cantidad}")
    if precio < 0:
        raise ValueError(f"Precio negativo: {precio}")

    return {
        "sucursal": sucursal,
        "producto": producto,
        "fecha": fecha,
        "proveedor": proveedor,
        "cantidad": cantidad,
        "precio": precio,
    }


def leer_compras(path_entrada):
    compras = []
    with open(path_entrada, "r", encoding="utf-8") as file:
        for linea in file:
            if not linea.strip():
                continue
            if "PRSUC" in linea:
                continue
            compras.append(parsear_linea(linea))
    return compras


def ordenar_compras(compras):
    datos = list(compras)
    n = len(datos)
    for i in range(n):
        for j in range(0, n - i - 1):
            a = datos[j]
            b = datos[j + 1]
            clave_a = (a["sucursal"], a["producto"], a["fecha"])
            clave_b = (b["sucursal"], b["producto"], b["fecha"])
            if clave_a > clave_b:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
    return datos


def total_por_producto(compras, sucursal, producto):
    unidades = 0
    importe = 0.0
    for c in compras:
        if c["sucursal"] == sucursal and c["producto"] == producto:
            unidades += c["cantidad"]
            importe += c["cantidad"] * c["precio"]
    return {"unidades": unidades, "importe": importe}


def importe_total_general(compras):
    return sum(c["cantidad"] * c["precio"] for c in compras)


def producto_mas_vendido(compras):
    if not compras:
        raise ValueError("No hay compras para analizar")

    unidades_por_producto = {}
    for c in compras:
        unidades_por_producto[c["producto"]] = (
            unidades_por_producto.get(c["producto"], 0) + c["cantidad"]
        )
    return max(unidades_por_producto, key=unidades_por_producto.get)


def resumen_por_sucursal(compras):
    importe_prod = {}
    unidades_suc = {}
    importe_suc = {}

    for c in compras:
        suc = c["sucursal"]
        prod = c["producto"]
        imp = c["cantidad"] * c["precio"]

        importe_prod[(suc, prod)] = importe_prod.get((suc, prod), 0.0) + imp
        unidades_suc[suc] = unidades_suc.get(suc, 0) + c["cantidad"]
        importe_suc[suc] = importe_suc.get(suc, 0.0) + imp

    resumen = {}
    for suc in sorted(unidades_suc):
        productos = {p: i for (s, p), i in importe_prod.items() if s == suc}
        resumen[suc] = {
            "total_unidades": unidades_suc[suc],
            "total_importe": importe_suc[suc],
            "producto_mayor": max(productos, key=productos.get),
            "producto_menor": min(productos, key=productos.get),
        }
    return resumen


def generar_informe(compras):
    lineas = []
    resumen = resumen_por_sucursal(compras)
    for suc, datos in resumen.items():
        lineas.append("-" * 50)
        lineas.append(f"INFORME SUCURSAL {suc}:")
        lineas.append(f"Total Unidades Vendidas: {datos['total_unidades']}")
        lineas.append(f"Producto Mayor Compra: {datos['producto_mayor']}")
        lineas.append(f"Producto Menor Compra: {datos['producto_menor']}")
    lineas.append("=" * 50)
    lineas.append("ESTADISTICA GENERAL DEL SUPERMERCADO")
    lineas.append(f"Total de Sucursales procesadas: {len(resumen)}")
    lineas.append(f"Importe Total General: ${importe_total_general(compras):.2f}")
    lineas.append("=" * 50)
    return "\n".join(lineas)
