from enumfields import Enum

class OrderStatus(Enum):
	RECEBIDO = 0
	PREPARO = 1
	PRONTO = 2

class Gender(Enum):
	MASCULINO = 0
	FEMININO = 1
	OUTRO = 2

class UserType(Enum):
	RESTAURANTE = 0
	CLIENTE = 1