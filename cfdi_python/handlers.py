import json

from jsonpickle.pickler import Pickler

from cfdi_python.wrappers.cfdi33 import CFDI as CFDIv33
from cfdi_python.wrappers.cfdi40 import CFDI as CFDIv40
from cfdi_python.wrappers.schemas import get_schema


class CFDI:
    def __init__(self, file, version=3.3, context=None):
        self.file = file

        self.context = context
        self.version = version
        self.schema = get_schema(self.version, context=self.context)

        self._dict = None
        self._raw = None
        self._model = None
        self._json = None

        # variables auxiliares
        # para convertir dict > JSON
        self._pickler = Pickler(use_decimal=False)

    def to_raw(self, file=None):
        if self._raw and file is None:
            return self._raw

        file = file or self.file
        self._raw = self.schema.to_dict(file)
        return self._raw

    def to_model(self, file=None):
        if self._model and file is None:
            return self._model

        file = file or self.file
        if self.version == 3.3:
            self._model = CFDIv33(self.to_raw(file))
        elif self.version == 4.0:
            self._model = CFDIv40(self.to_raw(file))
        return self._model

    def to_dict(self, file=None):
        if self._dict and file is None:
            return self._dict

        file = file or self.file
        self._dict = self._pickler.flatten(self.to_model(file))
        return self._dict

    def to_json(self, file=None):
        if self._json:
            return self._json

        file = file or self.file
        self._json = json.dumps(self.to_dict(file))
        return self._json
