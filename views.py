from typing import List, Tuple, Dict, Any, Optional, Set
from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

# Instancia global del gestor para leer y guardar en el archivo JSON
gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS: Tuple[str, ...] = (
    "nombre", "apellido", "email", "cedula", "carnet", 
    "facultad", "carrera", "nivel", "paralelo"
)

CAMPOS_BUSCABLES: Tuple[str, ...] = (
    "nombre", "apellido", "email", "cedula", "carnet", "carrera"
)


def emails_registrados(excepto_id: Optional[int] = None) -> Set[str]:
    """
    Crea un conjunto (set) con todos los emails almacenados en la base de datos.
    
    Args:
        excepto_id (int, opcional): ID del estudiante que se debe ignorar en la búsqueda 
                                    (muy útil al momento de actualizar a un estudiante).
    
    Returns:
        Set[str]: Un conjunto de correos electrónicos en minúsculas.
    """
    # Usamos una "comprensión de conjuntos" (set comprehension)
    # Esto extrae los emails, los pasa a minúsculas y elimina automáticamente duplicados
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def cedulas_registradas(excepto_id: Optional[int] = None) -> Set[str]:
    """
    Crea un conjunto (set) con todas las cédulas almacenadas para evitar doble matriculación.
    
    Args:
        excepto_id (int, opcional): ID del estudiante que se debe ignorar.
        
    Returns:
        Set[str]: Un conjunto de números de cédula como cadenas de texto.
    """
    return {
        str(registro["cedula"]).strip()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id() -> int:
    """
    Calcula el próximo ID secuencial disponible leyendo los registros actuales.
    
    Returns:
        int: El número de ID que le corresponderá al nuevo estudiante.
    """
    # Comprensión de listas: extraemos solo los IDs de todos los diccionarios
    ids = [registro["id"] for registro in gestor.leer()]
    # Si la lista tiene elementos, tomamos el máximo y le sumamos 1. Si está vacía, iniciamos en 1.
    return max(ids) + 1 if ids else 1

#Crear

def crear_estudiante(datos: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Procesa un diccionario de datos crudos, lo valida, instancia el modelo y lo guarda en JSON.
    
    Args:
        datos (dict): Diccionario con los datos ingresados por el usuario.
        
    Returns:
        Tuple[bool, str]: Una tupla donde el primer valor es un booleano (True si fue exitoso) 
                          y el segundo valor es un mensaje descriptivo.
    """
    try:
        # 1) NORMALIZACIÓN: Limpiamos los datos y forzamos los tipos correctos
        valores = {}
        for campo in CAMPOS_ESTUDIANTE:
            if campo == "beca_activa":
                # Forzamos a booleano
                valores[campo] = bool(datos.get(campo, False))
            elif campo == "nivel":
                # Si no envían el nivel, dejamos un string vacío para que la validación lo detecte
                valores[campo] = datos.get(campo, "") 
            else:
                # Limpiamos espacios en blanco a los extremos de los textos
                valores[campo] = str(datos.get(campo, "")).strip()

        # 2) VALIDACIÓN DE OBLIGATORIOS: Comparamos contra nuestra tupla fija
        # Si el campo está vacío, lo agregamos a la lista de faltantes
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if valores[campo] == ""]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 2.5) VALIDACIÓN DE TIPO: El nivel debe ser numérico
        try:
            valores["nivel"] = int(valores["nivel"])
        except ValueError:
            return False, "El nivel debe ser un número entero (ej: 3 para tercer semestre)"

        # 3) VALIDACIÓN DE FORMATO: Revisamos el correo
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 4) REGLAS DE NEGOCIO (DUPLICADOS): Búsqueda instantánea O(1) usando los conjuntos
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        if valores["cedula"] in cedulas_registradas():
            return False, "Esa cédula ya está registrada"

        # 5) INSTANCIACIÓN: Desempaquetamos (**) el diccionario para construir el objeto Estudiante
        estudiante = Estudiante(siguiente_id(), **valores)

        # 6) PERSISTENCIA: Agregamos el diccionario del objeto a la lista del archivo y guardamos
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} matriculado con id {estudiante.id}"

    except Exception as error:
        # Capturamos cualquier error inesperado para que el programa no colapse (Crash)
        return False, f"Error inesperado: {error}"


#Leer

def obtener_todos() -> List[Estudiante]:
    """
    Lee el archivo JSON y reconstruye todos los objetos Estudiante en memoria.
    
    Returns:
        List[Estudiante]: Una lista llena de instancias vivas de la clase Estudiante.
    """
    # Usamos el Factory Method (@classmethod) 'desde_diccionario' del modelo
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_estudiante: int) -> Optional[Estudiante]:
    """
    Busca a un estudiante específico según su identificador único.
    
    Args:
        id_estudiante (int): El ID del estudiante a buscar.
        
    Returns:
        Optional[Estudiante]: El objeto Estudiante si lo encuentra, o None si no existe.
    """
    # Recorremos los objetos ya instanciados
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


#Buscar
def buscar_estudiantes(termino: str) -> List[Estudiante]:
    """
    Realiza una búsqueda tipo "fuzzy" o lineal por múltiples campos configurados.
    
    Args:
        termino (str): La palabra o texto a buscar (ej: "Juan", "Ingeniería").
        
    Returns:
        List[Estudiante]: Una lista con los objetos Estudiante que coincidieron.
    """
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    # Recorremos los diccionarios crudos en el JSON por rendimiento
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            # Si el término de búsqueda es parte del contenido del campo (ej: "juan" in "juan perez")
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break  # Evitamos que el estudiante se agregue doble si coincide en 2 campos
    return encontrados


#Actualizar

def actualizar_estudiante(id_estudiante: int, cambios: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Modifica únicamente los campos enviados en el diccionario 'cambios' para un estudiante.
    
    Args:
        id_estudiante (int): ID del estudiante a editar.
        cambios (dict): Diccionario con las claves y los nuevos valores (ej: {"nivel": 4}).
        
    Returns:
        Tuple[bool, str]: Resultado de la operación (éxito, mensaje).
    """
    try:
        # 1) DIFERENCIA DE CONJUNTOS: Validamos que no envíen claves inventadas
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        # 2) Validaciones específicas solo si el campo viene en 'cambios'
        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            # Nótese que aquí pasamos el 'excepto_id' para que no diga que "su propio correo" ya está en uso
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"
                
        if "cedula" in cambios:
            if str(cambios["cedula"]).strip() in cedulas_registradas(excepto_id=id_estudiante):
                return False, "Esa cédula ya está registrada por otro estudiante"

        if "nivel" in cambios:
            try:
                cambios["nivel"] = int(cambios["nivel"])
            except ValueError:
                return False, "El nivel debe ser un número entero"

        # 3) Localizar la posición del registro en la lista global
        registros = gestor.leer()
        posicion = None
        # enumerate() nos devuelve el índice (0, 1, 2...) y el diccionario de cada iteración
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        # 4) Actualizamos usando el método nativo de los diccionarios (.update())
        registros[posicion].update(cambios)
        
        # 5) Guardamos la lista completa de nuevo en el archivo
        gestor.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


#Delete

def eliminar_estudiante(id_estudiante: int) -> Tuple[bool, str]:
    """
    Elimina un estudiante de la base de datos reconstruyendo la lista sin él.
    
    Args:
        id_estudiante (int): ID del estudiante a borrar.
        
    Returns:
        Tuple[bool, str]: Resultado de la operación (éxito, mensaje).
    """
    registros = gestor.leer()
    
    # Práctica segura: en vez de borrar con .remove() mientras iteramos (lo cual causa bugs),
    # construimos una lista nueva que incluya a todos EXCEPTO al que queremos borrar.
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]

    # Si la lista nueva tiene el mismo tamaño, significa que no se filtró a nadie (el ID no existía)
    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    # Guardamos la lista filtrada
    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"

#Gestion academica

def agregar_calificacion(id_estudiante: int, materia: str, nota: str):
    """Añade una nota a una materia específica de un estudiante y actualiza el archivo JSON."""
    try:
        estudiante = obtener_por_id(id_estudiante)
        if not estudiante:
            return False, f"No existe un estudiante con ID {id_estudiante}"

        # Convertimos la nota (que entra como texto desde el input) a número flotante
        nota_num = float(nota)
        
        # VALIDACIÓN DEL RANGO (0 a 20)
        if not (0 <= nota_num <= 20):
            return False, "La calificación debe estar entre 0 y 20."
        
        # Llamamos al modelo para que actualice la memoria RAM
        estudiante.agregar_nota(materia, nota_num)

        # Reconstruimos la lista para guardarla en disco
        registros = gestor.leer()
        for i, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                registros[i] = estudiante.a_diccionario()
                break

        # Persistimos el cambio
        gestor.guardar(registros)
        return True, f"Nota {nota_num} añadida a '{materia}' para {estudiante.obtener_nombre_completo()}"
        
    except ValueError:
        return False, "La calificación ingresada debe ser un número decimal (ej. 18.5) o entero válido"
    except Exception as error:
        return False, f"Error al registrar la calificación: {error}"

def materias_ofertadas() -> Set[str]:
    """Devuelve un set con todas las materias inscritas por todos los estudiantes, sin repetir."""
    estudiantes = obtener_todos()
    materias_totales = set()
    
    for estudiante in estudiantes:
        # El controlador se adapta al modelo usando directamente el set de materias
        materias_totales.update(estudiante.materias)
        
    return materias_totales

def estudiantes_en_comun(id_a: int, id_b: int) -> Set[str]:
    """Controlador que busca a dos estudiantes y devuelve sus materias en común."""
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)
    
    if not estudiante_a or not estudiante_b:
        return set() # O manejar el error según prefieras
        
    # Llamamos al método experto que ya creaste en el Modelo
    return estudiante_a.materias_en_comun(estudiante_b)


# ESTADÍSTICAS 

def estadisticas() -> Dict[str, Any]:
    """
    Genera métricas globales del sistema aplicando lógica de conjuntos y listas.
    
    Returns:
        Dict[str, Any]: Diccionario con resúmenes estadísticos listos para mostrarse.
    """
    registros = gestor.leer()
    
    # CONJUNTOS (sets): extraemos facultades y carreras únicas (sin repetidos)
    facultades = {r.get("facultad", "").title() for r in registros if r.get("facultad")}
    carreras = {r.get("carrera", "").title() for r in registros if r.get("carrera")}
    
    # LISTAS (lists): extraemos únicamente los nombres de quienes tienen beca
    becados = [r["nombre"] for r in registros if r.get("beca_activa")]

    return {
        "total": len(registros),
        # sorted() convierte los conjuntos en listas ordenadas alfabéticamente
        "facultades": sorted(facultades),
        "carreras": sorted(carreras),
        "total_becados": len(becados),
        "becados": becados,
    }