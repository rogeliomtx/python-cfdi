from cfdi_python import CFDI
from tests.assets import base_dir
from cfdi_python.wrappers.schemas import get_context
from cfdi_python.wrappers.locations import nomina12b, timbre_fiscal_digital11


def test_context():
    """
    Asegura que la configuración cargue siempre el timbre fiscal, no genere
    excepciones al validar el doc, y que mantenga una configuración local
    """
    context = get_context()

    # timbre fiscal digital siempre viene precargado para versiones 4.0 y 3.3
    assert context.get("locations") is not None
    assert context.get("locations") == [timbre_fiscal_digital11]

    assert context.get("validation") == "skip"
    assert context.get("allow") == "local"


def test_update_context():
    """
    Agrega complemento nomina1.2 para leer un recibo de nómina
    """
    context = get_context()
    context["locations"] += [nomina12b]

    with open(f"{base_dir}/cfdi33/complemento/nomina12.xml") as file:
        cfdi = CFDI(file, context=context)
        model = cfdi.to_model()
        assert model.version == "3.3"
