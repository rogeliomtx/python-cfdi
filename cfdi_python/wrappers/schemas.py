import os

import xmlschema

from .locations import timbre_fiscal_digital11
from .xsds import xsd_dir

cfdi33_path = os.path.join(xsd_dir, "cfdv33.xsd")
cfdi40_path = os.path.join(xsd_dir, "cfdv40.xsd")


def get_context():
    return dict(
        locations=[timbre_fiscal_digital11],
        converter=xmlschema.AbderaConverter,
        validation="skip",
        allow="local",
    )


def get_schema(version=3.3, context=None):
    context = context or get_context()
    if version == 3.3:
        return xmlschema.XMLSchema(cfdi33_path, **context)
    elif version == 4:
        return xmlschema.XMLSchema(cfdi40_path, **context)

    raise Exception(f"Version {version} not supported")
