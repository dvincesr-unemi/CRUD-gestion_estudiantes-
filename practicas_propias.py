# from typing import Dict, List, Set, Any, Optional

# # Tupla de configuración con todos los atributos de la entidad
# # Sirve como la "fuente de la verdad" para generar formularios dinámicos y validaciones
# CAMPOS_LIBRO: tuple[str, ...] = (
#     "titulo",
#     "autor",
#     "isbn",
#     "categoria",
#     "editorial",
#     "anio_publicacion",
#     "ejemplares_totales",
#     "disponible",
# )

# class Libro:
#     # MODELO: Representa un libro dentro del sistema de la biblioteca.
#     # Encapsula datos bibliográficos, calificaciones (diccionarios) y lectores (conjuntos).

#     def __init__(
#         self,
#         id_libro: int,
#         titulo: str,
#         autor: str,
#         isbn: str,
#         categoria: str,
#         editorial: str,
#         anio_publicacion: int,
#         ejemplares_totales: int,
#         disponible: bool = True,
#         calificaciones: Optional[Dict[str, List[float]]] = None,
#         lectores: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor de la clase que inicializa el estado del libro
#         self.id = id_libro
#         self.titulo = titulo
#         self.autor = autor
#         self.isbn = isbn
#         self.categoria = categoria
#         self.editorial = editorial
#         self.anio_publicacion = anio_publicacion
#         self.ejemplares_totales = ejemplares_totales
#         self.disponible = disponible
        
#         # Diccionario de listas: {"Ana": [5.0, 4.5], "Luis": [4.0]}
#         # Guarda las puntuaciones que los lectores le han dado a la obra
#         self.calificaciones = calificaciones if calificaciones else {}
        
#         # Conjunto (set): Nombres de los lectores que han leído el libro (sin repetidos)
#         self.lectores = set(lectores) if lectores else set()

#     def obtener_info_basica(self) -> str:
#         # Devuelve título y autor concatenados
#         # Se utilizará en el controlador para reportar el libro mejor calificado y al editar
#         return f"'{self.titulo}' escrito por {self.autor}"

#     def agregar_calificacion(self, lector: str, calificacion: float) -> None:
#         # Registra una puntuación dada por un lector
#         # Al añadir al set, si el lector ya existe, se ignora evitando duplicados automáticamente
#         self.lectores.add(lector)
        
#         # setdefault busca al lector: si no existe, crea una lista vacía y luego hace append
#         self.calificaciones.setdefault(lector, []).append(calificacion)

#     def obtener_calificacion_promedio(self) -> float:
#         # Calcula el promedio aritmético de TODAS las calificaciones recibidas
#         # Se utilizará en las estadísticas y al imprimir el objeto
#         todas = []
#         for lista_notas in self.calificaciones.values():
#             todas.extend(lista_notas)
            
#         if not todas:
#             return 0.0
            
#         return round(sum(todas) / len(todas), 2)

#     def lectores_en_comun(self, otro_libro: "Libro") -> Set[str]:
#         # Compara los lectores de este libro con los de otro usando intersección de conjuntos
#         # Se utilizará en el controlador para encontrar similitudes de público
#         return self.lectores & otro_libro.lectores

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa el objeto a diccionario para poder guardarlo en el archivo JSON
#         return {
#             "id": self.id,
#             "titulo": self.titulo,
#             "autor": self.autor,
#             "isbn": self.isbn,
#             "categoria": self.categoria,
#             "editorial": self.editorial,
#             "anio_publicacion": self.anio_publicacion,
#             "ejemplares_totales": self.ejemplares_totales,
#             "disponible": self.disponible,
#             "calificaciones": self.calificaciones,
#             # JSON no soporta 'set', por lo que lo convertimos a una lista ordenada
#             "lectores": sorted(self.lectores),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Libro":
#         # Factory Method: Reconstruye un objeto Libro a partir de un diccionario leído del JSON
#         return cls(
#             datos["id"],
#             datos["titulo"],
#             datos["autor"],
#             datos["isbn"],
#             datos["categoria"],
#             datos["editorial"],
#             int(datos["anio_publicacion"]),
#             int(datos["ejemplares_totales"]),
#             disponible=datos.get("disponible", True),
#             calificaciones=datos.get("calificaciones", {}),
#             lectores=set(datos.get("lectores", [])),
#         )

#     def __str__(self) -> str:
#         # Define cómo se muestra el objeto al imprimirlo directamente en consola
#         return f"[{self.isbn}] {self.obtener_info_basica()} - Rating: {self.obtener_calificacion_promedio()} ⭐"

# from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Libro, CAMPOS_LIBRO
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo del catálogo
# gestor = GestorJSON("biblioteca.json")

# # Campos permitidos para la búsqueda
# CAMPOS_BUSCABLES = ("titulo", "autor", "isbn", "categoria", "editorial")

# def isbns_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve un conjunto con todos los ISBN registrados
#     # SE USA en crear_libro y actualizar_libro para validar que no haya duplicados
#     registros = gestor.leer()
#     return {str(r["isbn"]).strip() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_libro(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea y persiste un nuevo libro validando las reglas de negocio
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_LIBRO:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "disponible":
#                     return False, f"El campo '{campo}' es obligatorio."

#         isbn = str(datos["isbn"]).strip()
        
#         # AQUÍ USAMOS la función auxiliar isbns_registrados
#         if isbn in isbns_registrados():
#             return False, "El ISBN ya está registrado en el catálogo."

#         try:
#             anio = int(datos["anio_publicacion"])
#             ejemplares = int(datos["ejemplares_totales"])
#         except ValueError:
#             return False, "El año y los ejemplares deben ser números enteros."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         disponible = bool(datos.get("disponible", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "titulo": datos["titulo"].strip().title(),
#             "autor": datos["autor"].strip().title(),
#             "isbn": isbn,
#             "categoria": datos["categoria"].strip().title(),
#             "editorial": datos["editorial"].strip().title(),
#             "anio_publicacion": anio,
#             "ejemplares_totales": ejemplares,
#             "disponible": disponible,
#             "calificaciones": {},
#             "lectores": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Libro registrado con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar libro: {error}"

# def obtener_todos() -> List[Libro]:
#     # Lee el JSON y reconstruye todos los objetos Libro
#     # AQUÍ USAMOS desde_diccionario() del modelo
#     return [Libro.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_libro: int) -> Optional[Libro]:
#     # Busca un libro por su ID único
#     # AQUÍ USAMOS obtener_todos()
#     for libro in obtener_todos():
#         if libro.id == id_libro:
#             return libro
#     return None

# def buscar_libros(termino: str) -> List[Libro]:
#     # Búsqueda difusa o lineal por múltiples campos configurados
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Libro.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_libro(id_libro: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Modifica únicamente los campos enviados en el diccionario
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio"
                
#         if "isbn" in cambios:
#             # AQUÍ USAMOS nuevamente la función auxiliar isbns_registrados
#             if str(cambios["isbn"]).strip() in isbns_registrados(excepto_id=id_libro):
#                 return False, "Ese ISBN ya pertenece a otro libro."

#         if "anio_publicacion" in cambios or "ejemplares_totales" in cambios:
#             try:
#                 if "anio_publicacion" in cambios: cambios["anio_publicacion"] = int(cambios["anio_publicacion"])
#                 if "ejemplares_totales" in cambios: cambios["ejemplares_totales"] = int(cambios["ejemplares_totales"])
#             except ValueError:
#                 return False, "El año y los ejemplares deben ser números enteros."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_libro:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un libro con id {id_libro}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Libro {id_libro} actualizado"

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_libro(id_libro: int) -> Tuple[bool, str]:
#     # Elimina un libro del catálogo
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_libro]

#     if len(quedan) == len(registros):
#         return False, f"No existe un libro con id {id_libro}"

#     gestor.guardar(quedan)
#     return True, f"Libro {id_libro} eliminado"

# def agregar_calificacion_libro(id_libro: int, lector: str, calificacion: str) -> Tuple[bool, str]:
#     # Añade la reseña de un lector a un libro
#     try:
#         libro = obtener_por_id(id_libro)
#         if not libro:
#             return False, f"No existe un libro con ID {id_libro}"

#         calif_num = float(calificacion)
#         if not (0 <= calif_num <= 5):
#             return False, "La calificación debe estar entre 0 y 5 estrellas."
        
#         # AQUÍ USAMOS el método del modelo agregar_calificacion()
#         libro.agregar_calificacion(lector.title(), calif_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_libro:
#                 # AQUÍ USAMOS el método del modelo a_diccionario()
#                 registros[i] = libro.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Calificación de {calif_num}⭐ añadida por {lector.title()}."
        
#     except ValueError:
#         return False, "La calificación debe ser un número (ej. 4.5)"
#     except Exception as error:
#         return False, f"Error al registrar la calificación: {error}"

# def todos_los_lectores() -> Set[str]:
#     # Devuelve un set con los nombres de todos los usuarios
#     libros = obtener_todos()
#     lectores_totales = set()
    
#     for libro in libros:
#         lectores_totales.update(libro.lectores)
        
#     return lectores_totales

# def lectores_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos libros y devuelve los lectores que han leído AMBOS
#     libro_a = obtener_por_id(id_a)
#     libro_b = obtener_por_id(id_b)
    
#     if not libro_a or not libro_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo lectores_en_comun()
#     return libro_a.lectores_en_comun(libro_b)

# def libro_mejor_calificado() -> Optional[Dict[str, Any]]:
#     # Función de reporte que busca el libro con el promedio más alto
#     # SE USA internamente en la función de estadísticas
#     libros = obtener_todos()
#     if not libros:
#         return None
    
#     # AQUÍ USAMOS obtener_calificacion_promedio() del modelo para la lógica de búsqueda
#     mejor = max(libros, key=lambda l: l.obtener_calificacion_promedio())
    
#     # AQUÍ USAMOS obtener_info_basica() y obtener_calificacion_promedio() del modelo
#     return {
#         "info": mejor.obtener_info_basica(),
#         "rating": mejor.obtener_calificacion_promedio()
#     }

# def estadisticas() -> Dict[str, Any]:
#     # Genera métricas globales del catálogo
#     registros = gestor.leer()
    
#     categorias = {r.get("categoria", "").title() for r in registros if r.get("categoria")}
#     ejemplares_totales = sum(r.get("ejemplares_totales", 0) for r in registros)
    
#     # AQUÍ USAMOS libro_mejor_calificado() asegurando que ningún código quede muerto
#     mejor = libro_mejor_calificado()

#     return {
#         "total_libros": len(registros),
#         "total_ejemplares": ejemplares_totales,
#         "categorias": sorted(categorias),
#         "mejor_libro": mejor
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Libro, CAMPOS_LIBRO
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_libro, obtener_todos, obtener_por_id, buscar_libros,
#     actualizar_libro, eliminar_libro, agregar_calificacion_libro,
#     todos_los_lectores, lectores_en_comun, estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(libros: List[Libro]) -> None:
#     # Imprime una tabla formateada en consola con los datos de los libros
#     print(f"{'ID':<5}{'ISBN':<15}{'TÍTULO':<30}{'AUTOR':<25}{'STOCK':<7}")
#     print("-" * 85)
#     for lib in libros:
#         print(f"{lib.id:<5}{lib.isbn:<15}{lib.titulo[:28]:<30}{lib.autor[:23]:<25}{lib.ejemplares_totales:<7}")
#     print("-" * 85)
#     imprimir_info(f"Total: {len(libros)} libro(s)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para registrar un libro
#     imprimir_titulo("REGISTRAR NUEVO LIBRO")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_LIBRO:
#         if campo == "disponible":
#             datos[campo] = input("¿Está disponible para préstamo? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize()}: ")

#     exito, mensaje = crear_libro(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra la tabla completa del catálogo usando la función del controlador
#     imprimir_titulo("CATÁLOGO GENERAL DE LA BIBLIOTECA")
#     libros = obtener_todos()
    
#     if not libros:
#         imprimir_info("No hay libros registrados. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(libros)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por texto parcial
#     imprimir_titulo("BUSCAR LIBRO")
#     termino = input("Ingrese título, autor, ISBN, categoría o editorial: ")
#     encontrados = buscar_libros(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún libro coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de un libro específico y su rating
#     imprimir_titulo("VER DETALLE DE LIBRO")
#     try:
#         id_libro = int(input("Ingrese el ID del libro: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     libro = obtener_por_id(id_libro)
#     if not libro:
#         imprimir_error(f"No existe un libro con ID {id_libro}")
#     else:
#         print("\nDATOS BIBLIOGRÁFICOS")
#         for clave, valor in libro.a_diccionario().items():
#             print(f"  {clave.upper():<18}: {valor}")
            
#         print("\nRECEPCIÓN DEL PÚBLICO")
#         print(f"  RATING PROMEDIO   : {libro.obtener_calificacion_promedio()} ⭐")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos de un libro validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DEL LIBRO")
#     try:
#         id_libro = int(input("Ingrese el ID del libro a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     libro = obtener_por_id(id_libro)
#     if not libro:
#         imprimir_error(f"No existe un libro con ID {id_libro}")
#         return pausa()

#     imprimir_info(f"Editando: {libro.obtener_info_basica()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_LIBRO:
#         actual = getattr(libro, campo)
#         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "disponible":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_libro(id_libro, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y elimina un libro por ID a través del controlador
#     imprimir_titulo("ELIMINAR LIBRO DEL CATÁLOGO")
#     try:
#         id_libro = int(input("Ingrese el ID del libro a eliminar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     libro = obtener_por_id(id_libro)
#     if not libro:
#         imprimir_error(f"No existe un libro con ID {id_libro}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente:\n{libro}")
    
#     if confirmar("¿Confirma la eliminación? (si/no): "):
#         exito, mensaje = eliminar_libro(id_libro)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_agregar_calificacion() -> None:
#     # Interacciona con la lógica matemática para añadir estrellas a un libro
#     imprimir_titulo("RESEÑAR / CALIFICAR LIBRO")
#     try:
#         id_libro = int(input("Ingrese el ID del libro: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     lector = input("Nombre del lector: ").strip().title()
#     calificacion_str = input("Calificación (0 a 5 estrellas): ").strip()
    
#     exito, mensaje = agregar_calificacion_libro(id_libro, lector, calificacion_str)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_lectores_globales() -> None:
#     # Muestra un listado de todos los usuarios que han leído al menos un libro
#     imprimir_titulo("COMUNIDAD DE LECTORES ACTIVOS")
#     lectores = todos_los_lectores()
#     if not lectores:
#         imprimir_info("Aún no hay lectores registrados en el sistema.")
#     else:
#         for i, lector in enumerate(sorted(lectores), 1):
#             print(f"  {i}. {lector}")
#     pausa()

# def opcion_lectores_en_comun() -> None:
#     # Compara los lectores compartidos entre dos obras
#     imprimir_titulo("LECTORES COMPARTIDOS ENTRE DOS OBRAS")
#     try:
#         id_a = int(input("Ingrese el ID del primer libro: "))
#         id_b = int(input("Ingrese el ID del segundo libro: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = lectores_en_comun(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Usuarios que leyeron ambos libros: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No hay lectores en común o alguno de los IDs no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el resumen generado por las comprensiones de colecciones y métodos complejos
#     imprimir_titulo("ESTADÍSTICAS DE LA BIBLIOTECA")
#     datos = estadisticas()
    
#     print(f"  Títulos distintos en catálogo : {datos['total_libros']}")
#     print(f"  Ejemplares físicos totales    : {datos['total_ejemplares']}")
#     print(f"  Categorías activas ({len(datos['categorias'])})       : {', '.join(datos['categorias'])}")
    
#     mejor = datos.get("mejor_libro")
#     if mejor:
#         print("\n  LIBRO MEJOR CALIFICADO:")
#         print(f"  -> {mejor['info']} ({mejor['rating']} ⭐)")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal de la aplicación
#     imprimir_info("¡Gracias por usar el Sistema de Biblioteca! 👋")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # El motor del menú, asegura que cada opción apunta a una función real y utilizada
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Registrar nuevo libro", opcion_crear),
#     "2": ("Ver catálogo completo", opcion_ver_todos),
#     "3": ("Buscar libro", opcion_buscar),
#     "4": ("Ver detalle de un libro", opcion_ver_por_id),
#     "5": ("Actualizar datos de libro", opcion_actualizar),
#     "6": ("Dar de baja (Eliminar) libro", opcion_eliminar),
#     "7": ("Añadir calificación / reseña", opcion_agregar_calificacion),
#     "8": ("Ver comunidad de lectores (Sin repetir)", opcion_ver_lectores_globales),
#     "9": ("Ver lectores en común entre 2 libros", opcion_lectores_en_comun),
#     "10": ("Ver estadísticas de la biblioteca", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Itera sobre el diccionario de opciones para pintar el menú
#     imprimir_titulo("SISTEMA DE GESTIÓN BIBLIOTECARIA")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle principal que controla el ciclo de vida de la aplicación
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de entrada seguro
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable que define los campos exactos del empleado
# # Se usa dinámicamente para construir formularios y validaciones
# CAMPOS_EMPLEADO: tuple[str, ...] = (
#     "nombre",
#     "apellido",
#     "email",
#     "cedula",
#     "codigo_empleado",
#     "departamento",
#     "puesto",
#     "salario",
#     "bono_activo",
# )

# class Empleado:
#     # MODELO: Representa a un colaborador dentro de la empresa.
#     # Encapsula sus datos personales, financieros, evaluaciones (diccionarios) y habilidades (conjuntos).

#     def __init__(
#         self,
#         id_empleado: int,
#         nombre: str,
#         apellido: str,
#         email: str,
#         cedula: str,
#         codigo_empleado: str,
#         departamento: str,
#         puesto: str,
#         salario: float,
#         bono_activo: bool = False,
#         evaluaciones: Optional[Dict[str, List[float]]] = None,
#         habilidades: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor que inicializa el estado del empleado en memoria
#         self.id = id_empleado
#         self.nombre = nombre
#         self.apellido = apellido
#         self.email = email
#         self.cedula = cedula
#         self.codigo_empleado = codigo_empleado
#         self.departamento = departamento
#         self.puesto = puesto
#         self.salario = salario
#         self.bono_activo = bono_activo
        
#         # Diccionario de listas: {"Trimestre 1": [95.0, 90.5], "Trimestre 2": [88.0]}
#         # Guarda las puntuaciones de desempeño del empleado
#         self.evaluaciones = evaluaciones if evaluaciones else {}
        
#         # Conjunto (set): Habilidades técnicas o blandas (ej. "Python", "Liderazgo") sin repetir
#         self.habilidades = set(habilidades) if habilidades else set()

#     def obtener_nombre_completo(self) -> str:
#         # Concatena nombre y apellido
#         # Se usará en el controlador para reportes y mensajes de éxito
#         return f"{self.nombre} {self.apellido}"

#     def agregar_habilidad(self, habilidad: str) -> None:
#         # Añade una competencia al empleado
#         # Al ser un set, si se intenta añadir "Python" dos veces, la segunda se ignora
#         self.habilidades.add(habilidad.title())

#     def agregar_evaluacion(self, periodo: str, calificacion: float) -> None:
#         # Registra una nota de desempeño en un periodo específico
#         # setdefault crea la lista vacía si el periodo no existe, y luego hace append
#         self.evaluaciones.setdefault(periodo.title(), []).append(calificacion)

#     def obtener_promedio_desempeno(self) -> float:
#         # Calcula el rendimiento general promedio de todas las evaluaciones históricas
#         todas_las_notas = []
#         for lista_notas in self.evaluaciones.values():
#             todas_las_notas.extend(lista_notas)
            
#         if not todas_las_notas:
#             return 0.0
            
#         return round(sum(todas_las_notas) / len(todas_las_notas), 2)

#     def habilidades_en_comun(self, otro_empleado: "Empleado") -> Set[str]:
#         # Compara las competencias de este empleado con las de otro
#         # Retorna la intersección matemática de ambos conjuntos
#         return self.habilidades & otro_empleado.habilidades

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Convierte el objeto en un diccionario nativo para guardarlo en formato JSON
#         return {
#             "id": self.id,
#             "nombre": self.nombre,
#             "apellido": self.apellido,
#             "email": self.email,
#             "cedula": self.cedula,
#             "codigo_empleado": self.codigo_empleado,
#             "departamento": self.departamento,
#             "puesto": self.puesto,
#             "salario": self.salario,
#             "bono_activo": self.bono_activo,
#             "evaluaciones": self.evaluaciones,
#             # Se ordena alfabéticamente el set y se convierte a lista porque JSON no soporta sets
#             "habilidades": sorted(self.habilidades),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Empleado":
#         # Patrón Factory: Construye un objeto Empleado leyendo un diccionario crudo del JSON
#         return cls(
#             datos["id"],
#             datos["nombre"],
#             datos["apellido"],
#             datos["email"],
#             datos["cedula"],
#             datos["codigo_empleado"],
#             datos["departamento"],
#             datos["puesto"],
#             float(datos["salario"]),
#             bono_activo=datos.get("bono_activo", False),
#             evaluaciones=datos.get("evaluaciones", {}),
#             # Reconstruye el conjunto a partir de la lista almacenada
#             habilidades=set(datos.get("habilidades", [])),
#         )

#     def __str__(self) -> str:
#         # Formato visual al imprimir el objeto empleado directamente en consola
#         return f"[{self.codigo_empleado}] {self.obtener_nombre_completo()} - Desempeño: {self.obtener_promedio_desempeno()}/100"

