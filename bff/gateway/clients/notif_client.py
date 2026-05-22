from .base import ServiceClient


class NotificacionClient(ServiceClient):
    """Cliente para el microservicio de Notificaciones."""

    def __init__(self):
        super().__init__("NOTIFICACIONES_URL", "notificaciones")

    async def enviar_email(self, destino: str, asunto: str, mensaje: str) -> dict:
        return await self.post("/email", {"destino": destino, "asunto": asunto, "mensaje": mensaje})

    async def enviar_sms(self, destino: str, mensaje: str) -> dict:
        return await self.post("/sms", {"destino": destino, "mensaje": mensaje})
