"""
config.py — Configuración global del juego Click & Hide.

Contiene constantes relacionadas con:
  - Pantalla
  - Jugador
  - Colores
  - Fuentes
  - Rutas de recursos
  - Parámetros de la intro
  - Depuración / desarrollo
"""

# --- CONFIGURACIÓN DE PANTALLA ---
WIDTH = 1280  # Ancho de la ventana principal
HEIGHT = 720  # Alto de la ventana principal
FPS = 60  # Fotogramas por segundo
FULLSCREEN = False  # Si es True, inicia en modo pantalla completa


# --- PARÁMETROS DEL JUGADOR ---
MONEY_START = 0  # Dinero inicial del jugador
EARN_AMOUNT = 1  # Cantidad de dinero obtenida por clic
EARN_COOLDOWN = 0.2  # Tiempo mínimo (en segundos) entre clics válidos


# --- COLORES GENERALES (RGB) ---
COLOR_BG_TOP = (250, 240, 210)  # Color superior del fondo degradado
COLOR_BG_BOTTOM = (235, 220, 180)  # Color inferior del fondo degradado
COLOR_HEADER = (180, 150, 100)  # Color del encabezado superior
COLOR_PANEL = (245, 240, 220)  # Color de los paneles
COLOR_TEXT = (50, 35, 20)  # Color del texto general


# --- PARÁMETROS DE LA TIENDA ---
SHOP_PANEL_WIDTH = 380  # Ancho del panel de la tienda
SHOP_ITEM_HEIGHT = 60  # Altura de cada ítem de la tienda
SHOP_PADDING_X = 30  # Espaciado horizontal dentro del panel
SHOP_PADDING_Y = 8  # Espaciado vertical entre ítems


# --- CONFIGURACIÓN DE FUENTES ---
FONT_PATH = "assets/fonts/PressStart2P.ttf"  # Ruta de la fuente principal
FONT_SMALL = 14  # Tamaño de fuente pequeña
FONT_MEDIUM = 18  # Tamaño de fuente mediana
FONT_BIG = 28  # Tamaño de fuente grande


# --- INTRO / PANTALLA DE PRESENTACIÓN ---
INTRO_IMAGE = "clase.png"  # Imagen de fondo de la intro
LOGO_SIZE = (100, 100)  # Tamaño del logo principal
INTRO_MOVE_DURATION = 3.0  # Duración del movimiento del texto (s)
INTRO_LOAD_DURATION = 5.0  # Duración total de la pantalla de carga (s)
INTRO_FONT_SIZE = 64  # Tamaño del texto principal
INTRO_TEXT = "CLICK AND HIDE"  # Texto mostrado en la intro
INTRO_TEXT_COLOR = (255, 255, 255)  # Color del texto principal


# --- RUTAS Y ARCHIVOS ---
ASSETS_PATH = "assets"  # Carpeta raíz de los recursos
IMAGES_PATH = f"{ASSETS_PATH}/images"  # Carpeta de imágenes
FONTS_PATH = f"{ASSETS_PATH}/fonts"  # Carpeta de fuentes
SOUNDS_PATH = f"{ASSETS_PATH}/sounds"  # Carpeta de sonidos


# --- DEBUG / DESARROLLO ---
DEBUG_MODE = False  # Si es True, activa mensajes de depuración
