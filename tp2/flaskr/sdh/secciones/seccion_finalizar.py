import os

from sdh.secciones.seccion import Seccion


class SeccionFinalizar(Seccion):
    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return "nada" in pedido_de_usuario or "fin" in pedido_de_usuario

    def ejecutar(self):
        os.system("play sounds/chau.wav")
        self.sistema_de_dialogo.finalizar()