import json

OUT_FILE = "./out/OUTPUT.json"


class JSONWorker(object):
    """ Класс для работы с JSON файлом"""

    def __init__(self, flag, result):
        self.result = result
        _selector = {
            "get": self.get_jsonwork,
            "set": self.set_jsonwork,
        }
        _selector[flag]()

    def get_jsonwork(self):
        with open(OUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, ensure_ascii=False, indent=4)

    def set_jsonwork(self):
        with open(OUT_FILE, 'a', encoding='utf-8') as f:
            json.dump(self.result, f, ensure_ascii=False, indent=4)
