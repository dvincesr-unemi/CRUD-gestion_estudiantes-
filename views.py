from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración: fijas e inmutables durante el ciclo de vida de la app
CAMPOS_OBLIGATORIOS = (
    "nombre", 
    "apellido", 
    "email", 
    "cedula", 
    "facultad", 
    "carrera", 
    "nivel", 
    "paralelo"
)

CAMPOS_BUSCABLES = (
    "nombre", 
    "apellido", 
    "email", 
    "cedula", 
    "carrera", 
    "paralelo"
)


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """CONJUNTO (set) con los emails ya usados. Detecta duplicados en O(1)."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def cedulas_registradas(excepto_id=None):
    """CONJUNTO (set) con las cédulas ya usadas para evitar duplicidad de identidad."""
    return {
        str(registro["cedula"]).strip()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    """Calcula el siguiente id secuencial de forma segura."""
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """
    datos: diccionario con las claves de CAMPOS_ESTUDIANTE.
    Devuelve (exito: bool, mensaje: str).
    """
    try:
        # 1) Normalización de campos tipo texto y extracción de los demás
        valores = {}
        for campo in CAMPOS_ESTUDIANTE:
            if campo in ("nivel", "beca_activa"):
                valores[campo] = datos.get(campo)
            else:
                valores[campo] = str(datos.get(campo, "")).strip()

        # 2) Validación de campos obligatorios recorriendo la TUPLA
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if valores[campo] is None or valores[campo] == ""]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Validación de tipos numéricos y booleanos específicos
        try:
            valores["nivel"] = int(valores["nivel"])
        except (ValueError, TypeError):
            return False, "El nivel (semestre) debe ser un número entero válido"

        valores["beca_activa"] = bool(valores.get("beca_activa", False))

        # 4) Validación de formato de email
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 5) Validación de duplicados instantánea mediante CONJUNTOS (sets)
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado por otro estudiante"

        if valores["cedula"] in cedulas_registradas():
            return False, f"La cédula '{valores['cedula']}' ya se encuentra registrada"

        # 6) Instanciación del Modelo (desempaquetado ** de argumentos)
        estudiante = Estudiante(siguiente_id(), **valores)

        # 7) Persistencia: añadir a la LISTA y guardar en disco
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir en el archivo estudiantes.json"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} registrado con ID {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """LISTA de objetos Estudiante reconstruidos con su Factory Method."""
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_estudiante):
    """Busca y retorna la instancia de Estudiante según su identificador único."""
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def obtener_por_cedula(cedula):
    """Búsqueda directa por número de cédula."""
    cedula_limpia = str(cedula).strip()
    for estudiante in obtener_todos():
        if estudiante.cedula == cedula_limpia:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    """Búsqueda lineal en los campos definidos en CAMPOS_BUSCABLES."""
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break  # Coincidencia hallada: pasa al siguiente estudiante
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """cambios: diccionario únicamente con los campos que se desean modificar."""
    try:
        # DIFERENCIA DE CONJUNTOS: valida si enviaron claves inexistentes
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio para actualizar"

        # Validaciones de reglas de negocio sobre los cambios
        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya pertenece a otro estudiante"

        if "cedula" in cambios:
            cedula_str = str(cambios["cedula"]).strip()
            if cedula_str in cedulas_registradas(excepto_id=id_estudiante):
                return False, "Esa cédula ya pertenece a otro estudiante"
            cambios["cedula"] = cedula_str

        if "nivel" in cambios:
            try:
                cambios["nivel"] = int(cambios["nivel"])
            except (ValueError, TypeError):
                return False, "El nivel debe ser un número entero válido"

        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con ID {id_estudiante}"

        # Actualiza el diccionario en memoria y persiste en JSON
        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Estudiante con ID {id_estudiante} actualizado ({len(cambios)} campo/s modificados)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    """Eliminación no destructiva mediante comprensión de listas."""
    registros = gestor.leer()
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con ID {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante con ID {id_estudiante} eliminado correctamente"


# ===================== GESTIÓN ACADÉMICA (NOTAS Y MATERIAS) =====================

def agregar_calificacion(id_estudiante, materia, nota):
    """Añade una nota a una materia específica de un estudiante y actualiza el archivo."""
    try:
        estudiante = obtener_por_id(id_estudiante)
        if not estudiante:
            return False, f"No existe un estudiante con ID {id_estudiante}"

        nota_num = float(nota)
        estudiante.agregar_nota(materia, nota_num)

        # Actualizamos en disco reconstruyendo la lista
        registros = gestor.leer()
        for i, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                registros[i] = estudiante.a_diccionario()
                break

        gestor.guardar(registros)
        return True, f"Nota {nota_num} añadida a '{materia}' para {estudiante.obtener_nombre_completo()}"
    except ValueError:
        return False, "La calificación ingresada debe ser un número decimal o entero válido"
    except Exception as error:
        return False, f"Error al registrar la calificación: {error}"


# ===================== EXTRA: estadísticas con conjuntos =====================

def estadisticas():
    """Devuelve un DICCIONARIO resumen aplicando teoría de colecciones."""
    registros = gestor.leer()
    carreras = {r.get("carrera", "").title() for r in registros if r.get("carrera")}
    facultades = {r.get("facultad", "").title() for r in registros if r.get("facultad")}
    con_beca = [r["nombre"] for r in registros if r.get("beca_activa")]

    return {
        "total": len(registros),
        "carreras": sorted(carreras),
        "facultades": sorted(facultades),
        "total_becados": len(con_beca),
        "becados": con_beca,
    }