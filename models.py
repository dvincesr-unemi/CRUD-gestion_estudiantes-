import json

# TUPLA fija de campos para el Estudiante: inmutable y con orden garantizado.
# Actualizada con los nuevos datos académicos para la Vista y el Controlador.
CAMPOS_ESTUDIANTE = (
    "nombre", 
    "apellido", 
    "email", 
    "cedula", 
    "facultad", 
    "carrera", 
    "nivel", 
    "paralelo", 
    "beca_activa"
)


class Estudiante:
    """
    MODELO: Representa la entidad de un estudiante universitario en el sistema.
    Aplica las cuatro estructuras de datos de Python:
      - Tupla: CAMPOS_ESTUDIANTE (orden fijo)
      - Diccionario: self.notas (asociación materia -> lista de notas)
      - Lista: valores de notas y serialización para JSON
      - Conjunto (set): self.materias (elementos únicos sin duplicados)
    """

    def __init__(
        self,
        id_estudiante: int,
        nombre: str,
        apellido: str,
        email: str,
        cedula: str,
        facultad: str,
        carrera: str,
        nivel: int,
        paralelo: str,
        beca_activa: bool,
        notas: dict = None,
        materias: set = None,
    ) -> None:
        """
        Constructor del estudiante.

        Args:
            id_estudiante (int): Identificador numérico único del registro.
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            email (str): Correo electrónico institucional.
            cedula (str): Cédula de identidad de 10 dígitos.
            facultad (str): Facultad a la que pertenece (ej. 'Facultad de Ciencias de la Ingeniería').
            carrera (str): Programa de grado (ej. 'Ingeniería en Software').
            nivel (int): Semestre actual (ej. 1 para primer semestre).
            paralelo (str): Grupo o aula asignada (ej. 'A1', 'B2').
            beca_activa (bool): True si goza de algún beneficio económico/académico, False si no.
            notas (dict, opcional): Diccionario con formato {materia: [notas]}.
            materias (set, opcional): Conjunto de materias inscritas.
        """
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.cedula = cedula
        self.facultad = facultad
        self.carrera = carrera
        self.nivel = nivel
        self.paralelo = paralelo
        self.beca_activa = beca_activa

        # Evitamos el error común de usar {} o set() mutables como valores por defecto
        self.notas = notas if notas else {}
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self) -> str:
        """Concatena y devuelve el nombre y apellido del estudiante."""
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia: str) -> None:
        """Inscribe al estudiante usando un conjunto (evita duplicados)."""
        self.materias.add(materia)

    def agregar_nota(self, materia: str, nota: float) -> None:
        """Registra una calificación e inscribe automáticamente si no lo estaba."""
        self.inscribir_materia(materia)
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self) -> float:
        """Calcula el promedio general de todas las notas."""
        todas = []
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)

        if not todas:
            return 0.0
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante: "Estudiante") -> set:
        """Intersección de conjuntos: materias compartidas con otro estudiante."""
        return self.materias & otro_estudiante.materias

    def a_diccionario(self) -> dict:
        """Serializa la instancia a un diccionario nativo para guardar en JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "cedula": self.cedula,
            "facultad": self.facultad,
            "carrera": self.carrera,
            "nivel": self.nivel,
            "paralelo": self.paralelo,
            "beca_activa": self.beca_activa,
            "notas": self.notas,
            "materias": sorted(self.materias), # Convertimos el set a list
        }

    @classmethod
    def desde_diccionario(cls, datos: dict) -> "Estudiante":
        """Reconstruye un objeto Estudiante desde un diccionario (ej. al leer JSON)."""
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["cedula"],
            datos["facultad"],
            datos["carrera"],
            datos["nivel"],
            datos["paralelo"],
            # .get para booleanos evita errores si el JSON anterior no tenía este campo
            datos.get("beca_activa", False), 
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    def a_json(self) -> str:
        """Convierte la instancia en un string JSON directo."""
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    def __str__(self) -> str:
        """Representación para la consola."""
        # Ahora mostramos la cédula, la carrera y el nivel
        estado_beca = "⭐ Beca" if self.beca_activa else "Sin beca"
        return f"[{self.cedula}] {self.obtener_nombre_completo()} - {self.carrera} (Nivel {self.nivel}) | Promedio: {self.obtener_promedio()} | {estado_beca}"