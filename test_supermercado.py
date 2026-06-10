import pytest

from supermercado import (
    parsear_linea,
    ordenar_compras,
    total_por_producto,
    importe_total_general,
    producto_mas_vendido,
    resumen_por_sucursal,
)


COMPRAS_EJEMPLO = [
    {"sucursal": "SUC01", "producto": "P100", "fecha": "2025-01-01",
     "proveedor": "PROV01", "cantidad": 10, "precio": 100.0},
    {"sucursal": "SUC01", "producto": "P100", "fecha": "2025-01-02",
     "proveedor": "PROV02", "cantidad": 5, "precio": 100.0},
    {"sucursal": "SUC01", "producto": "P200", "fecha": "2025-01-01",
     "proveedor": "PROV01", "cantidad": 2, "precio": 50.0},
    {"sucursal": "SUC02", "producto": "P100", "fecha": "2025-01-01",
     "proveedor": "PROV03", "cantidad": 1, "precio": 100.0},
]


def test_total_por_producto():
    resultado = total_por_producto(COMPRAS_EJEMPLO, "SUC01", "P100")
    assert resultado["unidades"] == 15
    assert resultado["importe"] == 1500.0


def test_importe_total_general():
    assert importe_total_general(COMPRAS_EJEMPLO) == 999.99


def test_producto_mas_vendido():
    assert producto_mas_vendido(COMPRAS_EJEMPLO) == "P100"


def test_ordenar_compras():
    desordenado = [
        {"sucursal": "SUC02", "producto": "P100", "fecha": "2025-01-01",
         "proveedor": "X", "cantidad": 1, "precio": 1.0},
        {"sucursal": "SUC01", "producto": "P200", "fecha": "2025-01-01",
         "proveedor": "X", "cantidad": 1, "precio": 1.0},
        {"sucursal": "SUC01", "producto": "P100", "fecha": "2025-01-05",
         "proveedor": "X", "cantidad": 1, "precio": 1.0},
        {"sucursal": "SUC01", "producto": "P100", "fecha": "2025-01-01",
         "proveedor": "X", "cantidad": 1, "precio": 1.0},
    ]
    ordenado = ordenar_compras(desordenado)
    claves = [(c["sucursal"], c["producto"], c["fecha"]) for c in ordenado]
    assert claves == [
        ("SUC01", "P100", "2025-01-01"),
        ("SUC01", "P100", "2025-01-05"),
        ("SUC01", "P200", "2025-01-01"),
        ("SUC02", "P100", "2025-01-01"),
    ]


def test_resumen_por_sucursal():
    resumen = resumen_por_sucursal(COMPRAS_EJEMPLO)
    assert resumen["SUC01"]["total_unidades"] == 17
    assert resumen["SUC01"]["producto_mayor"] == "P100"
    assert resumen["SUC01"]["producto_menor"] == "P200"


def test_parsear_linea_valida():
    fila = "SUC01,P100,2025-01-01,PROV02,116,246.97"
    compra = parsear_linea(fila)
    assert compra["sucursal"] == "SUC01"
    assert compra["cantidad"] == 116
    assert compra["precio"] == 246.97


def test_parsear_linea_cantidad_invalida():
    fila = "SUC01,P100,2025-01-01,PROV02,abc,246.97"
    with pytest.raises(ValueError):
        parsear_linea(fila)


def test_parsear_linea_columnas_faltantes():
    fila = "SUC01,P100,2025-01-01"
    with pytest.raises(ValueError):
        parsear_linea(fila)


def test_parsear_linea_precio_negativo():
    fila = "SUC01,P100,2025-01-01,PROV02,10,-5.0"
    with pytest.raises(ValueError):
        parsear_linea(fila)


def test_producto_mas_vendido_lista_vacia():
    with pytest.raises(ValueError):
        producto_mas_vendido([])