# from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Empleado, CAMPOS_EMPLEADO
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo de la nómina
# gestor = GestorJSON("empleados.json")

# # Campos permitidos para el motor de búsqueda
# CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "cedula", "codigo_empleado", "departamento", "puesto")

# def emails_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve todos los emails para validar que no se repitan
#     # SE USA en crear_empleado y actualizar_empleado
#     registros = gestor.leer()
#     return {str(r["email"]).strip().lower() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def cedulas_registradas(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve las cédulas para validar unicidad
#     # SE USA en crear_empleado y actualizar_empleado
#     registros = gestor.leer()
#     return {str(r["cedula"]).strip() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def codigos_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve los códigos corporativos para evitar duplicados
#     # SE USA en crear_empleado y actualizar_empleado
#     registros = gestor.leer()
#     return {str(r["codigo_empleado"]).strip().upper() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_empleado(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea un nuevo empleado aplicando validaciones estrictas
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_EMPLEADO:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "bono_activo":
#                     return False, f"El campo '{campo}' es obligatorio."

#         email = str(datos["email"]).strip().lower()
#         cedula = str(datos["cedula"]).strip()
#         codigo = str(datos["codigo_empleado"]).strip().upper()

#         # AQUÍ USAMOS las tres funciones auxiliares de validación
#         if email in emails_registrados(): return False, "El email ya está registrado."
#         if cedula in cedulas_registradas(): return False, "La cédula ya existe en el sistema."
#         if codigo in codigos_registrados(): return False, "El código de empleado ya está en uso."

#         try:
#             salario = float(datos["salario"])
#         except ValueError:
#             return False, "El salario debe ser un valor numérico."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         bono = bool(datos.get("bono_activo"))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "nombre": datos["nombre"].strip().title(),
#             "apellido": datos["apellido"].strip().title(),
#             "email": email,
#             "cedula": cedula,
#             "codigo_empleado": codigo,
#             "departamento": datos["departamento"].strip().title(),
#             "puesto": datos["puesto"].strip().title(),
#             "salario": salario,
#             "bono_activo": bono,
#             "evaluaciones": {},
#             "habilidades": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Empleado contratado con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al crear empleado: {error}"

# def obtener_todos() -> List[Empleado]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Empleado
#     return [Empleado.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_empleado: int) -> Optional[Empleado]:
#     # Busca y devuelve un empleado específico
#     # AQUÍ USAMOS obtener_todos()
#     for empleado in obtener_todos():
#         if empleado.id == id_empleado:
#             return empleado
#     return None

# def buscar_empleados(termino: str) -> List[Empleado]:
#     # Búsqueda difusa de empleados
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Empleado.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_empleado(id_empleado: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza campos validados
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS nuevamente las funciones auxiliares para que no haya duplicidad al editar
#         if "email" in cambios and str(cambios["email"]).strip().lower() in emails_registrados(id_empleado):
#             return False, "Ese email ya lo usa otro empleado."
#         if "cedula" in cambios and str(cambios["cedula"]).strip() in cedulas_registradas(id_empleado):
#             return False, "Esa cédula ya está registrada."
#         if "codigo_empleado" in cambios and str(cambios["codigo_empleado"]).strip().upper() in codigos_registrados(id_empleado):
#             return False, "Ese código corporativo ya está en uso."

#         if "salario" in cambios:
#             try:
#                 cambios["salario"] = float(cambios["salario"])
#             except ValueError:
#                 return False, "El salario debe ser numérico."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_empleado:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un empleado con id {id_empleado}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Empleado {id_empleado} actualizado correctamente."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_empleado(id_empleado: int) -> Tuple[bool, str]:
#     # Da de baja a un empleado de la nómina
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_empleado]

#     if len(quedan) == len(registros):
#         return False, f"No existe un empleado con id {id_empleado}"

#     gestor.guardar(quedan)
#     return True, f"Empleado {id_empleado} dado de baja."

# def agregar_evaluacion_empleado(id_empleado: int, periodo: str, nota: str) -> Tuple[bool, str]:
#     # Registra una nota de desempeño para el empleado
#     try:
#         empleado = obtener_por_id(id_empleado)
#         if not empleado:
#             return False, f"No existe un empleado con ID {id_empleado}"

#         nota_num = float(nota)
#         if not (0 <= nota_num <= 100):
#             return False, "La calificación debe estar entre 0 y 100."
        
#         # AQUÍ USAMOS el método del modelo
#         empleado.agregar_evaluacion(periodo, nota_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_empleado:
#                 # AQUÍ USAMOS la serialización del modelo
#                 registros[i] = empleado.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Evaluación de {nota_num} añadida al periodo {periodo}."
        
#     except ValueError:
#         return False, "La calificación debe ser un número (ej. 95.5)"
#     except Exception as error:
#         return False, f"Error al registrar evaluación: {error}"

# def agregar_habilidad_empleado(id_empleado: int, habilidad: str) -> Tuple[bool, str]:
#     # Añade un skill al perfil del trabajador
#     empleado = obtener_por_id(id_empleado)
#     if not empleado:
#         return False, "Empleado no encontrado."
        
#     # AQUÍ USAMOS el método del modelo
#     empleado.agregar_habilidad(habilidad)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_empleado:
#             registros[i] = empleado.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Habilidad '{habilidad.title()}' agregada al perfil."

# def todas_las_habilidades() -> Set[str]:
#     # Devuelve el inventario total de skills presentes en la empresa
#     habilidades_empresa = set()
#     for empleado in obtener_todos():
#         habilidades_empresa.update(empleado.habilidades)
#     return habilidades_empresa

# def habilidades_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara las aptitudes compartidas entre dos colaboradores
#     emp_a = obtener_por_id(id_a)
#     emp_b = obtener_por_id(id_b)
    
#     if not emp_a or not emp_b:
#         return set()
        
#     # AQUÍ USAMOS el método de intersección del modelo
#     return emp_a.habilidades_en_comun(emp_b)

# def empleado_destacado() -> Optional[Dict[str, Any]]:
#     # Busca al empleado con el mejor puntaje global de desempeño
#     # Función auxiliar para estadísticas
#     empleados = obtener_todos()
#     if not empleados:
#         return None
    
#     # AQUÍ USAMOS obtener_promedio_desempeno del modelo
#     mejor = max(empleados, key=lambda e: e.obtener_promedio_desempeno())
    
#     # AQUÍ USAMOS obtener_nombre_completo del modelo
#     return {
#         "nombre": mejor.obtener_nombre_completo(),
#         "puntuacion": mejor.obtener_promedio_desempeno(),
#         "departamento": mejor.departamento
#     }

# def estadisticas() -> Dict[str, Any]:
#     # Calcula métricas globales de recursos humanos
#     empleados = obtener_todos()
    
#     departamentos = {e.departamento for e in empleados}
#     gasto_salarial = sum(e.salario for e in empleados)
#     empleados_con_bono = sum(1 for e in empleados if e.bono_activo)
    
#     # AQUÍ USAMOS la función de empleado destacado para que no quede huérfana
#     destacado = empleado_destacado()

#     return {
#         "total_empleados": len(empleados),
#         "departamentos_activos": sorted(departamentos),
#         "gasto_salarial_mensual": round(gasto_salarial, 2),
#         "empleados_con_bono": empleados_con_bono,
#         "empleado_destacado": destacado
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Empleado, CAMPOS_EMPLEADO
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_empleado, obtener_todos, obtener_por_id, buscar_empleados,
#     actualizar_empleado, eliminar_empleado, agregar_evaluacion_empleado,
#     agregar_habilidad_empleado, todas_las_habilidades, habilidades_en_comun, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(empleados: List[Empleado]) -> None:
#     # Imprime una tabla formateada en consola con los datos del personal
#     print(f"{'ID':<5}{'CÓDIGO':<12}{'NOMBRE Y APELLIDO':<30}{'DEPARTAMENTO':<18}{'SALARIO':<10}")
#     print("-" * 80)
#     for emp in empleados:
#         print(f"{emp.id:<5}{emp.codigo_empleado:<12}{emp.obtener_nombre_completo():<30}{emp.departamento[:16]:<18}${emp.salario:<9.2f}")
#     print("-" * 80)
#     imprimir_info(f"Total: {len(empleados)} colaborador(es)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para registrar un empleado
#     imprimir_titulo("REGISTRAR NUEVO EMPLEADO")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_EMPLEADO:
#         if campo == "bono_activo":
#             datos[campo] = input("¿Tiene bono por desempeño? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize()}: ")

#     exito, mensaje = crear_empleado(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra la nómina completa usando la función del controlador
#     imprimir_titulo("NÓMINA GENERAL DE EMPLEADOS")
#     empleados = obtener_todos()
    
#     if not empleados:
#         imprimir_info("No hay empleados registrados. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(empleados)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por texto parcial
#     imprimir_titulo("BUSCAR EMPLEADO")
#     termino = input("Ingrese nombre, cédula, código, puesto o departamento: ")
#     encontrados = buscar_empleados(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún empleado coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de un empleado específico y su desempeño
#     imprimir_titulo("PERFIL DEL EMPLEADO")
#     try:
#         id_empleado = int(input("Ingrese el ID del empleado: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     empleado = obtener_por_id(id_empleado)
#     if not empleado:
#         imprimir_error(f"No existe un empleado con ID {id_empleado}")
#     else:
#         print("\nDATOS CORPORATIVOS Y PERSONALES")
#         for clave, valor in empleado.a_diccionario().items():
#             print(f"  {clave.upper():<18}: {valor}")
            
#         print("\nRENDIMIENTO GLOBAL")
#         print(f"  DESEMPEÑO PROMEDIO: {empleado.obtener_promedio_desempeno()}/100")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos de un empleado validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DE EMPLEADO")
#     try:
#         id_empleado = int(input("Ingrese el ID del empleado a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     empleado = obtener_por_id(id_empleado)
#     if not empleado:
#         imprimir_error(f"No existe un empleado con ID {id_empleado}")
#         return pausa()

#     imprimir_info(f"Editando a: {empleado.obtener_nombre_completo()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_EMPLEADO:
#         actual = getattr(empleado, campo)
#         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "bono_activo":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_empleado(id_empleado, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y elimina un empleado por ID a través del controlador
#     imprimir_titulo("DAR DE BAJA A EMPLEADO")
#     try:
#         id_empleado = int(input("Ingrese el ID del empleado a dar de baja: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     empleado = obtener_por_id(id_empleado)
#     if not empleado:
#         imprimir_error(f"No existe un empleado con ID {id_empleado}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente a:\n{empleado}")
    
#     if confirmar("¿Confirma la baja de este empleado? (si/no): "):
#         exito, mensaje = eliminar_empleado(id_empleado)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_agregar_evaluacion() -> None:
#     # Interacciona con la lógica matemática para añadir una nota de desempeño
#     imprimir_titulo("REGISTRAR EVALUACIÓN DE DESEMPEÑO")
#     try:
#         id_empleado = int(input("Ingrese el ID del empleado: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     periodo = input("Periodo a evaluar (ej. Q1-2026, Trimestre 1): ").strip()
#     nota_str = input("Calificación (0 a 100): ").strip()
    
#     exito, mensaje = agregar_evaluacion_empleado(id_empleado, periodo, nota_str)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_agregar_habilidad() -> None:
#     # Añade un skill al perfil del empleado
#     imprimir_titulo("AGREGAR HABILIDAD AL PERFIL")
#     try:
#         id_empleado = int(input("Ingrese el ID del empleado: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     habilidad = input("Competencia o Habilidad (ej. Python, Liderazgo): ").strip()
    
#     exito, mensaje = agregar_habilidad_empleado(id_empleado, habilidad)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_habilidades_globales() -> None:
#     # Muestra un inventario de todos los skills presentes en la empresa
#     imprimir_titulo("INVENTARIO CORPORATIVO DE HABILIDADES")
#     habilidades = todas_las_habilidades()
#     if not habilidades:
#         imprimir_info("Aún no hay habilidades registradas en los perfiles.")
#     else:
#         for i, skill in enumerate(sorted(habilidades), 1):
#             print(f"  {i}. {skill}")
#     pausa()

# def opcion_habilidades_en_comun() -> None:
#     # Compara las aptitudes compartidas entre dos colaboradores
#     imprimir_titulo("SINERGIA ENTRE COLABORADORES (SKILLS EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID del primer empleado: "))
#         id_b = int(input("Ingrese el ID del segundo empleado: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = habilidades_en_comun(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Habilidades compartidas: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No hay habilidades en común o alguno de los IDs no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el resumen generado por las comprensiones de colecciones
#     imprimir_titulo("PANEL DE RECURSOS HUMANOS")
#     datos = estadisticas()
    
#     print(f"  Total de personal activo    : {datos['total_empleados']}")
#     print(f"  Gasto salarial mensual      : ${datos['gasto_salarial_mensual']}")
#     print(f"  Empleados con bono por meta : {datos['empleados_con_bono']}")
#     print(f"  Departamentos ({len(datos['departamentos_activos'])})           : {', '.join(datos['departamentos_activos'])}")
    
#     destacado = datos.get("empleado_destacado")
#     if destacado:
#         print("\n  EMPLEADO DESTACADO DEL MES:")
#         print(f"  -> {destacado['nombre']} ({destacado['departamento']}) - Puntuación: {destacado['puntuacion']}/100")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal de la aplicación
#     imprimir_info("¡Gracias por usar el Sistema de Recursos Humanos! 👋")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # El motor del menú interactivo, asegurando que cada opción apunta a una función real
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Contratar nuevo empleado", opcion_crear),
#     "2": ("Ver nómina completa", opcion_ver_todos),
#     "3": ("Buscar empleado", opcion_buscar),
#     "4": ("Ver perfil de empleado", opcion_ver_por_id),
#     "5": ("Actualizar datos de empleado", opcion_actualizar),
#     "6": ("Dar de baja a empleado", opcion_eliminar),
#     "7": ("Registrar evaluación de desempeño", opcion_agregar_evaluacion),
#     "8": ("Añadir habilidad al perfil", opcion_agregar_habilidad),
#     "9": ("Ver inventario global de habilidades", opcion_ver_habilidades_globales),
#     "10": ("Ver habilidades en común entre 2 empleados", opcion_habilidades_en_comun),
#     "11": ("Ver panel de estadísticas de RRHH", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Itera sobre el diccionario de opciones para pintar el menú
#     imprimir_titulo("SISTEMA DE GESTIÓN DE RECURSOS HUMANOS")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle principal que controla el ciclo de vida de la aplicación
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de entrada seguro
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla de configuración con los atributos de la entidad producto
# # Fuente de la verdad para generar formularios y validaciones dinámicas
# CAMPOS_PRODUCTO: tuple[str, ...] = (
#     "nombre",
#     "codigo_barras",
#     "categoria",
#     "proveedor",
#     "precio_compra",
#     "precio_venta",
#     "stock",
#     "stock_minimo",
# )

# class Producto:
#     # MODELO: Representa un artículo en el inventario de la tienda
#     # Maneja precios, control de stock, ventas (diccionarios) y etiquetas (conjuntos)
    
#     def __init__(
#         self,
#         id_producto: int,
#         nombre: str,
#         codigo_barras: str,
#         categoria: str,
#         proveedor: str,
#         precio_compra: float,
#         precio_venta: float,
#         stock: int,
#         stock_minimo: int,
#         ventas_mensuales: Optional[Dict[str, List[int]]] = None,
#         etiquetas: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor que inicializa el estado del producto
#         self.id = id_producto
#         self.nombre = nombre
#         self.codigo_barras = codigo_barras
#         self.categoria = categoria
#         self.proveedor = proveedor
#         self.precio_compra = precio_compra
#         self.precio_venta = precio_venta
#         self.stock = stock
#         self.stock_minimo = stock_minimo
        
#         # Diccionario de listas: {"Enero": [2, 1, 5], "Febrero": [10]}
#         # Registra la cantidad de unidades vendidas en cada transacción por mes
#         self.ventas_mensuales = ventas_mensuales if ventas_mensuales else {}
        
#         # Conjunto (set): Agrupa características descriptivas sin repetir (oferta, perecedero)
#         self.etiquetas = set(etiquetas) if etiquetas else set()

#     def obtener_info_basica(self) -> str:
#         # Devuelve un resumen legible del producto
#         # Se utilizará en el controlador para reportes de stock bajo y mensajes de edición
#         return f"{self.nombre} (Cód: {self.codigo_barras})"

#     def requiere_reabastecimiento(self) -> bool:
#         # Verifica si el stock actual está en o por debajo del mínimo permitido
#         # Se usará en el controlador para filtrar el reporte de alertas de inventario
#         return self.stock <= self.stock_minimo

#     def agregar_etiqueta(self, etiqueta: str) -> None:
#         # Añade una característica al producto usando el conjunto
#         # Si la etiqueta ya existe, el set la ignora automáticamente
#         self.etiquetas.add(etiqueta.title())

#     def registrar_venta(self, mes: str, cantidad: int) -> bool:
#         # Descuenta el stock y registra la transacción
#         # Retorna False si se intenta vender más de lo que hay
#         if cantidad > self.stock:
#             return False
            
#         self.stock -= cantidad
#         # setdefault crea la lista vacía si el mes no existe, luego hace append
#         self.ventas_mensuales.setdefault(mes.title(), []).append(cantidad)
#         return True

#     def total_unidades_vendidas(self) -> int:
#         # Suma todas las cantidades de todas las transacciones históricas
#         # Se usará en el controlador para el reporte de métricas globales
#         total = 0
#         for transacciones in self.ventas_mensuales.values():
#             total += sum(transacciones)
#         return total

#     def etiquetas_en_comun(self, otro_producto: "Producto") -> Set[str]:
#         # Compara las etiquetas de este producto con las de otro
#         # Retorna la intersección matemática de ambos conjuntos
#         return self.etiquetas & otro_producto.etiquetas

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa el objeto a diccionario para guardarlo en JSON
#         return {
#             "id": self.id,
#             "nombre": self.nombre,
#             "codigo_barras": self.codigo_barras,
#             "categoria": self.categoria,
#             "proveedor": self.proveedor,
#             "precio_compra": self.precio_compra,
#             "precio_venta": self.precio_venta,
#             "stock": self.stock,
#             "stock_minimo": self.stock_minimo,
#             "ventas_mensuales": self.ventas_mensuales,
#             # JSON no soporta set, lo convertimos a lista ordenada
#             "etiquetas": sorted(self.etiquetas),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Producto":
#         # Factory method: Reconstruye un objeto Producto desde el diccionario del JSON
#         return cls(
#             datos["id"],
#             datos["nombre"],
#             datos["codigo_barras"],
#             datos["categoria"],
#             datos["proveedor"],
#             float(datos["precio_compra"]),
#             float(datos["precio_venta"]),
#             int(datos["stock"]),
#             int(datos["stock_minimo"]),
#             ventas_mensuales=datos.get("ventas_mensuales", {}),
#             etiquetas=set(datos.get("etiquetas", [])),
#         )

#     def __str__(self) -> str:
#         # Representación en texto al imprimir el objeto directamente
#         alerta = " ⚠️ [STOCK BAJO]" if self.requiere_reabastecimiento() else ""
#         return f"[{self.codigo_barras}] {self.nombre} - Stock: {self.stock} | Precio: ${self.precio_venta}{alerta}"

# from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Producto, CAMPOS_PRODUCTO
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo del inventario
# gestor = GestorJSON("inventario.json")

# # Campos permitidos para el motor de búsqueda
# CAMPOS_BUSCABLES = ("nombre", "codigo_barras", "categoria", "proveedor")

# def codigos_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve un conjunto con todos los códigos de barras
#     # SE USA en crear_producto y actualizar_producto para evitar duplicidad
#     registros = gestor.leer()
#     return {str(r["codigo_barras"]).strip() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_producto(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea un nuevo artículo en el inventario aplicando validaciones
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_PRODUCTO:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 return False, f"El campo '{campo}' es obligatorio."

#         codigo = str(datos["codigo_barras"]).strip()
        
#         # AQUÍ USAMOS la función auxiliar para garantizar código único
#         if codigo in codigos_registrados():
#             return False, "El código de barras ya está registrado."

#         try:
#             precio_compra = float(datos["precio_compra"])
#             precio_venta = float(datos["precio_venta"])
#             stock = int(datos["stock"])
#             stock_minimo = int(datos["stock_minimo"])
#         except ValueError:
#             return False, "Los precios deben ser decimales y el stock números enteros."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1

#         nuevo_registro = {
#             "id": nuevo_id,
#             "nombre": datos["nombre"].strip().title(),
#             "codigo_barras": codigo,
#             "categoria": datos["categoria"].strip().title(),
#             "proveedor": datos["proveedor"].strip().title(),
#             "precio_compra": precio_compra,
#             "precio_venta": precio_venta,
#             "stock": stock,
#             "stock_minimo": stock_minimo,
#             "ventas_mensuales": {},
#             "etiquetas": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Producto registrado con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar: {error}"

# def obtener_todos() -> List[Producto]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Producto
#     return [Producto.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_producto: int) -> Optional[Producto]:
#     # Busca y devuelve un producto específico
#     # AQUÍ USAMOS obtener_todos()
#     for producto in obtener_todos():
#         if producto.id == id_producto:
#             return producto
#     return None

