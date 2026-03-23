# dataplot
- Notebook de ejemplo con todo
- Añadir la opcion de graficar datos + # filtrado de los filtrados
- Añadir la opcion de graficar datos + # derivadas de las derivadas
- Añadir la opcion de graficar datos + # integral de las integrales
- Añadir la opcion de graficar datos + # integral de la integral, derivada de las derivadas
- Graficar de multiples archivos, en un mismo plot
- Graficar de multiples archivos, en varios sunplots
- Graficar de un mismo archivo multiples datos

# mcda
- añadirle la opción de incluir varios métodos para normalizar los datos antes de comparar ("max", "minmax", "vector", "custom")
- Que los archivos se guarden en una carpeta /output

# in general TBD
- Lista de requerimientos
- Documentación (o al menos ejemplos)

# Ejecución de scripts Python desde cualquier carpeta del repositorio
## Resolución de `ModuleNotFoundError: No module named 'python_utilities'`

---

## Problema

Al ejecutar un script Python ubicado en una subcarpeta del repositorio, por ejemplo:

```bash
python scripts/test_mcda.py
```

se producía el error:

```text
ModuleNotFoundError: No module named 'python_utilities'
```

Esto ocurría a pesar de que:

- La estructura del paquete era correcta (`__init__.py` presentes).
- Los imports eran absolutos (`from python_utilities...`).
- El repositorio estaba correctamente organizado.

---

## Causa raíz

Python no añade automáticamente la raíz del repositorio al path de imports.

Aunque el prompt muestre que se está en la raíz del repo, Python solo puede importar módulos que estén en:

- El directorio del script ejecutado
- El `cwd`
- El `PYTHONPATH`
- `site-packages`

La variable de entorno `PYTHONPATH` no estaba definida en la terminal desde la que se ejecutaba el script.

Las variables de entorno configuradas en VSCode solo se aplican a terminales nuevas.
Las terminales abiertas antes del cambio no heredan la configuración.

---

## Solución

### 1. Configurar PYTHONPATH en VSCode

En el archivo `settings.json` del workspace o global, se añadió:

```json
"terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}"
}
```

Esto garantiza que todas las terminales integradas nuevas tengan como path de imports la raíz del repositorio.

---

### 2. Configuración adicional recomendada

Para evitar falsos errores en VSCode y mejorar autocompletado:

```json
"python.analysis.extraPaths": [
    "${workspaceFolder}"
],
"python.autoComplete.extraPaths": [
    "${workspaceFolder}"
]
```

Para asegurar consistencia en ejecución y debugging:

```json
"launch": {
    "configurations": [
        {
            "name": "Run Python Script (general)",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

---

## Paso crítico (imprescindible)

Después de modificar `settings.json`:

1. Cerrar todas las terminales integradas de VSCode
2. Abrir una nueva terminal integrada

Sin este paso, la variable `PYTHONPATH` no se aplica.

---

## Verificación

En una terminal integrada nueva:

```powershell
echo $env:PYTHONPATH
```

Resultado esperado:

```text
D:\repos\utilities
```

Luego ejecutar:

```bash
python scripts/test_mcda.py
```

El script debe ejecutarse sin errores de importación.

---

## Resultado final

Con esta configuración:

- Los scripts pueden ejecutarse desde cualquier carpeta del repositorio
- Se usan imports absolutos
- No se modifica `sys.path`
- No se requieren hacks ni configuraciones por archivo
- La solución es global, limpia y escalable

---

## Notas importantes

- Esta solución aplica solo a terminales integradas de VSCode
- No funciona automáticamente en PowerShell o CMD externos
- Para ejecución fuera de VSCode (CI, otros equipos), la alternativa correcta es:

```bash
pip install -e .
```

---

## Conclusión

El problema no estaba en la estructura del paquete ni en los imports, sino en el contexto de ejecución del entorno.

La combinación de:

- `PYTHONPATH = ${workspaceFolder}`
- reinicio de terminales integradas

resuelve de forma definitiva la ejecución de scripts desde cualquier ubicación del repositorio.
