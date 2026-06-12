from dataclasses import asdict, fields


class BaseRepository:
    dataset_name = ""
    id_field = "id"

    def __init__(self):
        from app.mocks.mock_data import DATASETS

        self.items = DATASETS[self.dataset_name]
        self.model = self.items[0].__class__ if self.items else None

    def list_all(self):
        return list(self.items)

    def get_by_id(self, item_id):
        if item_id is None:
            return None
        return next((item for item in self.items if getattr(item, self.id_field) == int(item_id)), None)

    def create(self, data):
        next_id = max([getattr(item, self.id_field) for item in self.items], default=0) + 1
        payload = self._coerce(data)
        payload[self.id_field] = next_id
        item = self.model(**payload)
        self.items.append(item)
        return item

    def update(self, item_id, data):
        item = self.get_by_id(item_id)
        if not item:
            return None
        for key, value in data.items():
            if hasattr(item, key):
                setattr(item, key, value)
        return item

    def delete(self, item_id):
        item = self.get_by_id(item_id)
        if not item:
            return False
        self.items.remove(item)
        return True

    def _coerce(self, data):
        if self.model is None:
            return dict(data)
        allowed = {field.name for field in fields(self.model)}
        payload = {key: value for key, value in dict(data).items() if key in allowed}
        for key, value in list(payload.items()):
            if isinstance(value, str):
                payload[key] = value.strip()
        return payload

    def to_dict(self, item):
        return asdict(item)