# def buscar_productos(termino: str) -> List[Producto]:
#     # Búsqueda difusa de productos en el catálogo
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Producto.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_producto(id_producto: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza campos validando reglas de negocio
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para no chocar con otro código de barras
#         if "codigo_barras" in cambios:
#             if str(cambios["codigo_barras"]).strip() in codigos_registrados(id_producto):
#                 return False, "Ese código de barras ya pertenece a otro artículo."

#         if any(k in cambios for k in ["precio_compra", "precio_venta", "stock", "stock_minimo"]):
#             try:
#                 if "precio_compra" in cambios: cambios["precio_compra"] = float(cambios["precio_compra"])
#                 if "precio_venta" in cambios: cambios["precio_venta"] = float(cambios["precio_venta"])
#                 if "stock" in cambios: cambios["stock"] = int(cambios["stock"])
#                 if "stock_minimo" in cambios: cambios["stock_minimo"] = int(cambios["stock_minimo"])
#             except ValueError:
#                 return False, "Valores numéricos inválidos para precios o stock."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_producto:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un producto con id {id_producto}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Producto {id_producto} actualizado correctamente."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_producto(id_producto: int) -> Tuple[bool, str]:
#     # Da de baja a un artículo del inventario
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_producto]

#     if len(quedan) == len(registros):
#         return False, f"No existe un producto con id {id_producto}"

#     gestor.guardar(quedan)
#     return True, f"Producto {id_producto} eliminado."

# def registrar_venta_producto(id_producto: int, mes: str, cantidad: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para descontar stock
#     try:
#         producto = obtener_por_id(id_producto)
#         if not producto:
#             return False, f"No existe un producto con ID {id_producto}"

#         cant_num = int(cantidad)
#         if cant_num <= 0:
#             return False, "La cantidad a vender debe ser mayor a 0."
        
#         # AQUÍ USAMOS el método del modelo registrar_venta
#         if not producto.registrar_venta(mes, cant_num):
#             return False, f"Stock insuficiente. Stock actual disponible: {producto.stock}"

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_producto:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = producto.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Venta registrada. Nuevo stock: {producto.stock}"
        
#     except ValueError:
#         return False, "La cantidad debe ser un número entero."
#     except Exception as error:
#         return False, f"Error al registrar la venta: {error}"

# def agregar_etiqueta_producto(id_producto: int, etiqueta: str) -> Tuple[bool, str]:
#     # Añade un atributo descriptivo al producto
#     producto = obtener_por_id(id_producto)
#     if not producto:
#         return False, "Producto no encontrado."
        
#     # AQUÍ USAMOS el método del modelo agregar_etiqueta
#     producto.agregar_etiqueta(etiqueta)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_producto:
#             registros[i] = producto.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Etiqueta '{etiqueta.title()}' agregada al producto."

# def todos_las_etiquetas() -> Set[str]:
#     # Devuelve un set con todas las etiquetas usadas en la tienda sin repetir
#     etiquetas_totales = set()
#     for producto in obtener_todos():
#         etiquetas_totales.update(producto.etiquetas)
#     return etiquetas_totales

# def etiquetas_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos productos y devuelve atributos compartidos
#     producto_a = obtener_por_id(id_a)
#     producto_b = obtener_por_id(id_b)
    
#     if not producto_a or not producto_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo etiquetas_en_comun
#     return producto_a.etiquetas_en_comun(producto_b)

# def productos_con_stock_critico() -> List[str]:
#     # Devuelve una lista de descripciones básicas de los productos que necesitan reabastecimiento
#     # Función auxiliar para el panel de estadísticas
#     alertas = []
#     for producto in obtener_todos():
#         # AQUÍ USAMOS requiere_reabastecimiento y obtener_info_basica del modelo
#         if producto.requiere_reabastecimiento():
#             alertas.append(f"{producto.obtener_info_basica()} (Stock: {producto.stock})")
#     return alertas

# def estadisticas() -> Dict[str, Any]:
#     # Genera métricas globales de la tienda
#     productos = obtener_todos()
    
#     categorias = {p.categoria for p in productos}
#     valor_inventario = sum(p.stock * p.precio_compra for p in productos)
    
#     # AQUÍ USAMOS total_unidades_vendidas del modelo
#     total_ventas_historicas = sum(p.total_unidades_vendidas() for p in productos)
    
#     # AQUÍ USAMOS la función de stock crítico para no dejarla suelta
#     alertas_stock = productos_con_stock_critico()

#     return {
#         "total_productos": len(productos),
#         "categorias_activas": sorted(categorias),
#         "valor_inventario": round(valor_inventario, 2),
#         "ventas_historicas": total_ventas_historicas,
#         "alertas_stock": alertas_stock
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Producto, CAMPOS_PRODUCTO
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_producto, obtener_todos, obtener_por_id, buscar_productos,
#     actualizar_producto, eliminar_producto, registrar_venta_producto,
#     agregar_etiqueta_producto, todos_las_etiquetas, etiquetas_en_comun, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(productos: List[Producto]) -> None:
#     # Imprime una tabla formateada en consola con los datos del inventario
#     print(f"{'ID':<5}{'CÓDIGO':<15}{'PRODUCTO':<25}{'CATEGORÍA':<15}{'STOCK':<8}{'PRECIO':<10}")
#     print("-" * 80)
#     for prod in productos:
#         print(f"{prod.id:<5}{prod.codigo_barras:<15}{prod.nombre[:23]:<25}{prod.categoria[:13]:<15}{prod.stock:<8}${prod.precio_venta:<9.2f}")
#     print("-" * 80)
#     imprimir_info(f"Total: {len(productos)} artículo(s)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para registrar un producto
#     imprimir_titulo("REGISTRAR NUEVO PRODUCTO")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_PRODUCTO:
#         datos[campo] = input(f"{campo.capitalize()}: ")

#     exito, mensaje = crear_producto(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra el catálogo completo usando la función del controlador
#     imprimir_titulo("CATÁLOGO GENERAL DE INVENTARIO")
#     productos = obtener_todos()
    
#     if not productos:
#         imprimir_info("No hay productos registrados. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(productos)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por texto parcial
#     imprimir_titulo("BUSCAR PRODUCTO")
#     termino = input("Ingrese nombre, código, categoría o proveedor: ")
#     encontrados = buscar_productos(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún producto coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de un artículo específico
#     imprimir_titulo("DETALLE DE PRODUCTO")
#     try:
#         id_producto = int(input("Ingrese el ID del producto: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     producto = obtener_por_id(id_producto)
#     if not producto:
#         imprimir_error(f"No existe un producto con ID {id_producto}")
#     else:
#         print("\nFICHA DEL PRODUCTO")
#         for clave, valor in producto.a_diccionario().items():
#             print(f"  {clave.upper():<18}: {valor}")
            
#         print("\nMÉTRICAS DE VENTA")
#         print(f"  UNIDADES VENDIDAS HISTÓRICAS: {producto.total_unidades_vendidas()}")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos de un artículo validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DE PRODUCTO")
#     try:
#         id_producto = int(input("Ingrese el ID del producto a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     producto = obtener_por_id(id_producto)
#     if not producto:
#         imprimir_error(f"No existe un producto con ID {id_producto}")
#         return pausa()

#     imprimir_info(f"Editando: {producto.obtener_info_basica()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_PRODUCTO:
#         actual = getattr(producto, campo)
#         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
#         if nuevo:
#             cambios[campo] = nuevo

#     exito, mensaje = actualizar_producto(id_producto, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y elimina un producto por ID a través del controlador
#     imprimir_titulo("ELIMINAR PRODUCTO DEL INVENTARIO")
#     try:
#         id_producto = int(input("Ingrese el ID del producto a eliminar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     producto = obtener_por_id(id_producto)
#     if not producto:
#         imprimir_error(f"No existe un producto con ID {id_producto}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente:\n{producto}")
    
#     if confirmar("¿Confirma la eliminación de este artículo? (si/no): "):
#         exito, mensaje = eliminar_producto(id_producto)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_registrar_venta() -> None:
#     # Interacciona con la lógica para descontar stock y registrar ingresos
#     imprimir_titulo("REGISTRAR VENTA")
#     try:
#         id_producto = int(input("Ingrese el ID del producto a vender: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     mes = input("Mes de la venta (ej. Enero): ").strip()
#     cantidad = input("Cantidad vendida: ").strip()
    
#     exito, mensaje = registrar_venta_producto(id_producto, mes, cantidad)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_agregar_etiqueta() -> None:
#     # Añade un atributo descriptivo al artículo
#     imprimir_titulo("AGREGAR ETIQUETA AL PRODUCTO")
#     try:
#         id_producto = int(input("Ingrese el ID del producto: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     etiqueta = input("Etiqueta (ej. Oferta, Perecedero, Frágil): ").strip()
    
#     exito, mensaje = agregar_etiqueta_producto(id_producto, etiqueta)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_etiquetas_globales() -> None:
#     # Muestra el inventario de todas las etiquetas usadas en la tienda
#     imprimir_titulo("ETIQUETAS ACTIVAS EN TIENDA")
#     etiquetas = todos_las_etiquetas()
#     if not etiquetas:
#         imprimir_info("Aún no hay etiquetas registradas.")
#     else:
#         for i, tag in enumerate(sorted(etiquetas), 1):
#             print(f"  {i}. {tag}")
#     pausa()

# def opcion_etiquetas_en_comun() -> None:
#     # Compara las etiquetas compartidas entre dos productos
#     imprimir_titulo("ANÁLISIS DE PRODUCTOS (ETIQUETAS EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID del primer producto: "))
#         id_b = int(input("Ingrese el ID del segundo producto: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = etiquetas_en_comun(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Etiquetas compartidas: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No hay etiquetas en común o alguno de los IDs no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el panel gerencial de la tienda
#     imprimir_titulo("PANEL DE ESTADÍSTICAS DEL INVENTARIO")
#     datos = estadisticas()
    
#     print(f"  Total de artículos distintos : {datos['total_productos']}")
#     print(f"  Valor del inventario actual  : ${datos['valor_inventario']}")
#     print(f"  Unidades vendidas en total   : {datos['ventas_historicas']}")
#     print(f"  Categorías ({len(datos['categorias_activas'])})               : {', '.join(datos['categorias_activas'])}")
    
#     alertas = datos.get("alertas_stock", [])
#     if alertas:
#         print(f"\n  ⚠️ ALERTA: {len(alertas)} PRODUCTO(S) CON STOCK BAJO")
#         for alerta in alertas:
#             print(f"  -> {alerta}")
#     else:
#         print("\n  ✅ Inventario saludable, ningún producto con stock bajo.")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal
#     imprimir_info("¡Gracias por usar el Sistema de Tienda! 👋")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # Asegura que cada opción apunta a una función real y que ninguna quede como código muerto
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Registrar nuevo producto", opcion_crear),
#     "2": ("Ver inventario completo", opcion_ver_todos),
#     "3": ("Buscar producto", opcion_buscar),
#     "4": ("Ver detalle de producto", opcion_ver_por_id),
#     "5": ("Actualizar datos de producto", opcion_actualizar),
#     "6": ("Eliminar producto", opcion_eliminar),
#     "7": ("Registrar venta (Descontar stock)", opcion_registrar_venta),
#     "8": ("Añadir etiqueta descriptiva", opcion_agregar_etiqueta),
#     "9": ("Ver todas las etiquetas del negocio", opcion_ver_etiquetas_globales),
#     "10": ("Comparar etiquetas entre 2 productos", opcion_etiquetas_en_comun),
#     "11": ("Ver panel financiero y alertas de stock", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Itera sobre el diccionario para pintar las opciones
#     imprimir_titulo("SISTEMA DE GESTIÓN DE INVENTARIO Y VENTAS")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle principal que mantiene viva la aplicación
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de entrada seguro
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable con los datos demográficos y médicos básicos
# # Define la estructura del formulario de admisión del paciente
# CAMPOS_PACIENTE: tuple[str, ...] = (
#     "nombre",
#     "apellido",
#     "cedula",
#     "fecha_nacimiento",
#     "tipo_sangre",
#     "seguro_activo",
# )

# class Paciente:
#     # MODELO: Representa un paciente dentro de la clínica u hospital
#     # Gestiona su historial de pagos/consultas (diccionario) y alergias (conjuntos)

#     def __init__(
#         self,
#         id_paciente: int,
#         nombre: str,
#         apellido: str,
#         cedula: str,
#         fecha_nacimiento: str,
#         tipo_sangre: str,
#         seguro_activo: bool = False,
#         historial_consultas: Optional[Dict[str, List[float]]] = None,
#         alergias: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor que inicializa la ficha médica del paciente
#         self.id = id_paciente
#         self.nombre = nombre
#         self.apellido = apellido
#         self.cedula = cedula
#         self.fecha_nacimiento = fecha_nacimiento
#         self.tipo_sangre = tipo_sangre
#         self.seguro_activo = seguro_activo
        
#         # Diccionario de listas: {"Cardiologia": [50.0, 45.0], "Pediatria": [30.0]}
#         # Registra el costo de cada consulta agrupado por especialidad médica
#         self.historial_consultas = historial_consultas if historial_consultas else {}
        
#         # Conjunto (set): Contraindicaciones o alergias a medicamentos (ej. "Penicilina")
#         # El set garantiza que no se registre la misma alergia dos veces por error
#         self.alergias = set(alergias) if alergias else set()

#     def obtener_nombre_completo(self) -> str:
#         # Retorna el nombre y apellido del paciente
#         # Se usará en el controlador para mensajes de confirmación y reportes
#         return f"{self.nombre} {self.apellido}"

#     def agregar_alergia(self, alergia: str) -> None:
#         # Añade una nueva contraindicación al expediente del paciente
#         self.alergias.add(alergia.title())

#     def registrar_consulta(self, especialidad: str, costo: float) -> None:
#         # Registra una nueva cita médica y su costo
#         # setdefault busca la especialidad, si no existe crea la lista, y luego añade el costo
#         self.historial_consultas.setdefault(especialidad.title(), []).append(costo)

#     def calcular_gasto_total(self) -> float:
#         # Suma todos los costos de todas las consultas históricas del paciente
#         # Se usará en el controlador para calcular los ingresos totales del hospital
#         total = 0.0
#         for costos in self.historial_consultas.values():
#             total += sum(costos)
#         return round(total, 2)

#     def alergias_en_comun(self, otro_paciente: "Paciente") -> Set[str]:
#         # Identifica si dos pacientes comparten las mismas alergias
#         # Usa la intersección matemática de conjuntos
#         return self.alergias & otro_paciente.alergias

#     def tiene_riesgo_alergico(self) -> bool:
#         # Verifica si el paciente tiene alguna alergia registrada
#         # Se usará en estadísticas para contar pacientes de cuidado especial
#         return len(self.alergias) > 0

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa el expediente médico a diccionario para guardarlo en JSON
#         return {
#             "id": self.id,
#             "nombre": self.nombre,
#             "apellido": self.apellido,
#             "cedula": self.cedula,
#             "fecha_nacimiento": self.fecha_nacimiento,
#             "tipo_sangre": self.tipo_sangre,
#             "seguro_activo": self.seguro_activo,
#             "historial_consultas": self.historial_consultas,
#             # Se ordena alfabéticamente y se convierte a lista (JSON no soporta sets nativos)
#             "alergias": sorted(self.alergias),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Paciente":
#         # Factory method: Reconstruye un objeto Paciente desde el diccionario del archivo JSON
#         return cls(
#             datos["id"],
#             datos["nombre"],
#             datos["apellido"],
#             datos["cedula"],
#             datos["fecha_nacimiento"],
#             datos["tipo_sangre"],
#             seguro_activo=datos.get("seguro_activo", False),
#             historial_consultas=datos.get("historial_consultas", {}),
#             # Reconstruye el set de alergias a partir de la lista
#             alergias=set(datos.get("alergias", [])),
#         )

#     def __str__(self) -> str:
#         # Define cómo se muestra el paciente al imprimirlo en consola
#         alerta = " ⚠️ [ALERGIAS REGISTRADAS]" if self.tiene_riesgo_alergico() else ""
#         seguro = "🏥 Asegurado" if self.seguro_activo else "Particula"
#         return f"[{self.cedula}] {self.obtener_nombre_completo()} - Tipo: {self.tipo_sangre} | {seguro}{alerta}"

# from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Paciente, CAMPOS_PACIENTE
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo del hospital
# gestor = GestorJSON("pacientes.json")

# # Campos permitidos para el motor de búsqueda de expedientes
# CAMPOS_BUSCABLES = ("nombre", "apellido", "cedula", "tipo_sangre")

# def cedulas_registradas(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve un conjunto con todas las cédulas para validar unicidad
#     # SE USA en crear_paciente y actualizar_paciente
#     registros = gestor.leer()
#     return {str(r["cedula"]).strip() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_paciente(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea un nuevo expediente médico validando las reglas de negocio
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_PACIENTE:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "seguro_activo":
#                     return False, f"El campo '{campo}' es obligatorio."

#         cedula = str(datos["cedula"]).strip()
        
#         # AQUÍ USAMOS la función auxiliar para garantizar expediente único
#         if cedula in cedulas_registradas():
#             return False, "La cédula ya está registrada en otro expediente."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         seguro = bool(datos.get("seguro_activo"))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "nombre": datos["nombre"].strip().title(),
#             "apellido": datos["apellido"].strip().title(),
#             "cedula": cedula,
#             "fecha_nacimiento": datos["fecha_nacimiento"].strip(),
#             "tipo_sangre": datos["tipo_sangre"].strip().upper(),
#             "seguro_activo": seguro,
#             "historial_consultas": {},
#             "alergias": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Paciente registrado con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar paciente: {error}"

# def obtener_todos() -> List[Paciente]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Paciente
#     return [Paciente.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_paciente: int) -> Optional[Paciente]:
#     # Busca y devuelve el expediente de un paciente específico
#     # AQUÍ USAMOS obtener_todos()
#     for paciente in obtener_todos():
#         if paciente.id == id_paciente:
#             return paciente
#     return None

# def buscar_pacientes(termino: str) -> List[Paciente]:
#     # Búsqueda difusa de expedientes en el sistema hospitalario
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Paciente.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_paciente(id_paciente: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos demográficos validando reglas del hospital
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar duplicar cédulas al editar
#         if "cedula" in cambios:
#             if str(cambios["cedula"]).strip() in cedulas_registradas(id_paciente):
#                 return False, "Esa cédula ya pertenece a otro expediente médico."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_paciente:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un paciente con id {id_paciente}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Expediente del paciente {id_paciente} actualizado."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_paciente(id_paciente: int) -> Tuple[bool, str]:
#     # Da de baja un expediente del hospital
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_paciente]

#     if len(quedan) == len(registros):
#         return False, f"No existe un paciente con id {id_paciente}"

#     gestor.guardar(quedan)
#     return True, f"Expediente {id_paciente} eliminado permanentemente."

# def registrar_consulta_medica(id_paciente: int, especialidad: str, costo: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para agregar consultas
#     try:
#         paciente = obtener_por_id(id_paciente)
#         if not paciente:
#             return False, f"No existe un paciente con ID {id_paciente}"

#         costo_num = float(costo)
#         if costo_num < 0:
#             return False, "El costo de la consulta no puede ser negativo."
        
#         # AQUÍ USAMOS el método del modelo registrar_consulta
#         paciente.registrar_consulta(especialidad, costo_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_paciente:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = paciente.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Consulta en {especialidad.title()} registrada con éxito."
        
#     except ValueError:
#         return False, "El costo debe ser un valor numérico."
#     except Exception as error:
#         return False, f"Error al registrar la cita médica: {error}"

# def agregar_alergia_paciente(id_paciente: int, alergia: str) -> Tuple[bool, str]:
#     # Registra una contraindicación o alergia en el expediente
#     paciente = obtener_por_id(id_paciente)
#     if not paciente:
#         return False, "Paciente no encontrado."
        
#     # AQUÍ USAMOS el método del modelo agregar_alergia
#     paciente.agregar_alergia(alergia)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_paciente:
#             registros[i] = paciente.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Alerta de alergia a '{alergia.title()}' guardada."

# def todas_las_alergias() -> Set[str]:
#     # Devuelve un set global con todas las alergias identificadas en el hospital
#     alergias_totales = set()
#     for paciente in obtener_todos():
#         alergias_totales.update(paciente.alergias)
#     return alergias_totales

# def pacientes_con_alergias_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos expedientes y devuelve contraindicaciones compartidas
#     paciente_a = obtener_por_id(id_a)
#     paciente_b = obtener_por_id(id_b)
    
#     if not paciente_a or not paciente_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo alergias_en_comun
#     return paciente_a.alergias_en_comun(paciente_b)

# def listado_pacientes_riesgo() -> List[str]:
#     # Genera una lista de nombres de pacientes que requieren atención especial por alergias
#     # SE USA internamente en la función de estadísticas para no dejar código huérfano
#     nombres = []
#     for paciente in obtener_todos():
#         # AQUÍ USAMOS tiene_riesgo_alergico y obtener_nombre_completo del modelo
#         if paciente.tiene_riesgo_alergico():
#             nombres.append(f"{paciente.obtener_nombre_completo()} (Cédula: {paciente.cedula})")
#     return nombres

# def estadisticas() -> Dict[str, Any]:
#     # Genera el panel de métricas administrativas del hospital
#     pacientes = obtener_todos()
    
#     tipos_sangre = {p.tipo_sangre for p in pacientes}
    
#     # AQUÍ USAMOS calcular_gasto_total del modelo para totalizar ingresos
#     ingresos_totales = sum(p.calcular_gasto_total() for p in pacientes)
    
#     pacientes_asegurados = sum(1 for p in pacientes if p.seguro_activo)
    
