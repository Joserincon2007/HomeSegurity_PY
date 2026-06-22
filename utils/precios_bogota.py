PRECIOS_M2 = {
    "Chapinero": 7500000,
    "Usaquen": 8200000,
    "Suba": 5200000,
    "Engativa": 4200000,
    "Kennedy": 3800000,
    "Fontibon": 4300000,
    "Bosa": 3000000,
    "Ciudad Bolivar": 2500000,
    "Teusaquillo": 7000000,
    "Barrios Unidos": 6100000,
    "Puente Aranda": 4700000,
    "Antonio Nariño": 5400000
}

def calcular_avaluo(area, localidad, estrato, antiguedad, parqueadero):

    precio_base = PRECIOS_M2.get(localidad, 4000000)

    valor = area * precio_base

    # ajuste por estrato
    valor *= (1 + (estrato - 3) * 0.05)

    # depreciación por antigüedad
    valor *= (1 - (antiguedad * 0.005))

    # parqueadero suma valor
    if parqueadero:
        valor += 15000000

    descripcion = f"""
El valor fue calculado según el precio promedio del metro cuadrado
en {localidad}, ajustado por estrato socioeconómico,
antigüedad del inmueble y características adicionales.
"""

    return precio_base, round(valor, 2), descripcion