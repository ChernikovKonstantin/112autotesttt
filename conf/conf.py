class Conf:
    configuration = dict()

    def __new__(cls):
        """
        Singleton
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Conf, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_config(cls):
        return cls.configuration
