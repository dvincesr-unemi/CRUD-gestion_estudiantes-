from typing import List, Dict, Callable, Any
from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# Asumimos que el archivo anterior lo guardaste como controllers.py
from controllers import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, estadisticas, agregar_calificacion
)

def pausa() -> None:
    """Detiene la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes: List[Estudiante]) -> None:
    """
    Imprime una tabla formateada en consola con los datos de una lista de estudiantes.
    
    Args:
        estudiantes (List[Estudiante]): Lista de objetos Estudiante a mostrar.
    """
    # Usamos f-strings con alineación: <5 (alineado a la izquierda, 5 espacios)
    print(f"{'ID':<5}{'CÉDULA':<15}{'NOMBRE Y APELLIDO':<30}{'CARRERA':<20}{'NIVEL':<7}")
    print("-" * 80)
    for est in estudiantes:
        print(f"{est.id:<5}{est.cedula:<15}{est.obtener_nombre_completo():<30}"
              f"{est.carrera:<20}{est.nivel:<7}")
    print("-" * 80)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ===================== C · CREAR =====================

def opcion_crear() -> None:
    """Solicita los datos por teclado y llama al controlador para crear un estudiante."""
    imprimir_titulo("MATRICULAR NUEVO ESTUDIANTE")
    
    datos: Dict[str, str] = {}
    # Recorremos la TUPLA inmutable del modelo. Si mañana agregas "direccion" al modelo,
    # este formulario se actualiza automáticamente sin tocar este archivo.
    for campo in CAMPOS_ESTUDIANTE:
        if campo == "beca_activa":
            datos[campo] = input("¿Tiene beca activa? (Deje en blanco para NO, escriba algo para SÍ): ")
        else:
            datos[campo] = input(f"{campo.capitalize()}: ")

    # Desempaquetamos la tupla (bool, str) que nos devuelve el controlador
    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ===================== R · LEER TODOS =====================

def opcion_ver_todos() -> None:
    """Obtiene y muestra la tabla completa de estudiantes."""
    imprimir_titulo("LISTADO GENERAL DE ESTUDIANTES")
    estudiantes = obtener_todos()
    
    if not estudiantes:
        imprimir_info("No hay estudiantes matriculados. Use la opción 1 para empezar.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ===================== S · BUSCAR =====================

def opcion_buscar() -> None:
    """Busca estudiantes por texto parcial usando el controlador."""
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Ingrese nombre, email, cédula, carnet o carrera: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ===================== R · LEER UNO =====================

def opcion_ver_por_id() -> None:
    """Muestra el detalle completo (diccionario) de un estudiante específico."""
    imprimir_titulo("VER DETALLE DE ESTUDIANTE")
    try:
        id_estudiante = int(input("Ingrese el ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con ID {id_estudiante}")
    else:
        # Recorremos el DICCIONARIO que nos devuelve el método de serialización del modelo
        print("\n--- DATOS PERSONALES Y ACADÉMICOS ---")
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.upper():<12}: {valor}")
            
        print("\n--- RENDIMIENTO ---")
        print(f"  PROMEDIO    : {estudiante.obtener_promedio()}")
    pausa()


# ===================== U · ACTUALIZAR =====================

def opcion_actualizar() -> None:
    """Solicita campos a editar y envía solo los cambios al controlador."""
    imprimir_titulo("ACTUALIZAR DATOS DE ESTUDIANTE")
    try:
        id_estudiante = int(input("Ingrese el ID del estudiante a editar: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con ID {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a: {estudiante.obtener_nombre_completo()}")
    print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

    cambios: Dict[str, Any] = {}
    for campo in CAMPOS_ESTUDIANTE:
        # getattr() nos permite extraer el valor actual de un atributo del objeto usando un string
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
        # Si el usuario escribió algo, lo agregamos al diccionario de cambios
        if nuevo:
            if campo == "beca_activa":
                # Truco simple: si escribió algo, asumimos True, si escribió "false/0/no", False
                cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
            else:
                cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ===================== D · ELIMINAR =====================

def opcion_eliminar() -> None:
    """Pide confirmación y elimina un estudiante por ID."""
    imprimir_titulo("DAR DE BAJA ESTUDIANTE")
    try:
        id_estudiante = int(input("Ingrese el ID del estudiante a dar de baja: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con ID {id_estudiante}")
        return pausa()

    # Usamos el método mágico __str__ del objeto para mostrarlo de forma bonita
    imprimir_info(f"Se eliminará permanentemente a:\n{estudiante}")
    
    if confirmar("¿Confirma la eliminación? (s/n): "):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada.")
    pausa()


# ===================== A · GESTIÓN ACADÉMICA =====================

def opcion_agregar_nota() -> None:
    """Opción nueva para interactuar con la lógica matemática del modelo."""
    imprimir_titulo("REGISTRAR CALIFICACIÓN")
    try:
        id_estudiante = int(input("Ingrese el ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    materia = input("Nombre de la materia (ej. Cálculo): ").strip().title()
    nota_str = input("Calificación (ej. 18.5): ").strip()
    
    exito, mensaje = agregar_calificacion(id_estudiante, materia, nota_str)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ===================== EXTRA · ESTADÍSTICAS =====================

def opcion_estadisticas() -> None:
    """Muestra el resumen generado por las comprensiones de colecciones del controlador."""
    imprimir_titulo("ESTADÍSTICAS ACADÉMICAS")
    datos = estadisticas()
    
    print(f"  Estudiantes matriculados : {datos['total']}")
    print(f"  Facultades activas       : {len(datos['facultades'])} -> {', '.join(datos['facultades'])}")
    print(f"  Carreras con alumnos     : {len(datos['carreras'])} -> {', '.join(datos['carreras'])}")
    print(f"  Total alumnos con Beca   : {datos['total_becados']}")
    
    if datos["becados"]:
        print(f"  Listado de Becados       : {', '.join(datos['becados'])}")
    pausa()


def salir() -> str:
    """Cierra el bucle principal de la aplicación."""
    imprimir_info("¡Gracias por usar el Sistema Académico! 👋")
    return "salir"


# ===================== MOTOR DEL MENÚ =====================

# DICCIONARIO DE FUNCIONES: En Python, las funciones son "ciudadanos de primera clase".
# Esto significa que podemos guardar funciones dentro de variables o diccionarios.
# La clave es el string que el usuario teclea, el valor es una Tupla (Texto del menú, Función a ejecutar).
OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
    "1": ("Matricular estudiante", opcion_crear),
    "2": ("Ver listado completo", opcion_ver_todos),
    "3": ("Buscar estudiante", opcion_buscar),
    "4": ("Ver detalle de estudiante", opcion_ver_por_id),
    "5": ("Actualizar datos", opcion_actualizar),
    "6": ("Dar de baja (Eliminar)", opcion_eliminar),
    "7": ("Registrar calificación (Materia/Nota)", opcion_agregar_nota),
    "8": ("Ver estadísticas globales", opcion_estadisticas),
    "0": ("Salir del sistema", salir),
}


def mostrar_menu() -> None:
    """Itera sobre el diccionario de opciones para pintar el menú en consola."""
    imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA - ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main() -> None:
    """Bucle infinito (while True) que controla el ciclo de vida de la aplicación."""
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        # Búsqueda instantánea en las claves del diccionario O(1)
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida. Por favor, intente de nuevo.")
            pausa()
            continue

        # Desempaquetamos la tupla correspondiente a la tecla presionada
        _texto, funcion = OPCIONES[tecla]
        
        # Ejecutamos la función. Si la función devuelve "salir", rompemos el bucle.
        if funcion() == "salir":
            break


# Punto de entrada de la aplicación. Evita que main() se ejecute si este archivo es importado en otro lugar.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Captura amigable del Ctrl+C
        print("\n\nPrograma interrumpido por el usuario de forma abrupta.")