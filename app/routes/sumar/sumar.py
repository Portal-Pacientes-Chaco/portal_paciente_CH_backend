from typing import Dict
from app.schemas.sumar_result import SumarResult
from app.gear.sumar.sumar_impl import SumarImplChaco, Vacunacion, GetData
from app.routes.common import router_sumar
from app.gear.local.sumar import get_afiliado_data


@router_sumar.get("/me", tags=["SUMAR"])
async def get_me() -> Dict:
    sumar_impl = SumarImplChaco()
    return sumar_impl.get_me()


@router_sumar.get("/prestaciones", tags=["SUMAR"])
async def get_prestaciones(dni: str) -> Dict:
    sumar_impl = SumarImplChaco()
    return sumar_impl.get_prestaciones(dni)


@router_sumar.get("/efectores", tags=["SUMAR"])
async def get_efectores() -> Dict:
    sumar_impl = SumarImplChaco()
    return sumar_impl.get_efectores()


@router_sumar.get("/efectores-priorizados", tags=["SUMAR"])
async def get_efectores_priorizados() -> Dict:
    sumar_impl = SumarImplChaco().get_efectores()
    efectores = []

    for i in sumar_impl:
        if i['cuie'] == 'H00895' or i['cuie'] == 'H00608' or i['cuie'] == 'H00613' or i['cuie'] == 'H00494' or i['cuie'] == 'H00878':
            efectores.append(i)
    return efectores


@router_sumar.get("/vaccines", tags=["SUMAR"])
async def get_vaccines(dni: str) -> Dict:
    sumar_impl = Vacunacion()
    return sumar_impl.get_vaccines(dni)

@router_sumar.get("/ceb/{dni_afiliado}", tags=["SUMAR", "ceb"], response_model=Dict[str, bool])
async def get_ceb_value(dni_afiliado: str) -> Dict[str, bool]:
    ceb_value = GetData.get_ceb_value(dni_afiliado)
    return {"msg": ceb_value}

@router_sumar.get("/data/{dni_afiliado}", tags=["SUMAR", "data"], response_model=SumarResult)
async def get_sumar_data(dni_afiliado: str) -> SumarResult:
    return get_afiliado_data(dni_afiliado)
