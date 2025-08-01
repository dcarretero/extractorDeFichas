# extractorDeFichas

Este proyecto permite extraer y procesar información de fichas de seguridad química almacenadas en la carpeta [`Fichas/`](Fichas). El script principal es [`extractorDeFichas.py`](extractorDeFichas.py).

## Estructura del proyecto

- [`extractorDeFichas.py`](extractorDeFichas.py): Script principal para la extracción y procesamiento de fichas.
- [`requirements.txt`](requirements.txt): Dependencias necesarias para ejecutar el proyecto.
- [`drivers/`](drivers): Controladores y licencias para automatización (por ejemplo, `chromedriver.exe`).
- [`Fichas/`](Fichas): Carpeta que contiene los archivos de fichas de seguridad química en formato `.txt`.
- [`.vscode/`](.vscode): Configuración para Visual Studio Code.

## Requisitos

Instala las dependencias ejecutando:

```sh
pip install -r requirements.txt
```

## Uso

Ejecuta el script principal:

```sh
python extractorDeFichas.py
```

## Notas

- El proyecto está pensado para ejecutarse en un entorno Linux (Ubuntu 24.04.2 LTS).
- Si necesitas abrir una página web desde el contenedor, utiliza el comando:
  ```sh
  "$BROWSER" <url>
  ```

## Licencia

Consulta los archivos de licencia en la carpeta [`drivers/`](drivers) para información sobre el uso de los controladores.

---

Si tienes dudas, revisa el código fuente o los archivos de configuración incluidos.
