from dataclasses import dataclass

class BaseContpaq:
    created_at: str
    updated_at: str 

@dataclass
class Empresa():
    nombre: str
    dbname: str
    

@dataclass
class Cuenta(BaseContpaq):
    id: int
    cuenta: str
    nombre: str
    bd: str
    categoriaid: int
    created_at: str
    updated_at: str

    def todict(self):
        return {
            "id": self.id,
            "cuenta": self.cuenta,
            "nombre": self.nombre,
            "bd": self.bd,
            "categoriaid": self.categoriaid,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }