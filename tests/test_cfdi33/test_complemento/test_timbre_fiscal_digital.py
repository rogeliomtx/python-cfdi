from cfdi_python import CFDI
from tests.assets import base_dir


def test_model_complete_timbre_fiscal_digital11():
    with open(f"{base_dir}/cfdi33/cfdi33.xml") as file:
        cfdi = CFDI(file)
        model = cfdi.to_model()

        assert model.version == "3.3"

        assert model.complemento.timbre_fiscal_digital is not None

        tfd = model.complemento.timbre_fiscal_digital
        assert tfd.version == "1.1"
        assert (
            tfd.schema_location
            == "http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd"
        )
        assert tfd.rfc_prov_certif == "AAA010101AAA"
        assert tfd.uuid == "ea8152af-b116-4812-817a-3b4f9617c99c"
        assert tfd.fecha_timbrado == "2017-05-10T15:22:28"
        assert tfd.sello_cfd == "__SELLO_CFD__"
        assert tfd.no_certificado_sat == "20001000000100005761"
        assert tfd.sello_sat == "__SELLO_SAT__"

        # timbreFiscalDigital v1.1 only
        assert tfd.leyenda is None