#     # AQUÍ USAMOS la función de riesgo para completar el reporte
#     pacientes_riesgo = listado_pacientes_riesgo()

#     return {
#         "total_pacientes": len(pacientes),
#         "tipos_sangre_registrados": sorted(tipos_sangre),
#         "ingresos_consultas": round(ingresos_totales, 2),
#         "pacientes_con_seguro": pacientes_asegurados,
#         "pacientes_riesgo": pacientes_riesgo
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Paciente, CAMPOS_PACIENTE
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_paciente, obtener_todos, obtener_por_id, buscar_pacientes,
#     actualizar_paciente, eliminar_paciente, registrar_consulta_medica,
#     agregar_alergia_paciente, todas_las_alergias, pacientes_con_alergias_en_comun, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(pacientes: List[Paciente]) -> None:
#     # Imprime una tabla formateada en consola con los expedientes
#     print(f"{'ID':<5}{'CÉDULA':<15}{'NOMBRE DEL PACIENTE':<30}{'SANGRE':<10}{'SEGURO':<15}")
#     print("-" * 80)
#     for pac in pacientes:
#         seguro = "Sí" if pac.seguro_activo else "No"
#         print(f"{pac.id:<5}{pac.cedula:<15}{pac.obtener_nombre_completo()[:28]:<30}{pac.tipo_sangre:<10}{seguro:<15}")
#     print("-" * 80)
#     imprimir_info(f"Total: {len(pacientes)} paciente(s)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para registrar un paciente
#     imprimir_titulo("ADMISIÓN DE NUEVO PACIENTE")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_PACIENTE:
#         if campo == "seguro_activo":
#             datos[campo] = input("¿Tiene seguro médico activo? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize()}: ")

#     exito, mensaje = crear_paciente(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra los expedientes completos usando la función del controlador
#     imprimir_titulo("REGISTRO GLOBAL DE PACIENTES")
#     pacientes = obtener_todos()
    
#     if not pacientes:
#         imprimir_info("No hay pacientes registrados. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(pacientes)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por texto parcial
#     imprimir_titulo("BUSCAR EXPEDIENTE MÉDICO")
#     termino = input("Ingrese nombre, apellido, cédula o tipo de sangre: ")
#     encontrados = buscar_pacientes(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún paciente coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de un paciente específico
#     imprimir_titulo("FICHA MÉDICA DEL PACIENTE")
#     try:
#         id_paciente = int(input("Ingrese el ID del paciente: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     paciente = obtener_por_id(id_paciente)
#     if not paciente:
#         imprimir_error(f"No existe un paciente con ID {id_paciente}")
#     else:
#         print("\nDATOS DEMOGRÁFICOS")
#         for clave, valor in paciente.a_diccionario().items():
#             print(f"  {clave.upper():<20}: {valor}")
            
#         print("\nRESUMEN FINANCIERO")
#         print(f"  GASTO TOTAL EN CONSULTAS: ${paciente.calcular_gasto_total()}")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DEL PACIENTE")
#     try:
#         id_paciente = int(input("Ingrese el ID del paciente a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     paciente = obtener_por_id(id_paciente)
#     if not paciente:
#         imprimir_error(f"No existe un paciente con ID {id_paciente}")
#         return pausa()

#     imprimir_info(f"Editando a: {paciente.obtener_nombre_completo()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_PACIENTE:
#         actual = getattr(paciente, campo)
#         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "seguro_activo":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_paciente(id_paciente, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y elimina un expediente por ID a través del controlador
#     imprimir_titulo("DAR DE BAJA EXPEDIENTE MÉDICO")
#     try:
#         id_paciente = int(input("Ingrese el ID del paciente a eliminar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     paciente = obtener_por_id(id_paciente)
#     if not paciente:
#         imprimir_error(f"No existe un paciente con ID {id_paciente}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente:\n{paciente}")
    
#     if confirmar("¿Confirma la eliminación de este expediente? (si/no): "):
#         exito, mensaje = eliminar_paciente(id_paciente)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_registrar_consulta() -> None:
#     # Registra una nueva cita médica sumando al historial del paciente
#     imprimir_titulo("REGISTRAR CONSULTA MÉDICA")
#     try:
#         id_paciente = int(input("Ingrese el ID del paciente: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     especialidad = input("Especialidad médica (ej. Cardiología, Pediatría): ").strip()
#     costo = input("Costo de la consulta: $").strip()
    
#     exito, mensaje = registrar_consulta_medica(id_paciente, especialidad, costo)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_agregar_alergia() -> None:
#     # Añade una alerta de contraindicación al expediente
#     imprimir_titulo("AÑADIR ALERTA DE ALERGIA")
#     try:
#         id_paciente = int(input("Ingrese el ID del paciente: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     alergia = input("Nombre de la alergia o medicamento (ej. Penicilina): ").strip()
    
#     exito, mensaje = agregar_alergia_paciente(id_paciente, alergia)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_alergias_globales() -> None:
#     # Muestra un listado unificado de todas las alergias detectadas en la clínica
#     imprimir_titulo("INVENTARIO DE ALERGIAS IDENTIFICADAS")
#     alergias = todas_las_alergias()
#     if not alergias:
#         imprimir_info("Aún no hay alergias registradas en ningún expediente.")
#     else:
#         for i, alergia in enumerate(sorted(alergias), 1):
#             print(f"  {i}. {alergia}")
#     pausa()

# def opcion_alergias_en_comun() -> None:
#     # Compara contraindicaciones compartidas entre dos pacientes
#     imprimir_titulo("ANÁLISIS DE RIESGOS (ALERGIAS EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID del primer paciente: "))
#         id_b = int(input("Ingrese el ID del segundo paciente: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = pacientes_con_alergias_en_comun(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Alergias compartidas: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No hay alergias en común o alguno de los IDs no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el panel gerencial del hospital
#     imprimir_titulo("PANEL DE ESTADÍSTICAS DEL HOSPITAL")
#     datos = estadisticas()
    
#     print(f"  Total de pacientes ingresados : {datos['total_pacientes']}")
#     print(f"  Ingresos totales por consultas: ${datos['ingresos_consultas']}")
#     print(f"  Pacientes con seguro médico   : {datos['pacientes_con_seguro']}")
#     print(f"  Grupos sanguíneos registrados ({len(datos['tipos_sangre_registrados'])}) : {', '.join(datos['tipos_sangre_registrados'])}")
    
#     pacientes_riesgo = datos.get("pacientes_riesgo", [])
#     if pacientes_riesgo:
#         print(f"\n  ⚠️ ALERTA: {len(pacientes_riesgo)} PACIENTE(S) CON ALERGIAS REGISTRADAS")
#         for paciente in pacientes_riesgo:
#             print(f"  -> {paciente}")
#     else:
#         print("\n  ✅ No hay pacientes con riesgos alérgicos registrados.")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal de la aplicación
#     imprimir_info("¡Gracias por usar el Sistema de Gestión Hospitalaria! 👋")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # El núcleo del menú: cada opción invoca una función específica asegurando cero código muerto
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Admitir nuevo paciente", opcion_crear),
#     "2": ("Ver todos los expedientes", opcion_ver_todos),
#     "3": ("Buscar paciente", opcion_buscar),
#     "4": ("Ver ficha médica completa", opcion_ver_por_id),
#     "5": ("Actualizar datos demográficos", opcion_actualizar),
#     "6": ("Dar de baja expediente", opcion_eliminar),
#     "7": ("Registrar consulta médica", opcion_registrar_consulta),
#     "8": ("Añadir alerta de alergia", opcion_agregar_alergia),
#     "9": ("Ver listado global de alergias", opcion_ver_alergias_globales),
#     "10": ("Analizar alergias compartidas entre 2 pacientes", opcion_alergias_en_comun),
#     "11": ("Ver panel de estadísticas del hospital", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Pinta las opciones del menú dinámicamente
#     imprimir_titulo("SISTEMA DE GESTIÓN HOSPITALARIA")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle infinito que mantiene la app corriendo hasta elegir Salir
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de ejecución
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable con los datos del socio
# # Define la estructura del formulario de inscripción
# CAMPOS_SOCIO: tuple[str, ...] = (
#     "nombre",
#     "apellido",
#     "cedula",
#     "tipo_membresia",
#     "fecha_ingreso",
#     "cuota_al_dia",
# )

# class Socio:
#     # MODELO: Representa a un cliente o miembro del gimnasio
#     # Gestiona sus asistencias (diccionarios) y clases/disciplinas (conjuntos)

#     def __init__(
#         self,
#         id_socio: int,
#         nombre: str,
#         apellido: str,
#         cedula: str,
#         tipo_membresia: str,
#         fecha_ingreso: str,
#         cuota_al_dia: bool = True,
#         registros_asistencia: Optional[Dict[str, List[int]]] = None,
#         disciplinas: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor que inicializa la ficha del miembro del gimnasio
#         self.id = id_socio
#         self.nombre = nombre
#         self.apellido = apellido
#         self.cedula = cedula
#         self.tipo_membresia = tipo_membresia
#         self.fecha_ingreso = fecha_ingreso
#         self.cuota_al_dia = cuota_al_dia
        
#         # Diccionario de listas: {"Enero": [1, 5, 12, 15], "Febrero": [2, 4]}
#         # Registra los días del mes en los que el socio asistió a entrenar
#         self.registros_asistencia = registros_asistencia if registros_asistencia else {}
        
#         # Conjunto (set): Clases matriculadas (ej. "Crossfit", "Spinning")
#         # El set evita que se matricule a la misma clase más de una vez
#         self.disciplinas = set(disciplinas) if disciplinas else set()

#     def obtener_nombre_completo(self) -> str:
#         # Retorna el nombre y apellido concatenados
#         # Se usará en el controlador para generar la lista de deudores y reportes
#         return f"{self.nombre} {self.apellido}"

#     def requiere_pago(self) -> bool:
#         # Verifica si el socio tiene la mensualidad vencida
#         # Se usará en las estadísticas para contar cuántos socios deben pagar
#         return not self.cuota_al_dia

#     def inscribir_disciplina(self, disciplina: str) -> None:
#         # Añade una nueva clase al perfil del socio
#         self.disciplinas.add(disciplina.title())

#     def registrar_asistencia(self, mes: str, dia: int) -> None:
#         # Marca un día de entrenamiento en un mes específico
#         # setdefault busca el mes; si no existe crea la lista, y luego añade el día
#         self.registros_asistencia.setdefault(mes.title(), []).append(dia)

#     def total_asistencias_historicas(self) -> int:
#         # Suma todos los días que el socio ha ido al gimnasio en total
#         # Se usará en el controlador para premiar al socio más activo
#         total = 0
#         for dias in self.registros_asistencia.values():
#             total += len(dias)
#         return total

#     def disciplinas_en_comun(self, otro_socio: "Socio") -> Set[str]:
#         # Identifica si dos socios asisten a las mismas clases
#         # Usa la intersección matemática de conjuntos
#         return self.disciplinas & otro_socio.disciplinas

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa el perfil del socio a diccionario para guardarlo en JSON
#         return {
#             "id": self.id,
#             "nombre": self.nombre,
#             "apellido": self.apellido,
#             "cedula": self.cedula,
#             "tipo_membresia": self.tipo_membresia,
#             "fecha_ingreso": self.fecha_ingreso,
#             "cuota_al_dia": self.cuota_al_dia,
#             "registros_asistencia": self.registros_asistencia,
#             # Se ordena alfabéticamente y se convierte a lista (JSON no soporta sets nativos)
#             "disciplinas": sorted(self.disciplinas),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Socio":
#         # Factory method: Reconstruye un objeto Socio desde el diccionario del archivo JSON
#         return cls(
#             datos["id"],
#             datos["nombre"],
#             datos["apellido"],
#             datos["cedula"],
#             datos["tipo_membresia"],
#             datos["fecha_ingreso"],
#             cuota_al_dia=datos.get("cuota_al_dia", True),
#             registros_asistencia=datos.get("registros_asistencia", {}),
#             # Reconstruye el set de disciplinas a partir de la lista
#             disciplinas=set(datos.get("disciplinas", [])),
#         )

#     def __str__(self) -> str:
#         # Define cómo se muestra el socio al imprimirlo en consola
#         estado = "✅ Al día" if self.cuota_al_dia else "❌ Pago pendiente"
#         return f"[{self.cedula}] {self.obtener_nombre_completo()} - Membresía: {self.tipo_membresia} | {estado}"

# from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Socio, CAMPOS_SOCIO
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo del gimnasio
# gestor = GestorJSON("gimnasio.json")

# # Campos permitidos para el motor de búsqueda de miembros
# CAMPOS_BUSCABLES = ("nombre", "apellido", "cedula", "tipo_membresia")

# def cedulas_registradas(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve todas las cédulas para validar unicidad de miembros
#     # SE USA en crear_socio y actualizar_socio
#     registros = gestor.leer()
#     return {str(r["cedula"]).strip() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_socio(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea un nuevo perfil de socio validando las reglas del gimnasio
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_SOCIO:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "cuota_al_dia":
#                     return False, f"El campo '{campo}' es obligatorio."

#         cedula = str(datos["cedula"]).strip()
        
#         # AQUÍ USAMOS la función auxiliar para evitar duplicar inscripciones
#         if cedula in cedulas_registradas():
#             return False, "La cédula ya está registrada en otro socio."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         cuota = bool(datos.get("cuota_al_dia", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "nombre": datos["nombre"].strip().title(),
#             "apellido": datos["apellido"].strip().title(),
#             "cedula": cedula,
#             "tipo_membresia": datos["tipo_membresia"].strip().title(),
#             "fecha_ingreso": datos["fecha_ingreso"].strip(),
#             "cuota_al_dia": cuota,
#             "registros_asistencia": {},
#             "disciplinas": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Socio inscrito con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar socio: {error}"

# def obtener_todos() -> List[Socio]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Socio
#     return [Socio.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_socio: int) -> Optional[Socio]:
#     # Busca y devuelve el perfil de un socio específico
#     # AQUÍ USAMOS obtener_todos()
#     for socio in obtener_todos():
#         if socio.id == id_socio:
#             return socio
#     return None

# def buscar_socios(termino: str) -> List[Socio]:
#     # Búsqueda difusa de miembros en la base de datos
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Socio.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_socio(id_socio: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos del socio validando reglas del club
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar conflictos de cédula al editar
#         if "cedula" in cambios:
#             if str(cambios["cedula"]).strip() in cedulas_registradas(id_socio):
#                 return False, "Esa cédula ya pertenece a otro socio."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_socio:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un socio con id {id_socio}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Perfil del socio {id_socio} actualizado."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_socio(id_socio: int) -> Tuple[bool, str]:
#     # Da de baja a un socio del gimnasio
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_socio]

#     if len(quedan) == len(registros):
#         return False, f"No existe un socio con id {id_socio}"

#     gestor.guardar(quedan)
#     return True, f"Socio {id_socio} eliminado permanentemente."

# def registrar_asistencia_socio(id_socio: int, mes: str, dia: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para sumar días de entrenamiento
#     try:
#         socio = obtener_por_id(id_socio)
#         if not socio:
#             return False, f"No existe un socio con ID {id_socio}"

#         dia_num = int(dia)
#         if not (1 <= dia_num <= 31):
#             return False, "El día debe estar entre 1 y 31."
        
#         # AQUÍ USAMOS el método del modelo registrar_asistencia
#         socio.registrar_asistencia(mes, dia_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_socio:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = socio.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Asistencia registrada para el {dia_num} de {mes.title()}."
        
#     except ValueError:
#         return False, "El día debe ser un valor numérico entero."
#     except Exception as error:
#         return False, f"Error al registrar la asistencia: {error}"

# def inscribir_disciplina_socio(id_socio: int, disciplina: str) -> Tuple[bool, str]:
#     # Matricula al cliente en una nueva clase
#     socio = obtener_por_id(id_socio)
#     if not socio:
#         return False, "Socio no encontrado."
        
#     # AQUÍ USAMOS el método del modelo inscribir_disciplina
#     socio.inscribir_disciplina(disciplina)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_socio:
#             registros[i] = socio.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Socio inscrito en la clase de '{disciplina.title()}'."

# def todas_las_disciplinas() -> Set[str]:
#     # Devuelve un set global con todas las clases que se imparten (según demanda)
#     disciplinas_totales = set()
#     for socio in obtener_todos():
#         disciplinas_totales.update(socio.disciplinas)
#     return disciplinas_totales

# def socios_disciplinas_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos clientes y devuelve las clases que comparten
#     socio_a = obtener_por_id(id_a)
#     socio_b = obtener_por_id(id_b)
    
#     if not socio_a or not socio_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo disciplinas_en_comun
#     return socio_a.disciplinas_en_comun(socio_b)

# def socio_mas_activo() -> Optional[Dict[str, Any]]:
#     # Busca al cliente con más días de entrenamiento registrados
#     # SE USA internamente en la función de estadísticas
#     socios = obtener_todos()
#     if not socios:
#         return None
    
#     # AQUÍ USAMOS total_asistencias_historicas del modelo para buscar al máximo
#     mejor = max(socios, key=lambda s: s.total_asistencias_historicas())
    
#     # AQUÍ USAMOS obtener_nombre_completo del modelo
#     return {
#         "nombre": mejor.obtener_nombre_completo(),
#         "asistencias": mejor.total_asistencias_historicas()
#     }

# def listado_deudores() -> List[str]:
#     # Genera una lista de nombres de socios que deben pagar la mensualidad
#     # SE USA internamente en las estadísticas
#     nombres = []
#     for socio in obtener_todos():
#         # AQUÍ USAMOS requiere_pago y obtener_nombre_completo del modelo
#         if socio.requiere_pago():
#             nombres.append(f"{socio.obtener_nombre_completo()} (Cédula: {socio.cedula})")
#     return nombres

# def estadisticas() -> Dict[str, Any]:
#     # Genera el panel de métricas administrativas del gimnasio
#     socios = obtener_todos()
    
#     membresias = {s.tipo_membresia for s in socios}
    
#     # AQUÍ USAMOS la función del socio más activo
#     activo = socio_mas_activo()
    
#     # AQUÍ USAMOS la función de deudores
#     deudores = listado_deudores()

#     return {
#         "total_socios": len(socios),
#         "tipos_membresia": sorted(membresias),
#         "socio_mas_activo": activo,
#         "deudores": deudores
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Socio, CAMPOS_SOCIO
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_socio, obtener_todos, obtener_por_id, buscar_socios,
#     actualizar_socio, eliminar_socio, registrar_asistencia_socio,
#     inscribir_disciplina_socio, todas_las_disciplinas, socios_disciplinas_en_comun, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(socios: List[Socio]) -> None:
#     # Imprime una tabla formateada en consola con los miembros del gimnasio
#     print(f"{'ID':<5}{'CÉDULA':<15}{'NOMBRE DEL SOCIO':<30}{'MEMBRESÍA':<15}{'ESTADO':<15}")
#     print("-" * 80)
#     for socio in socios:
#         estado = "Al día" if socio.cuota_al_dia else "Pendiente"
#         print(f"{socio.id:<5}{socio.cedula:<15}{socio.obtener_nombre_completo()[:28]:<30}{socio.tipo_membresia[:13]:<15}{estado:<15}")
#     print("-" * 80)
#     imprimir_info(f"Total: {len(socios)} socio(s)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para inscribir un socio
#     imprimir_titulo("INSCRIPCIÓN DE NUEVO SOCIO")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_SOCIO:
#         if campo == "cuota_al_dia":
#             datos[campo] = input("¿El socio pagó la cuota de ingreso? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize()}: ")

#     exito, mensaje = crear_socio(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra la lista de miembros usando la función del controlador
#     imprimir_titulo("LISTADO GENERAL DE SOCIOS")
#     socios = obtener_todos()
    
#     if not socios:
#         imprimir_info("No hay socios registrados. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(socios)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por texto parcial
#     imprimir_titulo("BUSCAR SOCIO")
#     termino = input("Ingrese nombre, apellido, cédula o membresía: ")
#     encontrados = buscar_socios(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún socio coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de un cliente específico
#     imprimir_titulo("PERFIL DEL SOCIO")
#     try:
#         id_socio = int(input("Ingrese el ID del socio: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     socio = obtener_por_id(id_socio)
#     if not socio:
#         imprimir_error(f"No existe un socio con ID {id_socio}")
#     else:
#         print("\nDATOS PERSONALES Y MEMBRESÍA")
#         for clave, valor in socio.a_diccionario().items():
#             print(f"  {clave.upper():<22}: {valor}")
            
#         print("\nRENDIMIENTO DEPORTIVO")
#         print(f"  DÍAS TOTALES ENTRENADOS : {socio.total_asistencias_historicas()}")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DEL SOCIO")
#     try:
#         id_socio = int(input("Ingrese el ID del socio a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     socio = obtener_por_id(id_socio)
#     if not socio:
#         imprimir_error(f"No existe un socio con ID {id_socio}")
#         return pausa()

#     imprimir_info(f"Editando a: {socio.obtener_nombre_completo()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_SOCIO:
#         actual = getattr(socio, campo)
#         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "cuota_al_dia":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_socio(id_socio, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y da de baja a un socio por ID a través del controlador
#     imprimir_titulo("DAR DE BAJA A SOCIO")
#     try:
#         id_socio = int(input("Ingrese el ID del socio a dar de baja: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     socio = obtener_por_id(id_socio)
#     if not socio:
#         imprimir_error(f"No existe un socio con ID {id_socio}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente:\n{socio}")
    
