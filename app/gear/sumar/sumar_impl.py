import requests
import json
from typing import Dict
from app.gear.sumar.database import engine
from app.gear.sumar.config import ME_ENDPOINT, PRESTACIONES_ENDPOINT, EFECTORES_ENDPOINT
from app.gear.sumar.login import SumarChacoLogin
from app.gear.sumar.sql_sumar import SQL_SUMAR
from app.gear.log.main_logger import MainLogger, logging
from typing import Optional
from datetime import datetime, date
from dataclasses import dataclass


logger = MainLogger()
module = logging.getLogger(__name__)
@dataclass(order=True, frozen=True)
class Result:
    id_afiliado: int
    nombre: str
    tipo_doc: str
    dni: str
    clase_doc: str
    sexo: str
    fecha_nacimiento: Optional[date]
    fecha_comprobante: Optional[datetime]
    periodo: Optional[str]
    peso: Optional[float]
    tension_arterial: Optional[str]
    diagnostico: Optional[str]
    codigo: Optional[str]
    grupo: Optional[str]
    subgrupo: Optional[str]
    descripcion: Optional[str]
    dias_uti: Optional[int]
    dias_sala: Optional[int]
    dias_total: Optional[int]

class SumarImplChaco:
    def __init__(self):
        self.token = SumarChacoLogin().login()

    @property
    def header(self):
        return{
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_me(self) -> Dict:
        url = f"{ME_ENDPOINT}"
        response = requests.get(url, headers=self.header)
        return json.loads(response.text)

    def get_prestaciones(self, dni: str) -> Dict:
        url = f"{PRESTACIONES_ENDPOINT}"
        payload = json.dumps({
            "dni": f"{dni}"
        })
        response = requests.get(url, headers=self.header, data=payload)
        return json.loads(response.text)

    def get_efectores(self) -> Dict:
        url = f"{EFECTORES_ENDPOINT}"
        response = requests.get(url, headers=self.header)
        return json.loads(response.text)


class Vacunacion:
    def get_vaccines(self, dni: str):
        prestaciones = SumarImplChaco()
        vacunas = prestaciones.get_prestaciones(dni)
        idObjetos = []
        for n in vacunas:
            idObjetos.append(n['idObj'])
        vacunas_list = []
        for x in idObjetos:
            if x == "IMV015A98" or x == "IMV016A98" or x == "IMV017A98" or x == "IMV018A98" or x == "IMV019A98" or x == "IMV013A98" or x == "IMV001A98" or x == "IMV006A98" or x == "IMV002A98" or x == "IMV003A98" or x == "IMV009A98" or x == "IMV005A98" or x == "IMV012A98" or x == "IMV007A98" or x == "IMV004A98" or x == "IMV008A98" or x == "IMV010A98" or x == "IMV011A98" or x == "IMV014A98":
                vacunas_list.append(x)
        return vacunas_list

class GetData:
    def __init__(self):
        self.engine = engine

    def get_data(self, dni_afiliado: str):
        sentence = SQL_SUMAR.format(dni_afiliado=dni_afiliado)
        logger.log_info_message(f"SQL to run, {sentence}", module)
        with self.engine.connect() as conn:
            exec_result = conn.execute(sentence)
            result = [Result(*row.values()) for row in exec_result]
        return result

    def get_ceb_value(self, dni_afiliado: str) -> bool:
        sentence = f"SELECT smiafiliados.ceb FROM nacer.smiafiliados WHERE smiafiliados.afidni = '{dni_afiliado}'"
        with self.engine.connect() as conn:
            row = conn.execute(sentence).scalar()
        return row == "S"