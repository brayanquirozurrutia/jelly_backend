
def valida_rut(rut: str) -> bool:
    """
    Validates a Chilean RUT (Rol Único Tributario).

    Args:
        rut (str): The RUT to validate. Should be provided without dots, with a hyphen, and including the verification digit (e.g., 19703190-5).

    Returns:
        bool: True if the RUT is valid, False if it does not meet the requirements.
    """
    rut_sin_digito = rut[:-2]
    if rut_sin_digito.isdigit() and (7 <= len(rut_sin_digito) <= 8):
        lista_rut_enteros = [int(digito) for digito in rut_sin_digito]
        lista_rut_enteros.reverse()
        ponderador, suma_producto = 2, 0
        for digito in lista_rut_enteros:
            producto = ponderador * digito
            ponderador += 1
            suma_producto += producto
            if ponderador == 8:
                ponderador = 2
        resto = suma_producto % 11
        diferencia = 11 - resto
        if diferencia == 11:
            digito_verificador = 0
        elif diferencia == 10:
            digito_verificador = 'k'
        else:
            digito_verificador = diferencia
        return str(digito_verificador).lower() == rut[-1].lower()
    return False
