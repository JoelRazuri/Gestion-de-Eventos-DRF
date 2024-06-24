from datetime import datetime

# Validaciones para la clase Event
def validator_is_organizer(user):
    if user.role != 1 or user.role != 2:
        raise ValueError('El usuario no es organizador')

def validator_capacity(capacity):
    if capacity < 0:
        raise ValueError('La capacidad no puede ser negativa')

    if capacity == 0:
        raise ValueError('La capacidad no puede ser 0')
    
    if capacity > 1000:
        raise ValueError('La capacidad no puede ser mayor a 1000')

def validator_is_valid_date(date):
    if date < datetime.now():
        raise ValueError('La fecha no puede ser una fecha pasada') 

# Validaciones para la clase Rating
def validator_rating(rating):
    if 1 > rating > 5:
        raise ValueError('El rating solo puede ser entre 1 y 5')
