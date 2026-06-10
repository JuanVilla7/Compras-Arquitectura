# Compras Supermercado

Sistema de procesamiento de compras de un supermercado con integración continua
(GitHub Actions), pruebas unitarias y protección de la rama principal.

## Estructura

- `supermercado.py` — funciones principales del sistema.
- `main.py` — programa de consola que genera el informe.
- `test_supermercado.py` — pruebas unitarias (pytest).
- `COMPRAS_supermercado.csv` — datos de entrada.
- `requirements.txt` — dependencias.
- `.github/workflows/ci.yml` — pipeline de CI.

## Datos de entrada

Columnas del CSV: `PRSUC` (sucursal), `PRCOD` (producto), `PRFEC` (fecha),
`PRPROV` (proveedor), `PRCANT` (cantidad), `PRPRE` (precio unitario).

## Ejecución

```bash
pip install -r requirements.txt
python main.py
```

## Tests

```bash
pytest -v
```

## Integración continua

Cada push y cada Pull Request hacia `main` ejecuta el pipeline, que instala las
dependencias y corre los tests. La rama `main` está protegida: requiere Pull
Request y que el pipeline pase antes de poder mergear.
