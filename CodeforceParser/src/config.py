import configparser


class Config(object):
    __config = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__config = configparser.ConfigParser()
            cls.__config.read("../deployment/configs/config.conf")

            config = dict()
            config["DEFAULT"] = cls.__config["DEFAULT"]

            sections = cls.__config.sections()
            for section in sections:
                config[section] = cls.__config[section]

            cls.__instance = super(Config, cls).__new__(cls)
        return cls.__instance

    def __getitem__(self, key):
        return Config.__config[key]
