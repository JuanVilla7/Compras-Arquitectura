import sys

from supermercado import leer_compras, ordenar_compras, generar_informe


def main(argv):
    path = argv[1] if len(argv) > 1 else "COMPRAS_supermercado.csv"
    compras = leer_compras(path)
    compras = ordenar_compras(compras)
    print(generar_informe(compras))


if __name__ == "__main__":
    main(sys.argv)
