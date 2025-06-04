from lib.databases import Databases, DBConfig
from .contabilidad import ContabilidadSDK

class ContpaqISDK:
    
    sqlconfig: DBConfig
    contabilidad: ContabilidadSDK
    
    def __init__(self, dbconfig: dict):
        self.sqlconfig = DBConfig(**dbconfig)
        self.contabilidad = ContabilidadSDK(self.sqlconfig)