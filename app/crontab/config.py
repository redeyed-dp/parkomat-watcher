from yaml import safe_load, safe_dump

class Config():
    @staticmethod
    def read(file):
        f = open(file)
        conf = safe_load(f)
        f.close()
        return conf

    @staticmethod
    def write(file, conf):
        f = open(file, 'w')
        safe_dump(conf, f)
        f.close()