#     if confirmar("¿Confirma la baja de este socio? (si/no): "):
#         exito, mensaje = eliminar_socio(id_socio)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_registrar_asistencia() -> None:
#     # Registra un día de entrenamiento en el historial del socio
#     imprimir_titulo("REGISTRAR ASISTENCIA")
#     try:
#         id_socio = int(input("Ingrese el ID del socio: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     mes = input("Mes (ej. Enero, Febrero): ").strip()
#     dia = input("Día del mes (número): ").strip()
    
#     exito, mensaje = registrar_asistencia_socio(id_socio, mes, dia)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_inscribir_disciplina() -> None:
#     # Matricula al socio en una nueva clase deportiva
#     imprimir_titulo("INSCRIBIR EN CLASE / DISCIPLINA")
#     try:
#         id_socio = int(input("Ingrese el ID del socio: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     disciplina = input("Nombre de la clase (ej. Crossfit, Yoga, Boxeo): ").strip()
    
#     exito, mensaje = inscribir_disciplina_socio(id_socio, disciplina)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_disciplinas_globales() -> None:
#     # Muestra un listado unificado de todas las clases que toman los socios
#     imprimir_titulo("DISCIPLINAS ACTIVAS EN EL GIMNASIO")
#     disciplinas = todas_las_disciplinas()
#     if not disciplinas:
#         imprimir_info("Aún no hay socios inscritos en disciplinas.")
#     else:
#         for i, disciplina in enumerate(sorted(disciplinas), 1):
#             print(f"  {i}. {disciplina}")
#     pausa()

# def opcion_disciplinas_en_comun() -> None:
#     # Compara clases compartidas entre dos miembros
#     imprimir_titulo("COMPAÑEROS DE ENTRENAMIENTO (CLASES EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID del primer socio: "))
#         id_b = int(input("Ingrese el ID del segundo socio: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = socios_disciplinas_en_comun(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Disciplinas que entrenan juntos: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No coinciden en ninguna clase o algún ID no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el panel gerencial del club deportivo
#     imprimir_titulo("PANEL DE CONTROL DEL GIMNASIO")
#     datos = estadisticas()
    
#     print(f"  Total de socios activos         : {datos['total_socios']}")
#     print(f"  Tipos de membresías ({len(datos['tipos_membresia'])})          : {', '.join(datos['tipos_membresia'])}")
    
#     activo = datos.get("socio_mas_activo")
#     if activo:
#         print("\n  🏆 SOCIO MÁS CONSTANTE:")
#         print(f"  -> {activo['nombre']} con {activo['asistencias']} asistencias en total.")
    
#     deudores = datos.get("deudores", [])
#     if deudores:
#         print(f"\n  ❌ ATENCIÓN: {len(deudores)} SOCIO(S) CON PAGOS PENDIENTES")
#         for deudor in deudores:
#             print(f"  -> {deudor}")
#     else:
#         print("\n  ✅ Finanzas saludables, todos los socios están al día.")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal de la aplicación
#     imprimir_info("¡Gracias por usar el Sistema de Gestión del Gimnasio! 💪")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # El núcleo del menú: cada opción invoca una función específica para garantizar cero código muerto
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Inscribir nuevo socio", opcion_crear),
#     "2": ("Ver listado de socios", opcion_ver_todos),
#     "3": ("Buscar socio", opcion_buscar),
#     "4": ("Ver perfil completo del socio", opcion_ver_por_id),
#     "5": ("Actualizar datos de membresía", opcion_actualizar),
#     "6": ("Dar de baja a un socio", opcion_eliminar),
#     "7": ("Registrar día de asistencia", opcion_registrar_asistencia),
#     "8": ("Inscribir en clase/disciplina", opcion_inscribir_disciplina),
#     "9": ("Ver todas las disciplinas activas", opcion_ver_disciplinas_globales),
#     "10": ("Ver clases en común entre 2 socios", opcion_disciplinas_en_comun),
#     "11": ("Ver panel de control (Finanzas y Asistencia)", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Pinta las opciones del menú dinámicamente
#     imprimir_titulo("SISTEMA DE GESTIÓN DE GIMNASIO")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle infinito que mantiene la app corriendo hasta elegir Salir
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de ejecución
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable con los datos básicos de la habitación
# # Sirve como base para la creación y validación de formularios
# CAMPOS_HABITACION: tuple[str, ...] = (
#     "numero_habitacion",
#     "tipo",
#     "piso",
#     "precio_noche",
#     "disponible",
# )

# class Habitacion:
#     # MODELO: Representa una habitación dentro del hotel
#     # Gestiona su historial de ocupación (diccionarios) y comodidades (conjuntos)

#     def __init__(
#         self,
#         id_habitacion: int,
#         numero_habitacion: str,
#         tipo: str,
#         piso: int,
#         precio_noche: float,
#         disponible: bool = True,
#         reservas_por_mes: Optional[Dict[str, List[int]]] = None,
#         amenidades: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor que inicializa el estado de la habitación
#         self.id = id_habitacion
#         self.numero_habitacion = numero_habitacion
#         self.tipo = tipo
#         self.piso = piso
#         self.precio_noche = precio_noche
#         self.disponible = disponible
        
#         # Diccionario de listas: {"Enero": [3, 2, 5], "Febrero": [1, 4]}
#         # Registra la cantidad de noches que un huésped se quedó en cada reserva por mes
#         self.reservas_por_mes = reservas_por_mes if reservas_por_mes else {}
        
#         # Conjunto (set): Comodidades incluidas (ej. "WiFi", "Jacuzzi", "Balcón")
#         # El set evita que se registre la misma comodidad dos veces
#         self.amenidades = set(amenidades) if amenidades else set()

#     def obtener_info_basica(self) -> str:
#         # Retorna un resumen legible de la habitación
#         # Se usará en el controlador para reportar la habitación más rentable
#         return f"Hab. {self.numero_habitacion} ({self.tipo})"

#     def esta_libre(self) -> bool:
#         # Verifica si la habitación puede recibir huéspedes actualmente
#         # Se usará para filtrar las habitaciones disponibles en las estadísticas
#         return self.disponible

#     def agregar_amenidad(self, amenidad: str) -> None:
#         # Añade una nueva comodidad a la habitación
#         self.amenidades.add(amenidad.title())

#     def registrar_estadia(self, mes: str, noches: int) -> None:
#         # Registra una nueva reserva indicando cuántas noches se quedó el huésped
#         # setdefault busca el mes; si no existe crea la lista, y luego añade las noches
#         self.reservas_por_mes.setdefault(mes.title(), []).append(noches)

#     def calcular_ingresos_historicos(self) -> float:
#         # Suma todas las noches reservadas en la historia y las multiplica por el precio
#         # Se usará en el controlador para calcular las finanzas del hotel
#         total_noches = 0
#         for reservas in self.reservas_por_mes.values():
#             total_noches += sum(reservas)
            
#         return round(total_noches * self.precio_noche, 2)

#     def amenidades_en_comun(self, otra_habitacion: "Habitacion") -> Set[str]:
#         # Identifica qué comodidades comparten dos habitaciones
#         # Usa la intersección matemática de conjuntos
#         return self.amenidades & otra_habitacion.amenidades

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa los datos de la habitación a diccionario para guardarlo en JSON
#         return {
#             "id": self.id,
#             "numero_habitacion": self.numero_habitacion,
#             "tipo": self.tipo,
#             "piso": self.piso,
#             "precio_noche": self.precio_noche,
#             "disponible": self.disponible,
#             "reservas_por_mes": self.reservas_por_mes,
#             # Se ordena alfabéticamente y se convierte a lista (JSON no soporta sets)
#             "amenidades": sorted(self.amenidades),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Habitacion":
#         # Factory method: Reconstruye un objeto Habitacion desde el diccionario del JSON
#         return cls(
#             datos["id"],
#             datos["numero_habitacion"],
#             datos["tipo"],
#             int(datos["piso"]),
#             float(datos["precio_noche"]),
#             disponible=datos.get("disponible", True),
#             reservas_por_mes=datos.get("reservas_por_mes", {}),
#             # Reconstruye el set de comodidades a partir de la lista
#             amenidades=set(datos.get("amenidades", [])),
#         )

#     def __str__(self) -> str:
#         # Define cómo se muestra la habitación al imprimirla en consola
#         estado = "✅ Disponible" if self.disponible else "❌ Ocupada/Mantenimiento"
#         return f"[{self.numero_habitacion}] Piso {self.piso} - {self.tipo} | ${self.precio_noche}/noche | {estado}"

#     from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Habitacion, CAMPOS_HABITACION
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo de reservas del hotel
# gestor = GestorJSON("hotel.json")

# # Campos permitidos para el motor de búsqueda de habitaciones
# CAMPOS_BUSCABLES = ("numero_habitacion", "tipo")

# def numeros_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve todos los números de habitación para validar unicidad
#     # SE USA en crear_habitacion y actualizar_habitacion
#     registros = gestor.leer()
#     return {str(r["numero_habitacion"]).strip().upper() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_habitacion(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea una nueva habitación validando las reglas del hotel
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_HABITACION:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "disponible":
#                     return False, f"El campo '{campo}' es obligatorio."

#         numero = str(datos["numero_habitacion"]).strip().upper()
        
#         # AQUÍ USAMOS la función auxiliar para evitar números de cuarto duplicados
#         if numero in numeros_registrados():
#             return False, "El número de habitación ya existe en el hotel."

#         try:
#             piso = int(datos["piso"])
#             precio = float(datos["precio_noche"])
#         except ValueError:
#             return False, "El piso debe ser entero y el precio un número decimal."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         disponible = bool(datos.get("disponible", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "numero_habitacion": numero,
#             "tipo": datos["tipo"].strip().title(),
#             "piso": piso,
#             "precio_noche": precio,
#             "disponible": disponible,
#             "reservas_por_mes": {},
#             "amenidades": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Habitación registrada con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar habitación: {error}"

# def obtener_todos() -> List[Habitacion]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Habitacion
#     return [Habitacion.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_habitacion: int) -> Optional[Habitacion]:
#     # Busca y devuelve los datos de una habitación específica
#     # AQUÍ USAMOS obtener_todos()
#     for habitacion in obtener_todos():
#         if habitacion.id == id_habitacion:
#             return habitacion
#     return None

# def buscar_habitaciones(termino: str) -> List[Habitacion]:
#     # Búsqueda difusa de habitaciones en el sistema
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Habitacion.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_habitacion(id_habitacion: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos de la habitación validando reglas
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar chocar con otra habitación al editar
#         if "numero_habitacion" in cambios:
#             if str(cambios["numero_habitacion"]).strip().upper() in numeros_registrados(id_habitacion):
#                 return False, "Ese número ya pertenece a otra habitación."

#         if "piso" in cambios or "precio_noche" in cambios:
#             try:
#                 if "piso" in cambios: cambios["piso"] = int(cambios["piso"])
#                 if "precio_noche" in cambios: cambios["precio_noche"] = float(cambios["precio_noche"])
#             except ValueError:
#                 return False, "Valores numéricos inválidos para piso o precio."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_habitacion:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe una habitación con id {id_habitacion}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Habitación {id_habitacion} actualizada correctamente."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_habitacion(id_habitacion: int) -> Tuple[bool, str]:
#     # Da de baja una habitación (por remodelación o cierre)
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_habitacion]

#     if len(quedan) == len(registros):
#         return False, f"No existe una habitación con id {id_habitacion}"

#     gestor.guardar(quedan)
#     return True, f"Habitación {id_habitacion} eliminada del sistema."

# def registrar_estadia_habitacion(id_habitacion: int, mes: str, noches: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para sumar noches de ocupación
#     try:
#         habitacion = obtener_por_id(id_habitacion)
#         if not habitacion:
#             return False, f"No existe una habitación con ID {id_habitacion}"

#         noches_num = int(noches)
#         if noches_num <= 0:
#             return False, "La cantidad de noches debe ser mayor a 0."
        
#         # AQUÍ USAMOS el método del modelo registrar_estadia
#         habitacion.registrar_estadia(mes, noches_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_habitacion:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = habitacion.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Reserva de {noches_num} noche(s) en {mes.title()} registrada."
        
#     except ValueError:
#         return False, "La cantidad de noches debe ser un número entero."
#     except Exception as error:
#         return False, f"Error al registrar la estadía: {error}"

# def agregar_amenidad_habitacion(id_habitacion: int, amenidad: str) -> Tuple[bool, str]:
#     # Añade un servicio o comodidad a la habitación
#     habitacion = obtener_por_id(id_habitacion)
#     if not habitacion:
#         return False, "Habitación no encontrada."
        
#     # AQUÍ USAMOS el método del modelo agregar_amenidad
#     habitacion.agregar_amenidad(amenidad)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_habitacion:
#             registros[i] = habitacion.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Amenidad '{amenidad.title()}' agregada a la habitación."

# def todas_las_amenidades() -> Set[str]:
#     # Devuelve un set global con todas las comodidades ofrecidas en el hotel
#     amenidades_totales = set()
#     for habitacion in obtener_todos():
#         amenidades_totales.update(habitacion.amenidades)
#     return amenidades_totales

# def habitaciones_amenidades_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos cuartos y devuelve los servicios que comparten
#     habitacion_a = obtener_por_id(id_a)
#     habitacion_b = obtener_por_id(id_b)
    
#     if not habitacion_a or not habitacion_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo amenidades_en_comun
#     return habitacion_a.amenidades_en_comun(habitacion_b)

# def habitacion_mas_rentable() -> Optional[Dict[str, Any]]:
#     # Busca la habitación que más ingresos históricos ha generado
#     # SE USA internamente en la función de estadísticas
#     habitaciones = obtener_todos()
#     if not habitaciones:
#         return None
    
#     # AQUÍ USAMOS calcular_ingresos_historicos del modelo para buscar la más rentable
#     mejor = max(habitaciones, key=lambda h: h.calcular_ingresos_historicos())
    
#     # AQUÍ USAMOS obtener_info_basica del modelo
#     return {
#         "info": mejor.obtener_info_basica(),
#         "ingresos": mejor.calcular_ingresos_historicos()
#     }

# def estadisticas() -> Dict[str, Any]:
#     # Genera el panel gerencial del hotel
#     habitaciones = obtener_todos()
    
#     pisos = {h.piso for h in habitaciones}
    
#     # AQUÍ USAMOS calcular_ingresos_historicos del modelo para totalizar las finanzas globales
#     ingresos_totales = sum(h.calcular_ingresos_historicos() for h in habitaciones)
    
#     # AQUÍ USAMOS esta_libre del modelo
#     habitaciones_disponibles = sum(1 for h in habitaciones if h.esta_libre())
    
#     # AQUÍ USAMOS la función de la habitación más rentable
#     rentable = habitacion_mas_rentable()

#     return {
#         "total_habitaciones": len(habitaciones),
#         "habitaciones_disponibles": habitaciones_disponibles,
#         "pisos_activos": sorted(pisos),
#         "ingresos_totales": round(ingresos_totales, 2),
#         "habitacion_mas_rentable": rentable
#     }

# from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Habitacion, CAMPOS_HABITACION
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo de reservas del hotel
# gestor = GestorJSON("hotel.json")

# # Campos permitidos para el motor de búsqueda de habitaciones
# CAMPOS_BUSCABLES = ("numero_habitacion", "tipo")

# def numeros_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve todos los números de habitación para validar unicidad
#     # SE USA en crear_habitacion y actualizar_habitacion
#     registros = gestor.leer()
#     return {str(r["numero_habitacion"]).strip().upper() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_habitacion(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Crea una nueva habitación validando las reglas del hotel
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_HABITACION:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "disponible":
#                     return False, f"El campo '{campo}' es obligatorio."

#         numero = str(datos["numero_habitacion"]).strip().upper()
        
#         # AQUÍ USAMOS la función auxiliar para evitar números de cuarto duplicados
#         if numero in numeros_registrados():
#             return False, "El número de habitación ya existe en el hotel."

#         try:
#             piso = int(datos["piso"])
#             precio = float(datos["precio_noche"])
#         except ValueError:
#             return False, "El piso debe ser entero y el precio un número decimal."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         disponible = bool(datos.get("disponible", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "numero_habitacion": numero,
#             "tipo": datos["tipo"].strip().title(),
#             "piso": piso,
#             "precio_noche": precio,
#             "disponible": disponible,
#             "reservas_por_mes": {},
#             "amenidades": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Habitación registrada con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar habitación: {error}"

# def obtener_todos() -> List[Habitacion]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Habitacion
#     return [Habitacion.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_habitacion: int) -> Optional[Habitacion]:
#     # Busca y devuelve los datos de una habitación específica
#     # AQUÍ USAMOS obtener_todos()
#     for habitacion in obtener_todos():
#         if habitacion.id == id_habitacion:
#             return habitacion
#     return None

# def buscar_habitaciones(termino: str) -> List[Habitacion]:
#     # Búsqueda difusa de habitaciones en el sistema
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Habitacion.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_habitacion(id_habitacion: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos de la habitación validando reglas
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar chocar con otra habitación al editar
#         if "numero_habitacion" in cambios:
#             if str(cambios["numero_habitacion"]).strip().upper() in numeros_registrados(id_habitacion):
#                 return False, "Ese número ya pertenece a otra habitación."

#         if "piso" in cambios or "precio_noche" in cambios:
#             try:
#                 if "piso" in cambios: cambios["piso"] = int(cambios["piso"])
#                 if "precio_noche" in cambios: cambios["precio_noche"] = float(cambios["precio_noche"])
#             except ValueError:
#                 return False, "Valores numéricos inválidos para piso o precio."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_habitacion:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe una habitación con id {id_habitacion}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Habitación {id_habitacion} actualizada correctamente."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_habitacion(id_habitacion: int) -> Tuple[bool, str]:
#     # Da de baja una habitación (por remodelación o cierre)
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_habitacion]

#     if len(quedan) == len(registros):
#         return False, f"No existe una habitación con id {id_habitacion}"

#     gestor.guardar(quedan)
#     return True, f"Habitación {id_habitacion} eliminada del sistema."

# def registrar_estadia_habitacion(id_habitacion: int, mes: str, noches: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para sumar noches de ocupación
#     try:
#         habitacion = obtener_por_id(id_habitacion)
#         if not habitacion:
#             return False, f"No existe una habitación con ID {id_habitacion}"

#         noches_num = int(noches)
#         if noches_num <= 0:
#             return False, "La cantidad de noches debe ser mayor a 0."
        
#         # AQUÍ USAMOS el método del modelo registrar_estadia
#         habitacion.registrar_estadia(mes, noches_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_habitacion:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = habitacion.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Reserva de {noches_num} noche(s) en {mes.title()} registrada."
        
#     except ValueError:
#         return False, "La cantidad de noches debe ser un número entero."
#     except Exception as error:
#         return False, f"Error al registrar la estadía: {error}"

# def agregar_amenidad_habitacion(id_habitacion: int, amenidad: str) -> Tuple[bool, str]:
#     # Añade un servicio o comodidad a la habitación
#     habitacion = obtener_por_id(id_habitacion)
#     if not habitacion:
#         return False, "Habitación no encontrada."
        
#     # AQUÍ USAMOS el método del modelo agregar_amenidad
#     habitacion.agregar_amenidad(amenidad)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_habitacion:
#             registros[i] = habitacion.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Amenidad '{amenidad.title()}' agregada a la habitación."

# def todas_las_amenidades() -> Set[str]:
#     # Devuelve un set global con todas las comodidades ofrecidas en el hotel
#     amenidades_totales = set()
#     for habitacion in obtener_todos():
#         amenidades_totales.update(habitacion.amenidades)
#     return amenidades_totales

# def habitaciones_amenidades_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos cuartos y devuelve los servicios que comparten
#     habitacion_a = obtener_por_id(id_a)
#     habitacion_b = obtener_por_id(id_b)
    
#     if not habitacion_a or not habitacion_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo amenidades_en_comun
#     return habitacion_a.amenidades_en_comun(habitacion_b)

# def habitacion_mas_rentable() -> Optional[Dict[str, Any]]:
#     # Busca la habitación que más ingresos históricos ha generado
#     # SE USA internamente en la función de estadísticas
#     habitaciones = obtener_todos()
#     if not habitaciones:
#         return None
    
#     # AQUÍ USAMOS calcular_ingresos_historicos del modelo para buscar la más rentable
#     mejor = max(habitaciones, key=lambda h: h.calcular_ingresos_historicos())
    
#     # AQUÍ USAMOS obtener_info_basica del modelo
#     return {
#         "info": mejor.obtener_info_basica(),
#         "ingresos": mejor.calcular_ingresos_historicos()
#     }

# def estadisticas() -> Dict[str, Any]:
#     # Genera el panel gerencial del hotel
#     habitaciones = obtener_todos()
    
#     pisos = {h.piso for h in habitaciones}
    
#     # AQUÍ USAMOS calcular_ingresos_historicos del modelo para totalizar las finanzas globales
#     ingresos_totales = sum(h.calcular_ingresos_historicos() for h in habitaciones)
    
#     # AQUÍ USAMOS esta_libre del modelo
#     habitaciones_disponibles = sum(1 for h in habitaciones if h.esta_libre())
    
#     # AQUÍ USAMOS la función de la habitación más rentable
#     rentable = habitacion_mas_rentable()

