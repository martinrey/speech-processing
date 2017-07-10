class Seccion(object):
    @classmethod
    def para(cls, pedido_de_usuario):
        for subclass in cls.__subclasses__():
            if subclass.puede_procesar(pedido_de_usuario):
                return subclass()
        raise Exception('No se puede procesar el pedido')

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        raise NotImplementedError

    def __init__(self, sistema_de_dialogo):
        self.sistema_de_dialogo = sistema_de_dialogo

    def ejecutar(self):
        raise NotImplementedError


class SeccionRepetirPregunta(Seccion):
    def ejecutar(self):
        pass

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return "repetir" in pedido_de_usuario