# Ejercicio 1. Quitar duplicados conservando el orden

# Enunciado:
# Dada la lista:
# ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
# Obtenga una nueva lista sin elementos repetidos,
# respetando el orden en que aparecen por primera vez.

# Bosquejo:
# 1. Crear una lista vacia para el resultado.
# 2. Crear un conjunto para registrar las ciudades vistas.
# 3. Recorrer la lista original.
# 4. Si la ciudad no ha sido vista, agregarla al resultado.
# 5. Mostrar la nueva lista.

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

sin_repetidos = []
vistos = set()

for ciudad in ciudades:
    if ciudad not in vistos:
        sin_repetidos.append(ciudad)
        vistos.add(ciudad)

print(sin_repetidos)

# Ejercicio 2. Contar con un diccionario

# Enunciado:
# Dada la lista:
# ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
# Construya un diccionario que muestre cuantas veces
# aparece cada ciudad en la lista.

# Bosquejo:
# 1. Crear un diccionario vacio.
# 2. Recorrer la lista de ciudades.
# 3. Si la ciudad ya existe en el diccionario, sumar 1.
# 4. Si no existe, agregarla con valor 1.
# 5. Mostrar el diccionario.

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

conteo = {}

for ciudad in ciudades:
    if ciudad in conteo:
        conteo[ciudad] += 1
    else:
        conteo[ciudad] = 1

print(conteo)

# Ejercicio 3. Conjuntos en accion

# Enunciado:
# Dados los conjuntos:
# inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
# inscritos_ingles = {"Luis", "Marco", "Ruth"}
# Responder:
# 1. Quienes estan en las dos materias.
# 2. Quienes solo estan en matematica.
# 3. Cuantos estudiantes distintos hay en total.

# Bosquejo:
# 1. Crear los dos conjuntos.
# 2. Obtener la interseccion.
# 3. Obtener la diferencia de matematica con ingles.
# 4. Obtener la union de ambos conjuntos.
# 5. Mostrar los resultados.

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

ambas = inscritos_matematica.intersection(inscritos_ingles)
solo_matematica = inscritos_matematica.difference(inscritos_ingles)
total_estudiantes = len(inscritos_matematica.union(inscritos_ingles))

print("En las dos materias:", ambas)
print("Solo matematica:", solo_matematica)
print("Total de estudiantes distintos:", total_estudiantes)

# Ejercicio 4. De lista de diccionarios a indice

# Enunciado:
# Dada la lista:
# clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}]
# Crear un diccionario con la forma {id: cliente}
# para acceder por id sin recorrer la lista.
# Luego mostrar el nombre del cliente con id 2.

# Bosquejo:
# 1. Crear la lista de clientes.
# 2. Crear el indice usando una sola linea.
# 3. Mostrar el nombre del cliente con id 2.

clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]

indice = {cliente["id"]: cliente for cliente in clientes}

print(indice[2]["nombre"])

# Diferencia de costo:
# Recorrer la lista revisa hasta N registros.
# Acceder por indice requiere una sola busqueda.

# Ejercicio 5. Tuplas como registros inmutables

# Enunciado:
# Dada la lista:
# ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
# Mostrar el mes con la mayor venta y el total,
# usando desempaquetado de tuplas.

# Bosquejo:
# 1. Crear la lista de ventas.
# 2. Calcular el total.
# 3. Obtener el mes con mayor venta.
# 4. Mostrar los resultados.
# 5. Recorrer la lista usando desempaquetado.

ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]

total = sum(monto for _mes, monto in ventas)

mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])

print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")

for mes, monto in ventas:
    print(f"{mes:<10} {monto}")

# Ejercicio 6. Agrupar clientes por ciudad

# Enunciado:
# Agregar al controlador la funcion clientes_por_ciudad()
# que devuelva un diccionario con las ciudades como clave
# y una lista con los nombres de los clientes de cada ciudad.

# Bosquejo:
# 1. Crear un diccionario vacio.
# 2. Recorrer los registros de clientes.
# 3. Obtener la ciudad de cada cliente.
# 4. Agregar el nombre del cliente a la ciudad correspondiente.
# 5. Devolver el diccionario.

def clientes_por_ciudad():
    agrupados = {}

    #for registro in gestor.leer():
  #     ciudad = registro.get("ciudad", "").title() or "Sin ciudad"

      #  agrupados.setdefault(ciudad, []).append(registro["nombre"])

    return agrupados