#     return {
#         "total_habitaciones": len(habitaciones),
#         "habitaciones_disponibles": habitaciones_disponibles,
#         "pisos_activos": sorted(pisos),
#         "ingresos_totales": round(ingresos_totales, 2),
#         "habitacion_mas_rentable": rentable
#     }

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable con los datos básicos del vehículo
# # Servirá para iterar dinámicamente al momento de pedir datos o actualizar
# CAMPOS_VEHICULO: tuple[str, ...] = (
#     "placa",
#     "marca",
#     "modelo",
#     "anio",
#     "kilometraje",
#     "propietario",
#     "en_taller",
# )

# class Vehiculo:
#     # MODELO: Representa un vehículo registrado en el taller o concesionaria
#     # Gestiona su historial de gastos (diccionarios) y diagnósticos mecánicos (conjuntos)

#     def __init__(
#         self,
#         id_vehiculo: int,
#         placa: str,
#         marca: str,
#         modelo: str,
#         anio: int,
#         kilometraje: float,
#         propietario: str,
#         en_taller: bool = False,
#         mantenimientos: Optional[Dict[str, List[float]]] = None,
#         fallas_detectadas: Optional[Set[str]] = None,
#     ) -> None:
#         # Constructor que inicializa el estado y la ficha del vehículo
#         self.id = id_vehiculo
#         self.placa = placa
#         self.marca = marca
#         self.modelo = modelo
#         self.anio = anio
#         self.kilometraje = kilometraje
#         self.propietario = propietario
#         self.en_taller = en_taller
        
#         # Diccionario de listas: {"15-10-2026": [45.50, 120.0], "Motor": [350.0]}
#         # Registra los costos de reparación agrupados por fecha o por categoría de servicio
#         self.mantenimientos = mantenimientos if mantenimientos else {}
        
#         # Conjunto (set): Diagnósticos o averías (ej. "Fuga de aceite", "Frenos desgastados")
#         # El set garantiza que no se dupliquen las fallas diagnosticadas
#         self.fallas_detectadas = set(fallas_detectadas) if fallas_detectadas else set()

#     def obtener_info_basica(self) -> str:
#         # Retorna un resumen legible del auto
#         # Se usará en el controlador para reportar el vehículo que más ha gastado
#         return f"{self.marca} {self.modelo} ({self.anio}) - Placa: {self.placa}"

#     def requiere_cambio_aceite(self) -> bool:
#         # Lógica de negocio: Simulamos que cada vehículo requiere revisión si pasa de ciertos KMs
#         # Se usará en las estadísticas para alertar sobre autos que necesitan servicio preventivo
#         return self.kilometraje > 5000 and self.kilometraje % 5000 < 500

#     def agregar_falla(self, falla: str) -> None:
#         # Añade un nuevo diagnóstico mecánico al expediente del auto
#         self.fallas_detectadas.add(falla.title())

#     def registrar_mantenimiento(self, categoria: str, costo: float) -> None:
#         # Registra un nuevo servicio realizado y su precio
#         # setdefault busca la categoría; si no existe crea la lista, y luego añade el costo
#         self.mantenimientos.setdefault(categoria.title(), []).append(costo)

#     def calcular_gasto_total(self) -> float:
#         # Suma todos los valores invertidos en el mantenimiento histórico del vehículo
#         # Se usará en el controlador para calcular los ingresos del taller
#         total_gastado = 0.0
#         for costos in self.mantenimientos.values():
#             total_gastado += sum(costos)
            
#         return round(total_gastado, 2)

#     def fallas_en_comun(self, otro_vehiculo: "Vehiculo") -> Set[str]:
#         # Identifica qué averías comparten dos vehículos distintos
#         # Usa la intersección matemática de conjuntos, ideal para encontrar defectos de fábrica en un modelo
#         return self.fallas_detectadas & otro_vehiculo.fallas_detectadas

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa la ficha técnica del vehículo para guardarla en el JSON
#         return {
#             "id": self.id,
#             "placa": self.placa,
#             "marca": self.marca,
#             "modelo": self.modelo,
#             "anio": self.anio,
#             "kilometraje": self.kilometraje,
#             "propietario": self.propietario,
#             "en_taller": self.en_taller,
#             "mantenimientos": self.mantenimientos,
#             # Se ordena alfabéticamente y se convierte a lista (JSON no admite sets nativos)
#             "fallas_detectadas": sorted(self.fallas_detectadas),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Vehiculo":
#         # Factory method: Reconstruye un objeto Vehiculo leyendo la información del JSON
#         return cls(
#             datos["id"],
#             datos["placa"],
#             datos["marca"],
#             datos["modelo"],
#             int(datos["anio"]),
#             float(datos["kilometraje"]),
#             datos["propietario"],
#             en_taller=datos.get("en_taller", False),
#             mantenimientos=datos.get("mantenimientos", {}),
#             # Reconstruye el conjunto de fallas a partir de la lista
#             fallas_detectadas=set(datos.get("fallas_detectadas", [])),
#         )

#     def __str__(self) -> str:
#         # Representación en consola de la ficha del vehículo
#         estado = "🔧 En reparación" if self.en_taller else "🚗 Entregado / Circulando"
#         alerta = " ⚠️ [Revisar Aceite]" if self.requiere_cambio_aceite() else ""
#         return f"[{self.placa}] {self.obtener_info_basica()} | Dueño: {self.propietario} | {estado}{alerta}"

#     from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Vehiculo, CAMPOS_VEHICULO
# from shared.gestor_json import GestorJSON

# # Inicializamos el gestor apuntando al archivo del taller automotriz
# gestor = GestorJSON("taller.json")

# # Campos permitidos para el motor de búsqueda de vehículos
# CAMPOS_BUSCABLES = ("placa", "marca", "modelo", "propietario")

# def placas_registradas(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve todas las placas registradas para validar unicidad
#     # SE USA en crear_vehiculo y actualizar_vehiculo
#     registros = gestor.leer()
#     return {str(r["placa"]).strip().upper() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_vehiculo(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Registra el ingreso de un nuevo vehículo validando las reglas del taller
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_VEHICULO:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "en_taller":
#                     return False, f"El campo '{campo}' es obligatorio."

#         placa = str(datos["placa"]).strip().upper()
        
#         # AQUÍ USAMOS la función auxiliar para evitar duplicidad de placas
#         if placa in placas_registradas():
#             return False, "La placa ya está registrada en el sistema."

#         try:
#             anio = int(datos["anio"])
#             kilometraje = float(datos["kilometraje"])
#         except ValueError:
#             return False, "El año debe ser un entero y el kilometraje un número."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         en_taller = bool(datos.get("en_taller", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "placa": placa,
#             "marca": datos["marca"].strip().title(),
#             "modelo": datos["modelo"].strip().title(),
#             "anio": anio,
#             "kilometraje": kilometraje,
#             "propietario": datos["propietario"].strip().title(),
#             "en_taller": en_taller,
#             "mantenimientos": {},
#             "fallas_detectadas": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Vehículo registrado con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al registrar el vehículo: {error}"

# def obtener_todos() -> List[Vehiculo]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Vehiculo
#     return [Vehiculo.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_vehiculo: int) -> Optional[Vehiculo]:
#     # Busca y devuelve los datos de un vehículo en particular
#     # AQUÍ USAMOS obtener_todos()
#     for vehiculo in obtener_todos():
#         if vehiculo.id == id_vehiculo:
#             return vehiculo
#     return None

# def buscar_vehiculos(termino: str) -> List[Vehiculo]:
#     # Búsqueda difusa de vehículos en el taller
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Vehiculo.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_vehiculo(id_vehiculo: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos del vehículo (ej. cambio de dueño o kilometraje)
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar chocar con otra placa al editar
#         if "placa" in cambios:
#             if str(cambios["placa"]).strip().upper() in placas_registradas(id_vehiculo):
#                 return False, "Esa placa ya pertenece a otro vehículo registrado."

#         if "anio" in cambios or "kilometraje" in cambios:
#             try:
#                 if "anio" in cambios: cambios["anio"] = int(cambios["anio"])
#                 if "kilometraje" in cambios: cambios["kilometraje"] = float(cambios["kilometraje"])
#             except ValueError:
#                 return False, "Valores numéricos inválidos para año o kilometraje."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_vehiculo:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un vehículo con id {id_vehiculo}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Ficha del vehículo {id_vehiculo} actualizada."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_vehiculo(id_vehiculo: int) -> Tuple[bool, str]:
#     # Da de baja un auto del sistema del taller
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_vehiculo]

#     if len(quedan) == len(registros):
#         return False, f"No existe un vehículo con id {id_vehiculo}"

#     gestor.guardar(quedan)
#     return True, f"Vehículo {id_vehiculo} eliminado del sistema."

# def registrar_mantenimiento_vehiculo(id_vehiculo: int, categoria: str, costo: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para sumar costos de reparación
#     try:
#         vehiculo = obtener_por_id(id_vehiculo)
#         if not vehiculo:
#             return False, f"No existe un vehículo con ID {id_vehiculo}"

#         costo_num = float(costo)
#         if costo_num < 0:
#             return False, "El costo del mantenimiento no puede ser negativo."
        
#         # AQUÍ USAMOS el método del modelo registrar_mantenimiento
#         vehiculo.registrar_mantenimiento(categoria, costo_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_vehiculo:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = vehiculo.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Mantenimiento por ${costo_num} en la categoría '{categoria.title()}' registrado."
        
#     except ValueError:
#         return False, "El costo debe ser un valor numérico."
#     except Exception as error:
#         return False, f"Error al registrar el mantenimiento: {error}"

# def agregar_falla_vehiculo(id_vehiculo: int, falla: str) -> Tuple[bool, str]:
#     # Añade un diagnóstico o defecto detectado en el vehículo
#     vehiculo = obtener_por_id(id_vehiculo)
#     if not vehiculo:
#         return False, "Vehículo no encontrado."
        
#     # AQUÍ USAMOS el método del modelo agregar_falla
#     vehiculo.agregar_falla(falla)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_vehiculo:
#             registros[i] = vehiculo.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Diagnóstico '{falla.title()}' agregado al expediente."

# def todas_las_fallas() -> Set[str]:
#     # Devuelve un set global con todos los defectos mecánicos diagnosticados históricamente
#     fallas_totales = set()
#     for vehiculo in obtener_todos():
#         fallas_totales.update(vehiculo.fallas_detectadas)
#     return fallas_totales

# def vehiculos_fallas_en_comun(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos autos y devuelve las averías o defectos de fábrica que comparten
#     vehiculo_a = obtener_por_id(id_a)
#     vehiculo_b = obtener_por_id(id_b)
    
#     if not vehiculo_a or not vehiculo_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo fallas_en_comun
#     return vehiculo_a.fallas_en_comun(vehiculo_b)

# def vehiculo_mayor_gasto() -> Optional[Dict[str, Any]]:
#     # Busca el vehículo que más dinero ha invertido en reparaciones en el taller
#     # SE USA internamente en la función de estadísticas
#     vehiculos = obtener_todos()
#     if not vehiculos:
#         return None
    
#     # AQUÍ USAMOS calcular_gasto_total del modelo para la comparación
#     peor_estado = max(vehiculos, key=lambda v: v.calcular_gasto_total())
    
#     # AQUÍ USAMOS obtener_info_basica del modelo
#     return {
#         "info": peor_estado.obtener_info_basica(),
#         "gasto_total": peor_estado.calcular_gasto_total()
#     }

# def alertas_cambio_aceite() -> List[str]:
#     # Genera un listado de vehículos que requieren mantenimiento preventivo por kilometraje
#     # SE USA internamente en las estadísticas
#     alertas = []
#     for vehiculo in obtener_todos():
#         # AQUÍ USAMOS requiere_cambio_aceite y obtener_info_basica del modelo
#         if vehiculo.requiere_cambio_aceite():
#             alertas.append(f"{vehiculo.obtener_info_basica()} (KM: {vehiculo.kilometraje})")
#     return alertas

# def estadisticas() -> Dict[str, Any]:
#     # Genera el panel de facturación y diagnósticos del taller
#     vehiculos = obtener_todos()
    
#     marcas = {v.marca for v in vehiculos}
    
#     # AQUÍ USAMOS calcular_gasto_total del modelo para obtener la facturación global
#     facturacion_total = sum(v.calcular_gasto_total() for v in vehiculos)
    
#     autos_en_taller = sum(1 for v in vehiculos if v.en_taller)
    
#     # AQUÍ USAMOS las funciones dependientes para evitar código muerto
#     mayor_inversion = vehiculo_mayor_gasto()
#     alertas_mantenimiento = alertas_cambio_aceite()

#     return {
#         "total_vehiculos": len(vehiculos),
#         "autos_en_taller": autos_en_taller,
#         "marcas_atendidas": sorted(marcas),
#         "facturacion_historica": round(facturacion_total, 2),
#         "mayor_inversion": mayor_inversion,
#         "alertas_mantenimiento": alertas_mantenimiento
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Vehiculo, CAMPOS_VEHICULO
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_vehiculo, obtener_todos, obtener_por_id, buscar_vehiculos,
#     actualizar_vehiculo, eliminar_vehiculo, registrar_mantenimiento_vehiculo,
#     agregar_falla_vehiculo, todas_las_fallas, vehiculos_fallas_en_comun, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter para leer los resultados
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(vehiculos: List[Vehiculo]) -> None:
#     # Imprime una tabla estructurada en consola con los vehículos registrados
#     print(f"{'ID':<5}{'PLACA':<12}{'MARCA Y MODELO':<25}{'PROPIETARIO':<20}{'ESTADO':<15}")
#     print("-" * 80)
#     for veh in vehiculos:
#         estado = "En taller" if veh.en_taller else "Entregado"
#         vehiculo_str = f"{veh.marca} {veh.modelo}"
#         print(f"{veh.id:<5}{veh.placa:<12}{vehiculo_str[:23]:<25}{veh.propietario[:18]:<20}{estado:<15}")
#     print("-" * 80)
#     imprimir_info(f"Total: {len(vehiculos)} vehículo(s)")

# def opcion_crear() -> None:
#     # Solicita los datos y llama al controlador para ingresar un nuevo vehículo al sistema
#     imprimir_titulo("REGISTRAR INGRESO DE VEHÍCULO")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_VEHICULO:
#         if campo == "en_taller":
#             datos[campo] = input("¿El auto se queda en el taller? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize()}: ")

#     exito, mensaje = crear_vehiculo(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra el listado completo de la base de datos del taller
#     imprimir_titulo("REGISTRO GENERAL DE VEHÍCULOS")
#     vehiculos = obtener_todos()
    
#     if not vehiculos:
#         imprimir_info("No hay vehículos registrados. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(vehiculos)
#     pausa()

# def opcion_buscar() -> None:
#     # Búsqueda global por parámetros de texto
#     imprimir_titulo("BUSCAR VEHÍCULO")
#     termino = input("Ingrese placa, marca, modelo o nombre del propietario: ")
#     encontrados = buscar_vehiculos(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún vehículo coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra la ficha mecánica completa de un auto específico
#     imprimir_titulo("FICHA TÉCNICA DEL VEHÍCULO")
#     try:
#         id_vehiculo = int(input("Ingrese el ID del vehículo: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     vehiculo = obtener_por_id(id_vehiculo)
#     if not vehiculo:
#         imprimir_error(f"No existe un vehículo con ID {id_vehiculo}")
#     else:
#         print("\nINFORMACIÓN GENERAL")
#         for clave, valor in vehiculo.a_diccionario().items():
#             print(f"  {clave.upper():<20}: {valor}")
            
#         print("\nRESUMEN FINANCIERO")
#         print(f"  INVERSIÓN TOTAL EN REPARACIONES: ${vehiculo.calcular_gasto_total()}")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos validando mediante el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DE VEHÍCULO")
#     try:
#         id_vehiculo = int(input("Ingrese el ID del vehículo a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     vehiculo = obtener_por_id(id_vehiculo)
#     if not vehiculo:
#         imprimir_error(f"No existe un vehículo con ID {id_vehiculo}")
#         return pausa()

#     imprimir_info(f"Editando: {vehiculo.obtener_info_basica()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_VEHICULO:
#         actual = getattr(vehiculo, campo)
#         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "en_taller":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_vehiculo(id_vehiculo, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y da de baja un expediente mecánico a través del controlador
#     imprimir_titulo("ELIMINAR VEHÍCULO DEL SISTEMA")
#     try:
#         id_vehiculo = int(input("Ingrese el ID del vehículo a eliminar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     vehiculo = obtener_por_id(id_vehiculo)
#     if not vehiculo:
#         imprimir_error(f"No existe un vehículo con ID {id_vehiculo}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente:\n{vehiculo}")
    
#     if confirmar("¿Confirma la eliminación de este registro? (si/no): "):
#         exito, mensaje = eliminar_vehiculo(id_vehiculo)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_registrar_mantenimiento() -> None:
#     # Registra los costos de reparación para un vehículo
#     imprimir_titulo("REGISTRAR MANTENIMIENTO / REPARACIÓN")
#     try:
#         id_vehiculo = int(input("Ingrese el ID del vehículo: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     categoria = input("Categoría o repuesto (ej. Motor, Frenos, Aceite): ").strip()
#     costo = input("Costo de la reparación: $").strip()
    
#     exito, mensaje = registrar_mantenimiento_vehiculo(id_vehiculo, categoria, costo)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_agregar_falla() -> None:
#     # Añade un diagnóstico o defecto detectado
#     imprimir_titulo("AGREGAR DIAGNÓSTICO O FALLA")
#     try:
#         id_vehiculo = int(input("Ingrese el ID del vehículo: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     falla = input("Diagnóstico mecánico (ej. Fuga de refrigerante, Batería agotada): ").strip()
    
#     exito, mensaje = agregar_falla_vehiculo(id_vehiculo, falla)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_fallas_globales() -> None:
#     # Muestra el listado de todos los problemas mecánicos tratados históricamente
#     imprimir_titulo("INVENTARIO HISTÓRICO DE AVERÍAS")
#     fallas = todas_las_fallas()
#     if not fallas:
#         imprimir_info("Aún no hay fallas registradas en los expedientes.")
#     else:
#         for i, falla in enumerate(sorted(fallas), 1):
#             print(f"  {i}. {falla}")
#     pausa()

# def opcion_fallas_en_comun() -> None:
#     # Compara fallas entre dos vehículos (útil para detectar defectos de fábrica)
#     imprimir_titulo("ANÁLISIS DE DEFECTOS (FALLAS EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID del primer auto: "))
#         id_b = int(input("Ingrese el ID del segundo auto: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = vehiculos_fallas_en_comun(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Problemas mecánicos en común: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No comparten averías o algún ID no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Panel de ingresos y alertas de mantenimiento preventivo
#     imprimir_titulo("PANEL GERENCIAL DEL TALLER")
#     datos = estadisticas()
    
#     print(f"  Total de vehículos registrados  : {datos['total_vehiculos']}")
#     print(f"  Autos en reparación actualmente : {datos['autos_en_taller']}")
#     print(f"  Facturación histórica           : ${datos['facturacion_historica']}")
#     print(f"  Marcas atendidas ({len(datos['marcas_atendidas'])})             : {', '.join(datos['marcas_atendidas'])}")
    
#     peor_estado = datos.get("mayor_inversion")
#     if peor_estado:
#         print("\n  💸 VEHÍCULO CON MAYOR GASTO EN REPARACIONES:")
#         print(f"  -> {peor_estado['info']} (${peor_estado['gasto_total']} invertidos).")

#     alertas = datos.get("alertas_mantenimiento", [])
#     if alertas:
#         print(f"\n  ⚠️ ALERTA: {len(alertas)} VEHÍCULO(S) REQUIEREN CAMBIO DE ACEITE / MANTENIMIENTO")
#         for alerta in alertas:
#             print(f"  -> {alerta}")
#     else:
#         print("\n  ✅ Ningún vehículo con alertas preventivas por kilometraje.")
        
#     pausa()

# def salir() -> str:
#     # Finaliza el bucle y la ejecución de la app
#     imprimir_info("¡Gracias por usar el Sistema de Taller Mecánico! 🛠️")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # La sala de máquinas del menú interactivo: garantiza que cada vista se ejecute
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Ingresar nuevo vehículo", opcion_crear),
#     "2": ("Ver listado completo de vehículos", opcion_ver_todos),
#     "3": ("Buscar vehículo", opcion_buscar),
#     "4": ("Ver ficha técnica e historial de gastos", opcion_ver_por_id),
#     "5": ("Actualizar datos de vehículo", opcion_actualizar),
#     "6": ("Dar de baja / Eliminar expediente", opcion_eliminar),
#     "7": ("Registrar factura de reparación/mantenimiento", opcion_registrar_mantenimiento),
#     "8": ("Añadir diagnóstico mecánico", opcion_agregar_falla),
#     "9": ("Ver listado de todas las averías detectadas", opcion_ver_fallas_globales),
#     "10": ("Comparar defectos/fallas entre 2 vehículos", opcion_fallas_en_comun),
#     "11": ("Ver panel financiero y alertas preventivas", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Dibuja la lista de opciones basadas en el diccionario
#     imprimir_titulo("SISTEMA DE GESTIÓN DE TALLER MECÁNICO")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Mantiene la ejecución en un ciclo controlado
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de inicio
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable con la definicion de campos de la cuenta
# CAMPOS_CUENTA: tuple[str, ...] = (
#     "numero_cuenta",
#     "titular",
#     "cedula_titular",
#     "tipo_cuenta",
#     "saldo",
#     "activa",
# )

# class CuentaBancaria:
#     # MODELO: Representa una cuenta financiera en la institucion
#     # Gestiona movimientos historicos (diccionario de listas) y beneficios (conjuntos)

