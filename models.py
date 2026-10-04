from typing import Dict, List, Set, Any, Optional

# TUPLA de configuración con todos los atributos de la entidad.
# Al ser inmutable, sirve como la "fuente de la verdad" para el controlador.
CAMPOS_ESTUDIANTE: tuple[str, ...] = (
    "nombre",
    "apellido",
    "email",
    "cedula",
    "carnet",
    "facultad",
    "carrera",
    "nivel",
    "paralelo",
    "beca_activa",
)


class Estudiante:
    """
    MODELO: Representa a un estudiante dentro del sistema académico.
    Encapsula los datos personales, académicos y la lógica matemática/operativa (notas y materias).
    Utiliza las cuatro colecciones nativas de Python: Listas, Tuplas, Conjuntos y Diccionarios.
    """

    def __init__(
        self,
        id_estudiante: int,
        nombre: str,
        apellido: str,
        email: str,
        cedula: str,
        carnet: str,
        facultad: str,
        carrera: str,
        nivel: int,
        paralelo: str,
        beca_activa: bool = False,
        notas: Optional[Dict[str, List[float]]] = None,
        materias: Optional[Set[str]] = None,
    ) -> None:
        """Constructor de la clase. Inicializa el estado del estudiante en memoria."""
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.cedula = cedula
        self.carnet = carnet                      # ej: EST2026001
        self.facultad = facultad
        self.carrera = carrera
        self.nivel = nivel
        self.paralelo = paralelo
        self.beca_activa = beca_activa
        
        # DICCIONARIO DE LISTAS: {"Matemática": [18.5, 19.0], "Inglés": [17.0]}
        # Evitamos el defecto de los argumentos mutables inicializando un dict nuevo si llega None
        self.notas = notas if notas else {}
        
        # CONJUNTO (set): materias en las que está inscrito, sin repetidos.
        # Si envían datos, los convertimos a set; si llega None, creamos un set vacío.
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self) -> str:
        """Devuelve el nombre y apellido concatenados."""
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia: str) -> None:
        """
        Agrega una nueva materia al registro del estudiante.
        Al ser un conjunto (set), si la materia ya existe, la función .add() 
        simplemente la ignora evitando duplicados automáticamente.
        """
        self.materias.add(materia)

    def agregar_nota(self, materia: str, nota: float) -> None:
        """
        Registra una calificación en una materia específica.
        Si la materia no estaba inscrita, la inscribe y luego guarda la nota.
        """
        # Primero aseguramos que la materia esté en el conjunto de materias
        self.inscribir_materia(materia)
        
        # setdefault() busca la materia en el diccionario:
        # - Si ya existe, devuelve la lista de notas actual.
        # - Si NO existe, crea la clave con una lista vacía [] y la devuelve.
        # Luego hacemos .append(nota) a la lista resultante.
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self) -> float:
        """
        Calcula el promedio general aritmético de TODAS las notas de todas las materias.
        
        Returns:
            float: El promedio general redondeado a 2 decimales, o 0.0 si no hay notas.
        """
        todas = []
        # .values() ignora los nombres de las materias y extrae solo las listas de calificaciones
        for lista_notas in self.notas.values():
            # .extend() saca las notas de la sub-lista y las aplana en la lista 'todas'
            todas.extend(lista_notas)
            
        # Prevención contra error matemático (división por cero)
        if not todas:
            return 0.0
            
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante: "Estudiante") -> Set[str]:
        """
        Compara las materias de este estudiante con las de otro usando álgebra de conjuntos.
        
        Args:
            otro_estudiante (Estudiante): Otra instancia de la misma clase.
            
        Returns:
            Set[str]: Un conjunto con los nombres de las asignaturas que ambos cursan.
        """
        # El operador '&' realiza la INTERSECCIÓN matemática entre dos conjuntos (sets).
        return self.materias & otro_estudiante.materias

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Serializa el objeto (lo convierte a diccionario de Python) para poder guardarlo en JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "cedula": self.cedula,
            "carnet": self.carnet,
            "facultad": self.facultad,
            "carrera": self.carrera,
            "nivel": self.nivel,
            "paralelo": self.paralelo,
            "beca_activa": self.beca_activa,
            "notas": self.notas,
            # CRÍTICO: JSON no soporta el tipo 'set'. 
            # Usamos sorted() para convertirlo en una lista normal ('list') y ordenarla alfabéticamente.
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Estudiante":
        """
        Factory Method: Reconstruye un objeto Estudiante a partir de un diccionario leído del JSON.
        
        Args:
            datos (dict): Diccionario crudo proveniente del archivo JSON.
            
        Returns:
            Estudiante: Una nueva instancia viva y funcional.
        """
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["cedula"],
            datos["carnet"],
            datos["facultad"],
            datos["carrera"],
            datos["nivel"],
            datos["paralelo"],
            # Usamos .get() en campos que podrían faltar en registros muy viejos para evitar caídas
            beca_activa=datos.get("beca_activa", False),
            notas=datos.get("notas", {}),
            # Al leer del JSON (donde era lista), lo envolvemos en set() para restaurar el conjunto
            materias=set(datos.get("materias", [])),
        )

    def __str__(self) -> str:
        """
        Método mágico Dunder: Define cómo se muestra el objeto al usar print(estudiante).
        """
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"