from ..clients import usuarios_client
from ..schemas.logros import LogroOut, LogroUsuarioOut, VerificarLogrosIn


def _get_uat(request) -> str:
    return getattr(request, "user", {}).get("uat", "")


def _ensure_list(resp):
    return resp if isinstance(resp, list) else (resp.get("results", []) if isinstance(resp, dict) and "results" in resp else [])


async def listar_logros(request) -> list[LogroOut]:
    uat = _get_uat(request)
    data = _ensure_list(await usuarios_client.listar_logros(token=uat))
    return [LogroOut(**l) for l in data]


async def mis_logros(request) -> list[LogroUsuarioOut]:
    uat = _get_uat(request)
    data = _ensure_list(await usuarios_client.mis_logros(token=uat))
    return [LogroUsuarioOut(**l) for l in data]


async def verificar(request, stats: VerificarLogrosIn) -> dict:
    uat = _get_uat(request)
    result = await usuarios_client.verificar_logros(stats.model_dump(), token=uat)
    return result
