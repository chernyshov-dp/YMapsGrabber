OUT_FILE = "./out/OUTPUT.json"


class JSONWorker(object):
    def __init__(self, flag, result):
        self.result = result
        _selector = {
            "get": self.get_jsonwork,
            "set": self.set_jsonwork,
        }
        _selector[flag]()

    def get_jsonwork(self):
        f = open(OUT_FILE, "w")
        f.close()

    def set_jsonwork(self):
        f = open(OUT_FILE, "a")
        f.write(self.result)
        f.close()