#     def __init__(
#         self,
#         id_cuenta: int,
#         numero_cuenta: str,
#         titular: str,
#         cedula_titular: str,
#         tipo_cuenta: str,
#         saldo: float,
#         activa: bool = True,
#         historial_movimientos: Optional[Dict[str, List[float]]] = None,
#         beneficios: Optional[Set[str]] = None,
#     ) -> None:
#         self.id = id_cuenta
#         self.numero_cuenta = numero_cuenta
#         self.titular = titular
#         self.cedula_titular = cedula_titular
#         self.tipo_cuenta = tipo_cuenta
#         self.saldo = saldo
#         self.activa = activa
        
#         # Diccionario de listas: {"Octubre": [500.0, -120.0, 45.0]}
#         # Registra depositos (positivos) y retiros (negativos) por mes
#         self.historial_movimientos = historial_movimientos if historial_movimientos else {}
        
#         # Conjunto (set): Beneficios asociados sin duplicados
#         self.beneficios = set(beneficios) if beneficios else set()

#     def obtener_resumen(self) -> str:
#         # Devuelve descripcion concisa de la cuenta
#         return f"Cta {self.numero_cuenta} - {self.titular} (${self.saldo:.2f})"

#     def agregar_beneficio(self, beneficio: str) -> None:
#         # Registra un beneficio o servicio adicional en la cuenta
#         self.beneficios.add(beneficio.title())

#     def registrar_transaccion(self, mes: str, monto: float) -> bool:
#         # Aplica una transaccion: monto positivo es deposito, negativo es retiro
#         # Valida que no sobregire el saldo actual
#         if monto < 0 and abs(monto) > self.saldo:
#             return False
            
#         self.saldo = round(self.saldo + monto, 2)
#         self.historial_movimientos.setdefault(mes.title(), []).append(monto)
#         return True

#     def total_movimientos_historicos(self) -> int:
#         # Cuenta la cantidad de transacciones registradas en total
#         total = 0
#         for movs in self.historial_movimientos.values():
#             total += len(movs)
#         return total

#     def beneficios_en_comun(self, otra_cuenta: "CuentaBancaria") -> Set[str]:
#         # Interseccion de conjuntos para comparar beneficios entre cuentas
#         return self.beneficios & otra_cuenta.beneficios

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Serializa el objeto a diccionario para persistencia en JSON
#         return {
#             "id": self.id,
#             "numero_cuenta": self.numero_cuenta,
#             "titular": self.titular,
#             "cedula_titular": self.cedula_titular,
#             "tipo_cuenta": self.tipo_cuenta,
#             "saldo": self.saldo,
#             "activa": self.activa,
#             "historial_movimientos": self.historial_movimientos,
#             "beneficios": sorted(self.beneficios),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "CuentaBancaria":
#         # Reconstruye la entidad desde datos deserializados
#         return cls(
#             datos["id"],
#             datos["numero_cuenta"],
#             datos["titular"],
#             datos["cedula_titular"],
#             datos["tipo_cuenta"],
#             float(datos["saldo"]),
#             activa=datos.get("activa", True),
#             historial_movimientos=datos.get("historial_movimientos", {}),
#             beneficios=set(datos.get("beneficios", [])),
#         )

#     def __str__(self) -> str:
#         estado = "Activa" if self.activa else "Bloqueada"
#         return f"[{self.numero_cuenta}] {self.titular} - {self.tipo_cuenta} | Saldo: ${self.saldo:.2f} | {estado}"

#     from typing import List, Dict, Set, Any, Optional, Tuple
# from models import CuentaBancaria, CAMPOS_CUENTA
# from shared.gestor_json import GestorJSON

# # Inicializa el gestor de archivos apuntando a la base de datos del banco
# gestor = GestorJSON("banco.json")

# # Campos permitidos para el motor de búsqueda de cuentas
# CAMPOS_BUSCABLES = ("numero_cuenta", "titular", "cedula_titular", "tipo_cuenta")

# def numeros_cuenta_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve un conjunto con todos los números de cuenta para validar unicidad
#     # SE USA en crear_cuenta y actualizar_cuenta
#     registros = gestor.leer()
#     return {str(r["numero_cuenta"]).strip() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_cuenta(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Registra una nueva cuenta bancaria aplicando las validaciones de negocio
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_CUENTA:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "activa":
#                     return False, f"El campo '{campo}' es obligatorio."

#         numero = str(datos["numero_cuenta"]).strip()
        
#         # AQUÍ USAMOS la función auxiliar para evitar duplicidad de números de cuenta
#         if numero in numeros_cuenta_registrados():
#             return False, "El número de cuenta ya está registrado en el banco."

#         try:
#             saldo = float(datos["saldo"])
#         except ValueError:
#             return False, "El saldo inicial debe ser un valor numérico."

#         if saldo < 0:
#             return False, "El saldo inicial no puede ser negativo."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         activa = bool(datos.get("activa", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "numero_cuenta": numero,
#             "titular": datos["titular"].strip().title(),
#             "cedula_titular": datos["cedula_titular"].strip(),
#             "tipo_cuenta": datos["tipo_cuenta"].strip().title(),
#             "saldo": saldo,
#             "activa": activa,
#             "historial_movimientos": {},
#             "beneficios": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Cuenta bancaria creada con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al crear la cuenta: {error}"

# def obtener_todos() -> List[CuentaBancaria]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos CuentaBancaria
#     return [CuentaBancaria.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_cuenta: int) -> Optional[CuentaBancaria]:
#     # Busca y devuelve los datos de una cuenta en particular
#     # AQUÍ USAMOS obtener_todos()
#     for cuenta in obtener_todos():
#         if cuenta.id == id_cuenta:
#             return cuenta
#     return None

