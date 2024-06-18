# Validaciones para la clase CustomUser
def validator_role(value):
    if 1 > value > 3:
        raise ValueError('El rol solo puede ser 1, 2 o 3')