# BCV Rate scraper

Este README también esta disponible en [English/Ingles](README.md).

Este proyecto es un conjunto de scripts para extraer valores de monedas de la página web del Banco Central de Venezuela (BCV).

Los scripts son:

- `web_scrap.py`: Este script extrae los valores de USD y EUR de la página web del BCV y los guarda en un archivo. También registra las operaciones de extracción en un archivo de registro y muestra una notificación en la pantalla cuando los valores se extraen con éxito.

- `excel_scrap.py`: Este script extrae los valores de USD y EUR de los archivos xls en la página web del BCV y los guarda en un archivo. También renombra los archivos en la carpeta.

## Instalación

### Instrucciones de instalación

1. Crea un entorno virtual:

```bash
python -m venv venv
```

2. Activa el entorno virtual:

```bash
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Paquetes requeridos

- `beautifulsoup4`
- `xlrd`

## Configuración

Para configurar los scripts con diferentes ajustes, edite el archivo `config.py`, los valores predeterminados son:

```python
BCV_URL = "https://www.bcv.org.ve/"
OUTPUT_DIR = "./output/"
XLS_DIR = "./xls_files/"
XLS_FILE = OUTPUT_DIR + "excel.txt"
LOG_FILE = OUTPUT_DIR + "log.txt"
HISTORY_FILE = OUTPUT_DIR + "history.txt"
NOTIFICATION_ENABLED = True
RENAME_FILES_ENABLED = True
```

Nota: actualmente las notificaciones de nuevos valores de las monedas se hacen con notify-send, puedes utilizar cualquier otra interfaz de línea de comandos de notificación modificando la función `show_notification` en el script.

## Uso

### Uso independiente

Para ejecutar los scripts de forma independiente desde el directorio raíz, utiliza los siguientes comandos:

```bash
python python -m bcv_scraper.web_scrap
```

```bash
python python -m bcv_scraper.excel_scrap
```

**Nota:** el script `web_scrap.py` puede tener un argumento opcional para ejecutar el script, lo que agregará un valor al archivo de registro, esto puede ser utilizado para diferenciar entre ejecuciones de diferentes contextos. por ejemplo:

```bash
python -m bcv_scraper.web_scrap auto
```

Se generará la siguiente entrada en el registro:

```text
2024-07-03 15:30:00 auto
```

### Ejecutar con cron

Para ejecutar los scripts con cron, utilizando el script bash proporcionado `script.sh`, puedes agregar las siguientes líneas a tu crontab:

```text
*/30 15-16 * * 1-5 /absolute/path/to/project/script.sh
```

**Nota:** Debes cambiar esta línea en el script bash con la ruta absoluta al proyecto.

```bash
fullpath="/absolute/path/to/project"
```

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE). Esto significa que puedes usar, modificar y distribuir este proyecto de forma gratuita siempre y cuando incluyes la nota de derechos de autor y la licencia en todas las copias o partes significativas del software.
