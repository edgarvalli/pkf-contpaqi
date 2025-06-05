def eliminarDuplicados(lista_cuentas, año_prioritario=None):
    """
    Elimina cuentas duplicadas (mismo código) priorizando:
    1. El año_prioritario si se especifica
    2. El año más reciente si no se especifica año_prioritario

    Args:
        lista_cuentas: Lista de diccionarios con información de cuentas
        año_prioritario: Año que debe tener prioridad (opcional)

    Returns:
        Lista filtrada sin cuentas duplicadas
    """
    cuentas_por_codigo = {}

    for cuenta in lista_cuentas:
        codigo = cuenta["cuenta"]
        ejercicio = cuenta["ejercicio"]

        if codigo not in cuentas_por_codigo:
            cuentas_por_codigo[codigo] = cuenta
        else:
            actual = cuentas_por_codigo[codigo]

            # Priorizar el año específico si se proporciona
            if año_prioritario is not None:
                if (
                    ejercicio == año_prioritario
                    and actual["ejercicio"] != año_prioritario
                ):
                    cuentas_por_codigo[codigo] = cuenta
            else:
                # Si no hay año prioritario, usar el más reciente
                if ejercicio > actual["ejercicio"]:
                    cuentas_por_codigo[codigo] = cuenta

    return list(cuentas_por_codigo.values())
