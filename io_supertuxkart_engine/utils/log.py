class STKcoreLog:
    _listeners = []

    @staticmethod
    def ajouter(msg):
        print(msg)

        for i in STKcoreLog._listeners:
            i(msg)

    @classmethod
    def ajout_listeners(cls, i):
        cls._listeners.append(i)

    @classmethod
    def supr_listeners(cls, i):
        cls._listeners.remove(i)