class CrudService:
    repo_class = None
    int_fields = set()
    float_fields = set()

    def __init__(self):
        self.repo = self.repo_class()

    def listar(self):
        return self.repo.list_all()

    def obter(self, item_id):
        return self.repo.get_by_id(item_id)

    def salvar(self, data, item_id=None):
        payload = self._payload(data)
        return self.repo.update(item_id, payload) if item_id else self.repo.create(payload)

    def remover(self, item_id):
        return self.repo.delete(item_id)

    def _payload(self, data):
        payload = dict(data)
        for key in self.int_fields:
            if key in payload and payload[key] != "":
                payload[key] = int(payload[key])
        for key in self.float_fields:
            if key in payload and payload[key] != "":
                payload[key] = float(payload[key])
        return payload