# def buscar_cuentas(termino: str) -> List[CuentaBancaria]:
#     # Búsqueda difusa de cuentas por titular, cédula o número
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(CuentaBancaria.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_cuenta(id_cuenta: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos de la cuenta (ej. cambio de titular o estado)
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar conflictos con otros números de cuenta
#         if "numero_cuenta" in cambios:
#             if str(cambios["numero_cuenta"]).strip() in numeros_cuenta_registrados(id_cuenta):
#                 return False, "Ese número ya pertenece a otra cuenta."

#         if "saldo" in cambios:
#             try:
#                 cambios["saldo"] = float(cambios["saldo"])
#             except ValueError:
#                 return False, "El saldo debe ser un valor numérico."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_cuenta:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe una cuenta con id {id_cuenta}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Datos de la cuenta {id_cuenta} actualizados."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_cuenta(id_cuenta: int) -> Tuple[bool, str]:
#     # Elimina definitivamente una cuenta bancaria (cierre de cuenta)
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_cuenta]

#     if len(quedan) == len(registros):
#         return False, f"No existe una cuenta con id {id_cuenta}"

#     gestor.guardar(quedan)
#     return True, f"Cuenta {id_cuenta} cerrada y eliminada del sistema."

# def registrar_movimiento_cuenta(id_cuenta: int, mes: str, monto_str: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para aplicar depósitos o retiros
#     try:
#         cuenta = obtener_por_id(id_cuenta)
#         if not cuenta:
#             return False, f"No existe una cuenta con ID {id_cuenta}"
            
#         if not cuenta.activa:
#             return False, "La cuenta está bloqueada o inactiva."

#         monto_num = float(monto_str)
#         if monto_num == 0:
#             return False, "El monto de la transacción no puede ser cero."
        
#         # AQUÍ USAMOS el método del modelo registrar_transaccion
#         if not cuenta.registrar_transaccion(mes, monto_num):
#             return False, f"Fondos insuficientes. Saldo actual: ${cuenta.saldo:.2f}"

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_cuenta:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = cuenta.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         tipo = "Depósito" if monto_num > 0 else "Retiro"
#         return True, f"{tipo} procesado exitosamente. Nuevo saldo: ${cuenta.saldo:.2f}"
        
#     except ValueError:
#         return False, "El monto debe ser un valor numérico."
#     except Exception as error:
#         return False, f"Error al procesar la transacción: {error}"

# def agregar_beneficio_cuenta(id_cuenta: int, beneficio: str) -> Tuple[bool, str]:
#     # Activa un servicio adicional (ej. Banca Web, Cero Comisiones) en la cuenta
#     cuenta = obtener_por_id(id_cuenta)
#     if not cuenta:
#         return False, "Cuenta no encontrada."
        
#     # AQUÍ USAMOS el método del modelo agregar_beneficio
#     cuenta.agregar_beneficio(beneficio)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_cuenta:
#             registros[i] = cuenta.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Beneficio '{beneficio.title()}' activado en la cuenta."

# def todos_los_beneficios() -> Set[str]:
#     # Devuelve un set global con todos los beneficios bancarios otorgados a los clientes
#     beneficios_totales = set()
#     for cuenta in obtener_todos():
#         beneficios_totales.update(cuenta.beneficios)
#     return beneficios_totales

# def beneficios_en_comun_cuentas(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos cuentas y devuelve los servicios o ventajas que ambas tienen activos
#     cuenta_a = obtener_por_id(id_a)
#     cuenta_b = obtener_por_id(id_b)
    
#     if not cuenta_a or not cuenta_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo beneficios_en_comun
#     return cuenta_a.beneficios_en_comun(cuenta_b)

# def cuenta_mayor_actividad() -> Optional[Dict[str, Any]]:
#     # Busca la cuenta con el mayor número de transacciones históricas
#     # SE USA internamente en la función de estadísticas
#     cuentas = obtener_todos()
#     if not cuentas:
#         return None
    
#     # AQUÍ USAMOS total_movimientos_historicos del modelo para encontrar la más activa
#     mas_activa = max(cuentas, key=lambda c: c.total_movimientos_historicos())
    
#     # AQUÍ USAMOS obtener_resumen del modelo
#     return {
#         "info": mas_activa.obtener_resumen(),
#         "total_transacciones": mas_activa.total_movimientos_historicos()
#     }

# def estadisticas() -> Dict[str, Any]:
#     # Genera el reporte financiero del banco
#     cuentas = obtener_todos()
    
#     tipos_cuenta = {c.tipo_cuenta for c in cuentas}
#     fondos_totales = sum(c.saldo for c in cuentas)
#     cuentas_activas = sum(1 for c in cuentas if c.activa)
    
#     # AQUÍ USAMOS la función que identifica la cuenta más movida
#     cuenta_estrella = cuenta_mayor_actividad()

#     return {
#         "total_cuentas": len(cuentas),
#         "cuentas_activas": cuentas_activas,
#         "tipos_productos": sorted(tipos_cuenta),
#         "fondos_totales_banco": round(fondos_totales, 2),
#         "cuenta_mas_activa": cuenta_estrella
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import CuentaBancaria, CAMPOS_CUENTA
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_cuenta, obtener_todos, obtener_por_id, buscar_cuentas,
#     actualizar_cuenta, eliminar_cuenta, registrar_movimiento_cuenta,
#     agregar_beneficio_cuenta, todos_los_beneficios, beneficios_en_comun_cuentas, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(cuentas: List[CuentaBancaria]) -> None:
#     # Imprime una tabla formateada en consola con el estado de las cuentas
#     print(f"{'ID':<5}{'NÚMERO':<15}{'TITULAR':<25}{'TIPO':<15}{'SALDO':<12}{'ESTADO':<10}")
#     print("-" * 85)
#     for cta in cuentas:
#         estado = "Activa" if cta.activa else "Bloqueada"
#         print(f"{cta.id:<5}{cta.numero_cuenta:<15}{cta.titular[:23]:<25}{cta.tipo_cuenta[:13]:<15}${cta.saldo:<11.2f}{estado:<10}")
#     print("-" * 85)
#     imprimir_info(f"Total: {len(cuentas)} cuenta(s)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para abrir una cuenta
#     imprimir_titulo("APERTURA DE NUEVA CUENTA")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_CUENTA:
#         if campo == "activa":
#             datos[campo] = input("¿La cuenta estará activa inmediatamente? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize().replace('_', ' ')}: ")

#     exito, mensaje = crear_cuenta(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra el listado completo de cuentas del banco
#     imprimir_titulo("REGISTRO GENERAL DE CUENTAS")
#     cuentas = obtener_todos()
    
#     if not cuentas:
#         imprimir_info("No hay cuentas registradas. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(cuentas)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por texto parcial (número, titular, cédula)
#     imprimir_titulo("BUSCAR CUENTA BANCARIA")
#     termino = input("Ingrese número de cuenta, titular o cédula: ")
#     encontrados = buscar_cuentas(termino)

#     if not encontrados:
#         imprimir_info(f"Ninguna cuenta coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de la cuenta
#     imprimir_titulo("DETALLE DE LA CUENTA")
#     try:
#         id_cuenta = int(input("Ingrese el ID de la cuenta: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     cuenta = obtener_por_id(id_cuenta)
#     if not cuenta:
#         imprimir_error(f"No existe una cuenta con ID {id_cuenta}")
#     else:
#         print("\nDATOS DEL CLIENTE Y PRODUCTO")
#         for clave, valor in cuenta.a_diccionario().items():
#             print(f"  {clave.upper():<22}: {valor}")
            
#         print("\nACTIVIDAD FINANCIERA")
#         print(f"  TOTAL DE TRANSACCIONES HISTÓRICAS: {cuenta.total_movimientos_historicos()}")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DE LA CUENTA")
#     try:
#         id_cuenta = int(input("Ingrese el ID de la cuenta a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     cuenta = obtener_por_id(id_cuenta)
#     if not cuenta:
#         imprimir_error(f"No existe una cuenta con ID {id_cuenta}")
#         return pausa()

#     imprimir_info(f"Editando: {cuenta.obtener_resumen()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_CUENTA:
#         actual = getattr(cuenta, campo)
#         nuevo = input(f"{campo.capitalize().replace('_', ' ')} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "activa":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_cuenta(id_cuenta, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y da de baja una cuenta por ID a través del controlador
#     imprimir_titulo("CIERRE DEFINITIVO DE CUENTA")
#     try:
#         id_cuenta = int(input("Ingrese el ID de la cuenta a cerrar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     cuenta = obtener_por_id(id_cuenta)
#     if not cuenta:
#         imprimir_error(f"No existe una cuenta con ID {id_cuenta}")
#         return pausa()

#     imprimir_info(f"Se cerrará permanentemente:\n{cuenta}")
    
#     if confirmar("¿Confirma el cierre de esta cuenta? (si/no): "):
#         exito, mensaje = eliminar_cuenta(id_cuenta)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_registrar_movimiento() -> None:
#     # Registra un depósito (positivo) o retiro (negativo)
#     imprimir_titulo("REGISTRAR DEPÓSITO O RETIRO")
#     try:
#         id_cuenta = int(input("Ingrese el ID de la cuenta: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     mes = input("Mes de la transacción (ej. Octubre, Noviembre): ").strip()
#     monto = input("Monto (positivo para depósito, negativo para retiro): ").strip()
    
#     exito, mensaje = registrar_movimiento_cuenta(id_cuenta, mes, monto)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_agregar_beneficio() -> None:
#     # Añade un servicio extra a la cuenta
#     imprimir_titulo("ACTIVAR BENEFICIO EN LA CUENTA")
#     try:
#         id_cuenta = int(input("Ingrese el ID de la cuenta: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     beneficio = input("Servicio (ej. Banca Web, Cero Comisiones, Tarjeta Platino): ").strip()
    
#     exito, mensaje = agregar_beneficio_cuenta(id_cuenta, beneficio)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_beneficios_globales() -> None:
#     # Muestra un listado unificado de todos los beneficios otorgados en el banco
#     imprimir_titulo("CATÁLOGO DE SERVICIOS Y BENEFICIOS ACTIVOS")
#     beneficios = todos_los_beneficios()
#     if not beneficios:
#         imprimir_info("Aún no hay beneficios registrados en las cuentas.")
#     else:
#         for i, beneficio in enumerate(sorted(beneficios), 1):
#             print(f"  {i}. {beneficio}")
#     pausa()

# def opcion_beneficios_en_comun() -> None:
#     # Compara servicios compartidos entre dos cuentas
#     imprimir_titulo("COMPARAR CUENTAS (BENEFICIOS EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID de la primera cuenta: "))
#         id_b = int(input("Ingrese el ID de la segunda cuenta: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = beneficios_en_comun_cuentas(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Servicios que ambas comparten: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No comparten ningún beneficio o algún ID no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el panel gerencial y financiero del banco
#     imprimir_titulo("PANEL GERENCIAL DEL BANCO")
#     datos = estadisticas()
    
#     print(f"  Total de cuentas abiertas     : {datos['total_cuentas']}")
#     print(f"  Cuentas activas operando      : {datos['cuentas_activas']}")
#     print(f"  Tipos de productos ({len(datos['tipos_productos'])})         : {', '.join(datos['tipos_productos'])}")
#     print(f"  Fondos totales administrados  : ${datos['fondos_totales_banco']}")
    
#     activa = datos.get("cuenta_mas_activa")
#     if activa:
#         print("\n  🏆 CUENTA CON MAYOR MOVIMIENTO HISTÓRICO:")
#         print(f"  -> {activa['info']} con {activa['total_transacciones']} transacciones en total.")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal de la aplicación
#     imprimir_info("¡Gracias por usar el Sistema Bancario! 🏦")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # El núcleo del menú: cada opción invoca una función específica garantizando cero código inútil
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Aperturar nueva cuenta", opcion_crear),
#     "2": ("Ver todas las cuentas", opcion_ver_todos),
#     "3": ("Buscar cuenta", opcion_buscar),
#     "4": ("Ver detalles y actividad de cuenta", opcion_ver_por_id),
#     "5": ("Actualizar datos del titular", opcion_actualizar),
#     "6": ("Cerrar / Eliminar cuenta", opcion_eliminar),
#     "7": ("Registrar depósito o retiro", opcion_registrar_movimiento),
#     "8": ("Activar servicio/beneficio", opcion_agregar_beneficio),
#     "9": ("Ver catálogo de beneficios del banco", opcion_ver_beneficios_globales),
#     "10": ("Comparar beneficios entre 2 cuentas", opcion_beneficios_en_comun),
#     "11": ("Ver balance general y estadísticas", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Pinta las opciones del menú dinámicamente
#     imprimir_titulo("SISTEMA DE GESTIÓN BANCARIA")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle infinito que mantiene la app corriendo hasta elegir Salir
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de ejecución
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")

# from typing import Dict, List, Set, Any, Optional

# # Tupla inmutable con la definicion de campos para el formulario del plato
# CAMPOS_PLATO: tuple[str, ...] = (
#     "codigo",
#     "nombre",
#     "categoria",
#     "precio",
#     "tiempo_preparacion",
#     "disponible",
# )

# class Plato:
#     # MODELO: Representa un item en el menu del restaurante
#     # Gestiona historial de comandas (diccionario) y alertas alimentarias (conjuntos)

#     def __init__(
#         self,
#         id_plato: int,
#         codigo: str,
#         nombre: str,
#         categoria: str,
#         precio: float,
#         tiempo_preparacion: int,
#         disponible: bool = True,
#         pedidos_por_turno: Optional[Dict[str, List[int]]] = None,
#         alergenos: Optional[Set[str]] = None,
#     ) -> None:
#         # Inicializa las propiedades del item del menu
#         self.id = id_plato
#         self.codigo = codigo
#         self.nombre = nombre
#         self.categoria = categoria
#         self.precio = precio
#         self.tiempo_preparacion = tiempo_preparacion
#         self.disponible = disponible
        
#         # Diccionario de listas: {"Almuerzo": [2, 1, 4], "Cena": [1, 2]}
#         # Registra la cantidad de platos vendidos en cada mesa, agrupados por turno
#         self.pedidos_por_turno = pedidos_por_turno if pedidos_por_turno else {}
        
#         # Conjunto (set): Alertas dieteticas y alergenos (ej. "Gluten", "Mariscos")
#         # Previene que un mismo alergeno se registre por duplicado
#         self.alergenos = set(alergenos) if alergenos else set()

#     def obtener_resumen(self) -> str:
#         # Devuelve un texto descriptivo y corto del plato
#         # Se utilizara en los reportes del plato mas vendido
#         return f"{self.nombre} ({self.categoria})"

#     def agregar_alergeno(self, alergeno: str) -> None:
#         # Añade una advertencia de ingrediente al plato
#         self.alergenos.add(alergeno.title())

#     def registrar_pedido(self, turno: str, cantidad: int) -> None:
#         # Suma la cantidad de platos ordenados a un turno especifico
#         self.pedidos_por_turno.setdefault(turno.title(), []).append(cantidad)

#     def total_unidades_vendidas(self) -> int:
#         # Suma todas las porciones pedidas a lo largo de todos los turnos
#         total = 0
#         for cantidades in self.pedidos_por_turno.values():
#             total += sum(cantidades)
#         return total

#     def calcular_ingresos_historicos(self) -> float:
#         # Multiplica las unidades vendidas por el precio para saber la rentabilidad del plato
#         return round(self.total_unidades_vendidas() * self.precio, 2)

#     def alergenos_en_comun(self, otro_plato: "Plato") -> Set[str]:
#         # Interseccion de conjuntos para identificar si dos platos comparten restricciones dieteticas
#         return self.alergenos & otro_plato.alergenos

#     def a_diccionario(self) -> Dict[str, Any]:
#         # Convierte el objeto a diccionario para almacenarlo en JSON
#         return {
#             "id": self.id,
#             "codigo": self.codigo,
#             "nombre": self.nombre,
#             "categoria": self.categoria,
#             "precio": self.precio,
#             "tiempo_preparacion": self.tiempo_preparacion,
#             "disponible": self.disponible,
#             "pedidos_por_turno": self.pedidos_por_turno,
#             # JSON no soporta sets, se convierte a lista ordenada
#             "alergenos": sorted(self.alergenos),
#         }

#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> "Plato":
#         # Factory method: reconstruye la entidad desde los datos del archivo
#         return cls(
#             datos["id"],
#             datos["codigo"],
#             datos["nombre"],
#             datos["categoria"],
#             float(datos["precio"]),
#             int(datos["tiempo_preparacion"]),
#             disponible=datos.get("disponible", True),
#             pedidos_por_turno=datos.get("pedidos_por_turno", {}),
#             alergenos=set(datos.get("alergenos", [])),
#         )

#     def __str__(self) -> str:
#         # Representacion de consola al imprimir el menu
#         estado = "✅ Disponible" if self.disponible else "❌ Agotado"
#         riesgo = " ⚠️ [Alérgenos]" if len(self.alergenos) > 0 else ""
#         return f"[{self.codigo}] {self.nombre} ({self.tiempo_preparacion} min) | ${self.precio:.2f} | {estado}{riesgo}"

#     from typing import List, Dict, Set, Any, Optional, Tuple
# from models import Plato, CAMPOS_PLATO
# from shared.gestor_json import GestorJSON

# # Inicializa el gestor de archivos apuntando a la base de datos del restaurante
# gestor = GestorJSON("restaurante.json")

# # Campos permitidos para el motor de búsqueda en el menú
# CAMPOS_BUSCABLES = ("codigo", "nombre", "categoria")

# def codigos_registrados(excepto_id: Optional[int] = None) -> Set[str]:
#     # Función auxiliar: Devuelve un conjunto con todos los códigos de platillos para validar unicidad
#     # SE USA en crear_plato y actualizar_plato
#     registros = gestor.leer()
#     return {str(r["codigo"]).strip().upper() for r in registros if excepto_id is None or r.get("id") != excepto_id}

# def crear_plato(datos: Dict[str, Any]) -> Tuple[bool, str]:
#     # Agrega un nuevo platillo al menú aplicando las validaciones gastronómicas
#     try:
#         registros = gestor.leer()
        
#         for campo in CAMPOS_PLATO:
#             if campo not in datos or str(datos[campo]).strip() == "":
#                 if campo != "disponible":
#                     return False, f"El campo '{campo}' es obligatorio."

#         codigo = str(datos["codigo"]).strip().upper()
        
#         # AQUÍ USAMOS la función auxiliar para evitar duplicidad de códigos en la carta
#         if codigo in codigos_registrados():
#             return False, "El código ya está asignado a otro platillo."

#         try:
#             precio = float(datos["precio"])
#             tiempo = int(datos["tiempo_preparacion"])
#         except ValueError:
#             return False, "El precio debe ser decimal y el tiempo de preparación un número entero."

#         if precio < 0 or tiempo <= 0:
#             return False, "El precio y el tiempo deben ser valores positivos."

#         nuevo_id = max([r["id"] for r in registros], default=0) + 1
#         disponible = bool(datos.get("disponible", True))

#         nuevo_registro = {
#             "id": nuevo_id,
#             "codigo": codigo,
#             "nombre": datos["nombre"].strip().title(),
#             "categoria": datos["categoria"].strip().title(),
#             "precio": precio,
#             "tiempo_preparacion": tiempo,
#             "disponible": disponible,
#             "pedidos_por_turno": {},
#             "alergenos": []
#         }

#         registros.append(nuevo_registro)
#         gestor.guardar(registros)
#         return True, f"Platillo agregado al menú con éxito (ID: {nuevo_id})"

#     except Exception as error:
#         return False, f"Error inesperado al crear el platillo: {error}"

# def obtener_todos() -> List[Plato]:
#     # Lee el JSON y usa el Factory Method para instanciar objetos Plato
#     return [Plato.desde_diccionario(registro) for registro in gestor.leer()]

# def obtener_por_id(id_plato: int) -> Optional[Plato]:
#     # Busca y devuelve la receta/datos de un platillo en particular
#     # AQUÍ USAMOS obtener_todos()
#     for plato in obtener_todos():
#         if plato.id == id_plato:
#             return plato
#     return None

# def buscar_platos(termino: str) -> List[Plato]:
#     # Búsqueda difusa de platillos por código, nombre o categoría
#     termino = termino.strip().lower()
#     if not termino:
#         return []

#     encontrados = []
#     for registro in gestor.leer():
#         for campo in CAMPOS_BUSCABLES:
#             if termino in str(registro.get(campo, "")).lower():
#                 encontrados.append(Plato.desde_diccionario(registro))
#                 break  
#     return encontrados

# def actualizar_plato(id_plato: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
#     # Actualiza datos del menú (ej. cambio de precio, disponibilidad)
#     try:
#         if not cambios:
#             return False, "No se indicó ningún cambio."
                
#         # AQUÍ USAMOS la función auxiliar para evitar conflictos con otros códigos
#         if "codigo" in cambios:
#             if str(cambios["codigo"]).strip().upper() in codigos_registrados(id_plato):
#                 return False, "Ese código ya pertenece a otro platillo."

#         if "precio" in cambios or "tiempo_preparacion" in cambios:
#             try:
#                 if "precio" in cambios: cambios["precio"] = float(cambios["precio"])
#                 if "tiempo_preparacion" in cambios: cambios["tiempo_preparacion"] = int(cambios["tiempo_preparacion"])
#             except ValueError:
#                 return False, "Valores numéricos inválidos para precio o tiempo."

#         registros = gestor.leer()
#         posicion = None
#         for indice, registro in enumerate(registros):
#             if registro["id"] == id_plato:
#                 posicion = indice
#                 break

#         if posicion is None:
#             return False, f"No existe un platillo con id {id_plato}"

#         registros[posicion].update(cambios)
#         gestor.guardar(registros)
#         return True, f"Datos del platillo {id_plato} actualizados."

#     except Exception as error:
#         return False, f"Error inesperado: {error}"

# def eliminar_plato(id_plato: int) -> Tuple[bool, str]:
#     # Elimina definitivamente un platillo de la carta
#     registros = gestor.leer()
#     quedan = [registro for registro in registros if registro["id"] != id_plato]

#     if len(quedan) == len(registros):
#         return False, f"No existe un platillo con id {id_plato}"

#     gestor.guardar(quedan)
#     return True, f"Platillo {id_plato} retirado del menú."

# def registrar_comanda_plato(id_plato: int, turno: str, cantidad_str: str) -> Tuple[bool, str]:
#     # Conecta la vista con el método del modelo para sumar comandas/pedidos
#     try:
#         plato = obtener_por_id(id_plato)
#         if not plato:
#             return False, f"No existe un platillo con ID {id_plato}"
            
#         if not plato.disponible:
#             return False, "El platillo está marcado como agotado actualmente."

#         cantidad_num = int(cantidad_str)
#         if cantidad_num <= 0:
#             return False, "La cantidad pedida debe ser mayor a cero."
        
#         # AQUÍ USAMOS el método del modelo registrar_pedido
#         plato.registrar_pedido(turno, cantidad_num)

#         registros = gestor.leer()
#         for i, reg in enumerate(registros):
#             if reg["id"] == id_plato:
#                 # AQUÍ USAMOS el método a_diccionario
#                 registros[i] = plato.a_diccionario()
#                 break

#         gestor.guardar(registros)
#         return True, f"Se agregaron {cantidad_num} unidad(es) de {plato.nombre} al turno {turno.title()}."
        
#     except ValueError:
#         return False, "La cantidad debe ser un número entero."
#     except Exception as error:
#         return False, f"Error al procesar la comanda: {error}"

# def agregar_alergeno_plato(id_plato: int, alergeno: str) -> Tuple[bool, str]:
#     # Registra una advertencia de salud en la receta del platillo
#     plato = obtener_por_id(id_plato)
#     if not plato:
#         return False, "Platillo no encontrado."
        
#     # AQUÍ USAMOS el método del modelo agregar_alergeno
#     plato.agregar_alergeno(alergeno)
    
#     registros = gestor.leer()
#     for i, reg in enumerate(registros):
#         if reg["id"] == id_plato:
#             registros[i] = plato.a_diccionario()
#             break
            
#     gestor.guardar(registros)
#     return True, f"Alerta de '{alergeno.title()}' agregada al platillo."

# def todos_los_alergenos() -> Set[str]:
#     # Devuelve un set global con todas las advertencias alimentarias presentes en el menú entero
#     alergenos_totales = set()
#     for plato in obtener_todos():
#         alergenos_totales.update(plato.alergenos)
#     return alergenos_totales

# def alergenos_en_comun_platos(id_a: int, id_b: int) -> Set[str]:
#     # Compara dos platillos y devuelve los alérgenos o ingredientes riesgosos que ambos comparten
#     plato_a = obtener_por_id(id_a)
#     plato_b = obtener_por_id(id_b)
    
#     if not plato_a or not plato_b:
#         return set()
        
#     # AQUÍ USAMOS el método del modelo alergenos_en_comun
#     return plato_a.alergenos_en_comun(plato_b)

# def plato_estrella() -> Optional[Dict[str, Any]]:
#     # Busca el platillo más pedido por los comensales
#     # SE USA internamente en la función de estadísticas
#     platos = obtener_todos()
#     if not platos:
#         return None
    
#     # AQUÍ USAMOS total_unidades_vendidas del modelo para encontrar el más popular
#     mas_vendido = max(platos, key=lambda p: p.total_unidades_vendidas())
    
#     # AQUÍ USAMOS obtener_resumen del modelo
#     return {
#         "info": mas_vendido.obtener_resumen(),
#         "unidades": mas_vendido.total_unidades_vendidas()
#     }

# def estadisticas() -> Dict[str, Any]:
#     # Genera el reporte gerencial y de cocina del restaurante
#     platos = obtener_todos()
    
#     categorias = {p.categoria for p in platos}
#     platos_disponibles = sum(1 for p in platos if p.disponible)
    
#     # AQUÍ USAMOS calcular_ingresos_historicos del modelo para facturación global
#     ingresos_brutos = sum(p.calcular_ingresos_historicos() for p in platos)
    
#     # AQUÍ USAMOS la función que identifica el plato más vendido
#     estrella = plato_estrella()

#     return {
#         "total_platos_menu": len(platos),
#         "platos_disponibles": platos_disponibles,
#         "categorias_menu": sorted(categorias),
#         "ingresos_historicos": round(ingresos_brutos, 2),
#         "plato_mas_vendido": estrella
#     }

# from typing import List, Dict, Callable, Any, Tuple
# from models import Plato, CAMPOS_PLATO
# from shared.herramientas import (
#     imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
# )
# from views import (
#     crear_plato, obtener_todos, obtener_por_id, buscar_platos,
#     actualizar_plato, eliminar_plato, registrar_comanda_plato,
#     agregar_alergeno_plato, todos_los_alergenos, alergenos_en_comun_platos, 
#     estadisticas
# )

# def pausa() -> None:
#     # Detiene la ejecución hasta que el usuario presione Enter
#     input("\nPresione Enter para continuar...")

# def mostrar_tabla(platos: List[Plato]) -> None:
#     # Imprime una tabla formateada en consola con el menú
#     print(f"{'ID':<5}{'CÓDIGO':<10}{'PLATILLO':<25}{'CATEGORÍA':<15}{'PRECIO':<10}{'ESTADO':<15}")
#     print("-" * 80)
#     for plato in platos:
#         estado = "Disponible" if plato.disponible else "Agotado"
#         print(f"{plato.id:<5}{plato.codigo:<10}{plato.nombre[:23]:<25}{plato.categoria[:13]:<15}${plato.precio:<9.2f}{estado:<15}")
#     print("-" * 80)
#     imprimir_info(f"Total: {len(platos)} platillo(s)")

# def opcion_crear() -> None:
#     # Solicita los datos por teclado y llama al controlador para registrar un plato
#     imprimir_titulo("AGREGAR NUEVO PLATILLO AL MENÚ")
    
#     datos: Dict[str, str] = {}
#     for campo in CAMPOS_PLATO:
#         if campo == "disponible":
#             datos[campo] = input("¿Estará disponible para la venta hoy? (Deje en blanco para NO, escriba algo para SÍ): ")
#         else:
#             datos[campo] = input(f"{campo.capitalize().replace('_', ' ')}: ")

#     exito, mensaje = crear_plato(datos)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_todos() -> None:
#     # Obtiene y muestra la carta completa del restaurante
#     imprimir_titulo("CARTA / MENÚ COMPLETO")
#     platos = obtener_todos()
    
#     if not platos:
#         imprimir_info("El menú está vacío. Use la opción 1 para empezar.")
#     else:
#         mostrar_tabla(platos)
#     pausa()

# def opcion_buscar() -> None:
#     # Buscador global por código, nombre o categoría
#     imprimir_titulo("BUSCAR PLATILLO")
#     termino = input("Ingrese código, nombre o categoría (ej. Postre, Fuerte): ")
#     encontrados = buscar_platos(termino)

#     if not encontrados:
#         imprimir_info(f"Ningún platillo coincide con '{termino}'.")
#     else:
#         mostrar_tabla(encontrados)
#     pausa()

# def opcion_ver_por_id() -> None:
#     # Muestra el detalle completo de un platillo y su rentabilidad
#     imprimir_titulo("FICHA DEL PLATILLO")
#     try:
#         id_plato = int(input("Ingrese el ID del platillo: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     plato = obtener_por_id(id_plato)
#     if not plato:
#         imprimir_error(f"No existe un platillo con ID {id_plato}")
#     else:
#         print("\nRECETA Y DATOS DE VENTA")
#         for clave, valor in plato.a_diccionario().items():
#             print(f"  {clave.upper():<20}: {valor}")
            
#         print("\nRENDIMIENTO COMERCIAL")
#         print(f"  UNIDADES VENDIDAS  : {plato.total_unidades_vendidas()}")
#         print(f"  INGRESOS GENERADOS : ${plato.calcular_ingresos_historicos()}")
#     pausa()

# def opcion_actualizar() -> None:
#     # Permite editar campos específicos validando con el controlador
#     imprimir_titulo("ACTUALIZAR DATOS DEL PLATILLO")
#     try:
#         id_plato = int(input("Ingrese el ID del platillo a editar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     plato = obtener_por_id(id_plato)
#     if not plato:
#         imprimir_error(f"No existe un platillo con ID {id_plato}")
#         return pausa()

#     imprimir_info(f"Editando: {plato.obtener_resumen()}")
#     print("Nota: Deje presionado Enter (en blanco) en los campos que NO desee cambiar.\n")

#     cambios: Dict[str, Any] = {}
#     for campo in CAMPOS_PLATO:
#         actual = getattr(plato, campo)
#         nuevo = input(f"{campo.capitalize().replace('_', ' ')} [{actual}]: ").strip()
        
#         if nuevo:
#             if campo == "disponible":
#                 cambios[campo] = nuevo.lower() not in ("false", "0", "no", "f")
#             else:
#                 cambios[campo] = nuevo

#     exito, mensaje = actualizar_plato(id_plato, cambios)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_eliminar() -> None:
#     # Pide confirmación y retira un platillo del menú permanentemente
#     imprimir_titulo("RETIRAR PLATILLO DEL MENÚ")
#     try:
#         id_plato = int(input("Ingrese el ID del platillo a retirar: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     plato = obtener_por_id(id_plato)
#     if not plato:
#         imprimir_error(f"No existe un platillo con ID {id_plato}")
#         return pausa()

#     imprimir_info(f"Se eliminará permanentemente:\n{plato}")
    
#     if confirmar("¿Confirma que desea retirar este platillo del sistema? (si/no): "):
#         exito, mensaje = eliminar_plato(id_plato)
#         if exito:
#             imprimir_exito(mensaje)
#         else:
#             imprimir_error(mensaje)
#     else:
#         imprimir_info("Operación cancelada.")
#     pausa()

# def opcion_registrar_comanda() -> None:
#     # Registra pedidos en un turno específico
#     imprimir_titulo("REGISTRAR COMANDA / PEDIDO")
#     try:
#         id_plato = int(input("Ingrese el ID del platillo pedido: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     turno = input("Turno o mesa (ej. Almuerzo, Cena, Mesa 4): ").strip()
#     cantidad = input("Cantidad de platos pedidos: ").strip()
    
#     exito, mensaje = registrar_comanda_plato(id_plato, turno, cantidad)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_agregar_alergeno() -> None:
#     # Añade un riesgo dietético al plato
#     imprimir_titulo("AGREGAR ALERTA DE ALÉRGENO")
#     try:
#         id_plato = int(input("Ingrese el ID del platillo: "))
#     except ValueError:
#         imprimir_error("El ID debe ser un número entero.")
#         return pausa()

#     alergeno = input("Ingrediente alérgeno (ej. Mariscos, Maní, Gluten): ").strip()
    
#     exito, mensaje = agregar_alergeno_plato(id_plato, alergeno)
#     if exito:
#         imprimir_exito(mensaje)
#     else:
#         imprimir_error(mensaje)
#     pausa()

# def opcion_ver_alergenos_globales() -> None:
#     # Muestra un listado unificado de todos los alérgenos presentes en el restaurante
#     imprimir_titulo("INVENTARIO DE ALÉRGENOS DEL RESTAURANTE")
#     alergenos = todos_los_alergenos()
#     if not alergenos:
#         imprimir_info("Aún no hay alérgenos registrados en el menú.")
#     else:
#         for i, alergeno in enumerate(sorted(alergenos), 1):
#             print(f"  {i}. {alergeno}")
#     pausa()

# def opcion_alergenos_en_comun() -> None:
#     # Compara alérgenos compartidos entre dos recetas
#     imprimir_titulo("COMPARAR RECETAS (ALÉRGENOS EN COMÚN)")
#     try:
#         id_a = int(input("Ingrese el ID del primer platillo: "))
#         id_b = int(input("Ingrese el ID del segundo platillo: "))
#     except ValueError:
#         imprimir_error("Los IDs deben ser números enteros.")
#         return pausa()

#     comun = alergenos_en_comun_platos(id_a, id_b)
#     if comun:
#         imprimir_exito(f"Ingredientes de riesgo que comparten: {', '.join(sorted(comun))}")
#     else:
#         imprimir_info("No comparten ningún alérgeno o algún ID no existe.")
#     pausa()

# def opcion_estadisticas() -> None:
#     # Muestra el panel gerencial de cocina y ventas
#     imprimir_titulo("PANEL GERENCIAL DEL RESTAURANTE")
#     datos = estadisticas()
    
#     print(f"  Total de platillos en el menú   : {datos['total_platos_menu']}")
#     print(f"  Platillos disponibles hoy       : {datos['platos_disponibles']}")
#     print(f"  Categorías ({len(datos['categorias_menu'])})                  : {', '.join(datos['categorias_menu'])}")
#     print(f"  Ingresos brutos acumulados      : ${datos['ingresos_historicos']}")
    
#     estrella = datos.get("plato_mas_vendido")
#     if estrella:
#         print("\n  🏆 PLATILLO ESTRELLA DEL RESTAURANTE:")
#         print(f"  -> {estrella['info']} con {estrella['unidades']} porciones vendidas.")
        
#     pausa()

# def salir() -> str:
#     # Cierra el bucle principal de la aplicación
#     imprimir_info("¡Gracias por usar el Sistema del Restaurante! 🍽️")
#     return "salir"

# # DICCIONARIO DE FUNCIONES
# # El núcleo del menú: invoca cada función específica garantizando cero código muerto
# OPCIONES: Dict[str, Tuple[str, Callable[[], Any]]] = {
#     "1": ("Agregar nuevo platillo al menú", opcion_crear),
#     "2": ("Ver toda la carta", opcion_ver_todos),
#     "3": ("Buscar platillo", opcion_buscar),
#     "4": ("Ver receta y rentabilidad del plato", opcion_ver_por_id),
#     "5": ("Actualizar datos de un platillo", opcion_actualizar),
#     "6": ("Retirar platillo del menú", opcion_eliminar),
#     "7": ("Registrar pedido / comanda", opcion_registrar_comanda),
#     "8": ("Agregar alerta de alérgeno", opcion_agregar_alergeno),
#     "9": ("Ver inventario de alérgenos global", opcion_ver_alergenos_globales),
#     "10": ("Comparar alérgenos entre 2 platos", opcion_alergenos_en_comun),
#     "11": ("Ver estadísticas de ventas y menú", opcion_estadisticas),
#     "0": ("Salir del sistema", salir),
# }

# def mostrar_menu() -> None:
#     # Pinta las opciones del menú dinámicamente
#     imprimir_titulo("SISTEMA DE GESTIÓN GASTRONÓMICA")
#     for tecla, (texto, _funcion) in OPCIONES.items():
#         print(f"  {tecla}. {texto}")
#     print()

# def main() -> None:
#     # Bucle infinito que mantiene la app corriendo hasta elegir Salir
#     while True:
#         mostrar_menu()
#         tecla = input("Seleccione una opción: ").strip()

#         if tecla not in OPCIONES:
#             imprimir_error("Opción no válida. Por favor, intente de nuevo.")
#             pausa()
#             continue

#         _texto, funcion = OPCIONES[tecla]
        
#         if funcion() == "salir":
#             break

# # Punto de ejecución
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nPrograma interrumpido por el usuario de forma abrupta.")