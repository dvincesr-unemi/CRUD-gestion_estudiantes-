import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla() -> None:
    """
    Limpia la pantalla de la terminal.
    
    Args:
        Ninguno.
        
    Returns:
        None
    """
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto: str, color: str) -> None:
    """
    Imprime un texto en la consola usando un color específico.
    
    Args:
        texto (str): El mensaje que se desea imprimir.
        color (str): La clave del color a usar (ej. 'ROJO', 'VERDE').
        
    Returns:
        None
    """
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto: str) -> None:
    """
    Limpia la pantalla e imprime un texto centrado como título con bordes.
    
    Args:
        texto (str): El texto que irá en el centro del título.
        
    Returns:
        None
    """
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje: str) -> None:
    """
    Imprime un mensaje de éxito en color verde con un visto bueno.
    
    Args:
        mensaje (str): El mensaje de éxito a mostrar.
        
    Returns:
        None
    """
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje: str) -> None:
    """
    Imprime un mensaje de error en color rojo con una equis.
    
    Args:
        mensaje (str): El mensaje de error a mostrar.
        
    Returns:
        None
    """
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje: str) -> None:
    """
    Imprime un mensaje informativo en color cyan con un ícono.
    
    Args:
        mensaje (str): El mensaje informativo a mostrar.
        
    Returns:
        None
    """
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta: str) -> bool:
    """
    Muestra una pregunta al usuario y espera una confirmación por teclado.
    
    Args:
        pregunta (str): La pregunta que se le hará al usuario.
        
    Returns:
        bool: True si la respuesta está en la tupla RESPUESTAS_SI, False en caso contrario.
    """
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI 


def es_email_valido(texto: str) -> bool:
    """
    Verifica si una cadena de texto tiene el formato básico de un correo electrónico.
    
    Args:
        texto (str): El correo electrónico a evaluar.
        
    Returns:
        bool: True si cumple con la validación mínima, False en caso contrario.
    """
    # Validación mínima: un @, algo antes, algo después y un punto al final
    texto = texto.strip()   
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")