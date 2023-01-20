from cfdi_python import CFDI
from tests.assets import base_dir


def test_model_complete_timbre_fiscal_digital11():
    with open(f"{base_dir}/cfdi40/cfdi40.xml") as file:
        cfdi = CFDI(file, version=4)
        model = cfdi.to_model()

        assert model.version == "4.0"

        assert model.complemento.timbre_fiscal_digital is not None

        tfd = model.complemento.timbre_fiscal_digital
        assert tfd.version == "1.1"
        assert (
            tfd.schema_location
            == "http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd"
        )
        assert tfd.rfc_prov_certif == "PUT211201AX4"
        assert tfd.uuid == "499e9a70-36ac-448a-bbd9-f3f52102e4be"
        assert tfd.fecha_timbrado == "2021-12-19T21:19:11"
        assert tfd.sello_cfd == "__SELLO_CFD__"
        assert tfd.no_certificado_sat == "30001000000300023699"
        assert tfd.sello_sat == "__SELLO_SAT__"

        # timbreFiscalDigital v1.1 only
        assert tfd.leyenda is None
