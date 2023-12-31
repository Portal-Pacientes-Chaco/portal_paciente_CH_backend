from typing import Dict

from app.gear.hcd.hcd_impl import HSIImplChaco
from app.routes.common import router_hcd


@router_hcd.get("/turn", tags=["HCD"])
async def get_turnos(dni: str, dni_tipo: int, genero_id: int) -> Dict:
    hcd_impl = HSIImplChaco()
    return hcd_impl.get_turnos(dni, dni_tipo, genero_id)


@router_hcd.get("/clinichistory", tags=["HCD"])
async def get_hc(dni: str, dni_tipo: int, genero_id: int) -> Dict:
    hcd_impl = HSIImplChaco()
    return hcd_impl.get_hc(dni, dni_tipo, genero_id)


@router_hcd.get("/genders", tags=["HCD"])
async def get_genders() -> Dict:
    hcd_impl = HSIImplChaco()
    return hcd_impl.get_genders()


@router_hcd.get("/documenttype", tags=["HCD"])
async def get_documents_type() -> Dict:
    hcd_impl = HSIImplChaco()
    return hcd_impl.get_documents_type()
