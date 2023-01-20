from cfdi_python import CFDI
from tests.assets import base_dir


def test_model_min_cfdi33():
    with open(f"{base_dir}/cfdi33/cfdi33_min.xml") as file:
        cfdi = CFDI(file)
        model = cfdi.to_model()
        assert model.version == "3.3"

        assert model.serie is None
        assert model.folio is None
        assert model.fecha == "2017-05-01T01:23:59"
        assert model.sello == "__SELLO__"
        assert model.forma_pago == "02"
        assert model.no_certificado == "40001000000300000337"
        assert model.certificado == "__CERTIFICADO__"
        assert model.sub_total == 1000
        assert model.moneda == "MXN"
        assert model.total == 1500
        assert model.tipo_de_comprobante == "I"
        assert model.metodo_pago is None
        assert model.lugar_expedicion == "45079"
        assert model.condiciones_de_pago is None
        assert model.descuento is None
        assert model.tipo_cambio is None
        assert model.confirmacion is None

        # emisor
        assert model.emisor is not None
        assert model.emisor.rfc == "AAA010101AAA"
        assert model.emisor.nombre is None
        assert model.emisor.regimen_fiscal == "622"

        # receptor
        assert model.receptor is not None
        assert model.receptor.rfc == "BASJ600902KL9"
        assert model.receptor.nombre is None
        assert model.receptor.uso_cfdi == "G03"
        assert model.receptor.residencia_fiscal is None
        assert model.receptor.num_reg_id_trib is None

        # conceptos
        assert model.conceptos is not None
        assert len(model.conceptos) == 1

        concepto = model.conceptos[0]
        assert concepto.clave_prod_serv == "01010101"
        assert concepto.cantidad == 1.5
        assert concepto.clave_unidad == "C81"
        assert concepto.descripcion == "ACERO"
        assert concepto.valor_unitario == 1500000
        assert concepto.importe == 2250000
        assert concepto.no_identificacion is None
        assert concepto.unidad is None
        assert concepto.descuento is None
        assert concepto.impuestos is None
        assert concepto.complemento_concepto is None
        assert concepto.cuenta_predial is None
        assert concepto.informacion_aduanera == []
        assert concepto.parte == []

        # impuestos
        assert model.impuestos is None

        # complemento
        assert model.complemento is None

        # cfdi_relacionados
        assert model.cfdi_relacionados is None

        # addenda
        assert model.addenda is None


def test_model_complete_cfdi33():
    with open(f"{base_dir}/cfdi33/cfdi33.xml") as file:
        cfdi = CFDI(file)
        model = cfdi.to_model()

        assert model.version == "3.3"
        assert model.serie == "A"
        assert model.folio == "123ABC"
        assert model.fecha == "2017-05-01T01:23:59"
        assert model.sello == "__SELLO__"
        assert model.forma_pago == "02"
        assert model.no_certificado == "40001000000300000337"
        assert model.certificado == "__CERTIFICADO__"
        assert model.sub_total == 1000
        assert model.moneda == "MXN"
        assert model.total == 1500
        assert model.tipo_de_comprobante == "I"
        assert model.metodo_pago == "PUE"
        assert model.lugar_expedicion == "45079"
        assert model.condiciones_de_pago == "CONDICIONES"
        assert model.descuento == 0
        assert model.tipo_cambio == 1.0
        assert model.confirmacion == "Az123"

        # emisor
        assert model.emisor is not None
        assert model.emisor.rfc == "AAA010101AAA"
        assert model.emisor.nombre == "Esta es una demostración"
        assert model.emisor.regimen_fiscal == "622"

        # receptor
        assert model.receptor is not None
        assert model.receptor.rfc == "BASJ600902KL9"
        assert model.receptor.nombre == "Juanito Bananas De la Sierra"
        assert model.receptor.uso_cfdi == "G03"
        assert model.receptor.residencia_fiscal == "MEX"
        assert model.receptor.num_reg_id_trib == "987654321"

        # conceptos
        assert model.conceptos is not None
        assert len(model.conceptos) == 3

        concepto = model.conceptos[0]
        assert concepto.clave_prod_serv == "01010101"
        assert concepto.cantidad == 1.5
        assert concepto.clave_unidad == "C81"
        assert concepto.descripcion == "ACERO"
        assert concepto.valor_unitario == 1500000
        assert concepto.importe == 2250000
        assert concepto.no_identificacion == "00001"
        assert concepto.unidad == "TONELADA"
        assert concepto.descuento is None
        assert concepto.impuestos is None
        assert concepto.complemento_concepto is None
        assert concepto.cuenta_predial is not None
        assert concepto.cuenta_predial.numero == "51888"
        assert concepto.informacion_aduanera == []
        assert concepto.parte == []

        concepto = model.conceptos[1]
        assert concepto.clave_prod_serv == "95141904"
        assert concepto.cantidad == 1.3
        assert concepto.clave_unidad == "WEE"
        assert concepto.descripcion == "ALUMINIO"
        assert concepto.valor_unitario == 1500
        assert concepto.importe == 2400
        assert concepto.no_identificacion == "00002"
        assert concepto.unidad == "TONELADA"
        assert concepto.descuento is None

        # concepto.impuestos
        assert concepto.impuestos is not None
        assert len(concepto.impuestos.traslados) == 1
        traslado = concepto.impuestos.traslados[0]
        assert traslado.base == 2400
        assert traslado.impuesto == "002"
        assert traslado.tipo_factor == "Tasa"
        assert traslado.tasa_o_cuota == 1.6
        assert traslado.importe == 384

        assert len(concepto.impuestos.retenciones) == 1
        retencion = concepto.impuestos.retenciones[0]
        assert retencion.impuesto == "001"
        assert retencion.importe == 264

        # concepto.complemento_concepto
        assert concepto.complemento_concepto is None

        # concepto.cuenta_predial
        assert concepto.cuenta_predial is None

        # concepto.informacion_aduanera
        assert concepto.informacion_aduanera is not None
        assert len(concepto.informacion_aduanera) == 1
        informacion_aduanera = concepto.informacion_aduanera[0]
        assert informacion_aduanera.numero_pedimento == "15  48  4567  6001234"

        # concepto.parte
        assert concepto.parte == []

        concepto = model.conceptos[2]
        assert concepto.clave_prod_serv == "84101604"
        assert concepto.cantidad == 1.7
        assert concepto.clave_unidad == "G66"
        assert concepto.descripcion == "ZAMAC"
        assert concepto.valor_unitario == 10000
        assert concepto.importe == 17000
        assert concepto.no_identificacion == "00003"
        assert concepto.unidad == "TONELADA"
        assert concepto.descuento == 0

        # concepto.complemento_concepto
        assert concepto.complemento_concepto is None

        # concepto.cuenta_predial
        assert concepto.cuenta_predial is None

        # concepto.informacion_aduanera
        assert concepto.informacion_aduanera == []

        # concepto.parte
        assert concepto.parte is not None
        assert len(concepto.parte) == 1
        parte = concepto.parte[0]
        assert parte.clave_prod_serv == "25201513"
        assert parte.no_identificacion == "055155"
        assert parte.cantidad == 1.0
        assert parte.descripcion == "PARTE EJEMPLO"
        assert parte.unidad == "UNIDAD"
        assert parte.valor_unitario == 1
        assert parte.importe == 1

        # concepto.parte.informacion_aduanera
        assert parte.informacion_aduanera is not None
        assert len(parte.informacion_aduanera) == 2
        assert parte.informacion_aduanera[0].numero_pedimento == "15  48  4567  6001235"
        assert parte.informacion_aduanera[1].numero_pedimento == "15  48  4567  6001236"

        # impuestos
        assert model.impuestos is not None
        assert model.impuestos.total_impuestos_trasladados == 360000
        assert model.impuestos.total_impuestos_retenidos == 247500

        assert model.impuestos.retenciones is not None
        assert len(model.impuestos.retenciones) == 2

        retencion = model.impuestos.retenciones[0]
        assert retencion.impuesto == "001"
        assert retencion.importe == 247000

        retencion = model.impuestos.retenciones[1]
        assert retencion.impuesto == "003"
        assert retencion.importe == 500

        assert model.impuestos.traslados is not None
        assert len(model.impuestos.traslados) == 1

        traslado = model.impuestos.traslados[0]
        assert traslado.impuesto == "002"
        assert traslado.tipo_factor == "Tasa"
        assert traslado.tasa_o_cuota == 1.6
        assert traslado.importe == 360000

        # complemento
        assert model.complemento is not None
        assert model.complemento.timbre_fiscal_digital is not None

        # cfdi_relacionados
        assert model.cfdi_relacionados is not None
        assert model.cfdi_relacionados.tipo_relacion == "02"
        assert model.cfdi_relacionados.cfdi_relacionados is not None
        assert len(model.cfdi_relacionados.cfdi_relacionados) == 1
        cfdi_relacionado = model.cfdi_relacionados.cfdi_relacionados[0]
        assert cfdi_relacionado.uuid == "ED1752FE-E865-4FF2-BFE1-0F552E770DC9"

        # addenda
        assert model.addenda is None


def test_json_complete_cfdi33():
    with open(f"{base_dir}/cfdi33/cfdi33.xml") as file:
        cfdi = CFDI(file)
        json_obj = cfdi.to_json()

        assert type(json_obj) == str


def test_dict_complete_cfdi33():
    with open(f"{base_dir}/cfdi33/cfdi33.xml") as file:
        cfdi = CFDI(file)
        dict_obj = cfdi.to_dict()

        assert type(dict_obj) == dict
        assert dict_obj.get("version") == "3.3"
        assert dict_obj.get("serie") == "A"
        assert dict_obj.get("folio") == "123ABC"
        assert dict_obj.get("fecha") == "2017-05-01T01:23:59"
        assert dict_obj.get("sello") == "__SELLO__"
        assert dict_obj.get("forma_pago") == "02"
        assert dict_obj.get("no_certificado") == "40001000000300000337"
        assert dict_obj.get("certificado") == "__CERTIFICADO__"
        assert dict_obj.get("sub_total") == 1000
        assert dict_obj.get("moneda") == "MXN"
        assert dict_obj.get("total") == 1500
        assert dict_obj.get("tipo_de_comprobante") == "I"
        assert dict_obj.get("metodo_pago") == "PUE"
        assert dict_obj.get("lugar_expedicion") == "45079"
        assert dict_obj.get("condiciones_de_pago") == "CONDICIONES"
        assert dict_obj.get("descuento") == 0
        assert dict_obj.get("tipo_cambio") == 1
        assert dict_obj.get("confirmacion") == "Az123"

        # emisor
        assert dict_obj.get("emisor") is not None
        assert dict_obj.get("emisor").get("rfc") == "AAA010101AAA"
        assert dict_obj.get("emisor").get("nombre") == "Esta es una demostración"
        assert dict_obj.get("emisor").get("regimen_fiscal") == "622"

        # receptor
        assert dict_obj.get("receptor") is not None
        assert dict_obj.get("receptor").get("rfc") == "BASJ600902KL9"
        assert dict_obj.get("receptor").get("nombre") == "Juanito Bananas De la Sierra"
        assert dict_obj.get("receptor").get("uso_cfdi") == "G03"
        assert dict_obj.get("receptor").get("residencia_fiscal") == "MEX"
        assert dict_obj.get("receptor").get("num_reg_id_trib") == "987654321"

        # conceptos
        assert dict_obj.get("conceptos") is not None
        assert len(dict_obj.get("conceptos")) == 3

        concepto = dict_obj.get("conceptos")[0]
        assert concepto.get("clave_prod_serv") == "01010101"
        assert concepto.get("cantidad") == 1.5
        assert concepto.get("clave_unidad") == "C81"
        assert concepto.get("descripcion") == "ACERO"
        assert concepto.get("valor_unitario") == 1500000
        assert concepto.get("importe") == 2250000
        assert concepto.get("no_identificacion") == "00001"
        assert concepto.get("unidad") == "TONELADA"
        assert concepto.get("descuento") is None
        assert concepto.get("impuestos") is None
        assert concepto.get("complemento_concepto") is None
        assert concepto.get("cuenta_predial") is not None
        assert concepto.get("cuenta_predial").get("numero") == "51888"
        assert concepto.get("informacion_aduanera") == []
        assert concepto.get("parte") == []

        concepto = dict_obj.get("conceptos")[1]
        assert concepto.get("clave_prod_serv") == "95141904"
        assert concepto.get("cantidad") == 1.3
        assert concepto.get("clave_unidad") == "WEE"
        assert concepto.get("descripcion") == "ALUMINIO"
        assert concepto.get("valor_unitario") == 1500
        assert concepto.get("importe") == 2400
        assert concepto.get("no_identificacion") == "00002"
        assert concepto.get("unidad") == "TONELADA"
        assert concepto.get("descuento") is None

        # concepto.get("impuestos")
        assert concepto.get("impuestos") is not None
        assert len(concepto.get("impuestos").get("traslados")) == 1
        traslado = concepto.get("impuestos").get("traslados")[0]
        assert traslado.get("base") == 2400
        assert traslado.get("impuesto") == "002"
        assert traslado.get("tipo_factor") == "Tasa"
        assert traslado.get("tasa_o_cuota") == 1.600000
        assert traslado.get("importe") == 384

        assert len(concepto.get("impuestos").get("retenciones")) == 1
        retencion = concepto.get("impuestos").get("retenciones")[0]
        assert retencion.get("impuesto") == "001"
        assert retencion.get("importe") == 264

        # concepto.get("complemento_concepto")
        assert concepto.get("complemento_concepto") is None

        # concepto.get("cuenta_predial")
        assert concepto.get("cuenta_predial") is None

        # concepto.get("informacion_aduanera")
        assert concepto.get("informacion_aduanera") is not None
        assert len(concepto.get("informacion_aduanera")) == 1
        informacion_aduanera = concepto.get("informacion_aduanera")[0]
        assert informacion_aduanera.get("numero_pedimento") == "15  48  4567  6001234"

        # concepto.get("parte")
        assert concepto.get("parte") == []

        concepto = dict_obj.get("conceptos")[2]
        assert concepto.get("clave_prod_serv") == "84101604"
        assert concepto.get("cantidad") == 1.7
        assert concepto.get("clave_unidad") == "G66"
        assert concepto.get("descripcion") == "ZAMAC"
        assert concepto.get("valor_unitario") == 10000
        assert concepto.get("importe") == 17000
        assert concepto.get("no_identificacion") == "00003"
        assert concepto.get("unidad") == "TONELADA"
        assert concepto.get("descuento") == 0

        # concepto.get("complemento_concepto")
        assert concepto.get("complemento_concepto") is None

        # concepto.get("cuenta_predial")
        assert concepto.get("cuenta_predial") is None

        # concepto.get("informacion_aduanera")
        assert concepto.get("informacion_aduanera") == []

        # concepto.get("parte")
        assert concepto.get("parte") is not None
        assert len(concepto.get("parte")) == 1
        parte = concepto.get("parte")[0]
        assert parte.get("clave_prod_serv") == "25201513"
        assert parte.get("no_identificacion") == "055155"
        assert parte.get("cantidad") == 1.0
        assert parte.get("descripcion") == "PARTE EJEMPLO"
        assert parte.get("unidad") == "UNIDAD"
        assert parte.get("valor_unitario") == 1
        assert parte.get("importe") == 1

        # concepto.get("parte").informacion_aduanera
        assert parte.get("informacion_aduanera") is not None
        assert len(parte.get("informacion_aduanera")) == 2
        assert (
            parte.get("informacion_aduanera")[0].get("numero_pedimento")
            == "15  48  4567  6001235"
        )
        assert (
            parte.get("informacion_aduanera")[1].get("numero_pedimento")
            == "15  48  4567  6001236"
        )

        # impuestos
        assert dict_obj.get("impuestos") is not None
        assert dict_obj.get("impuestos").get("total_impuestos_trasladados") == 360000
        assert dict_obj.get("impuestos").get("total_impuestos_retenidos") == 247500

        assert dict_obj.get("impuestos").get("retenciones") is not None
        assert len(dict_obj.get("impuestos").get("retenciones")) == 2

        retencion = dict_obj.get("impuestos").get("retenciones")[0]
        assert retencion.get("impuesto") == "001"
        assert retencion.get("importe") == 247000

        retencion = dict_obj.get("impuestos").get("retenciones")[1]
        assert retencion.get("impuesto") == "003"
        assert retencion.get("importe") == 500

        assert dict_obj.get("impuestos").get("traslados") is not None
        assert len(dict_obj.get("impuestos").get("traslados")) == 1

        traslado = dict_obj.get("impuestos").get("traslados")[0]
        assert traslado.get("impuesto") == "002"
        assert traslado.get("tipo_factor") == "Tasa"
        assert traslado.get("tasa_o_cuota") == 1.6
        assert traslado.get("importe") == 360000

        # complemento
        assert dict_obj.get("complemento") is not None
        assert dict_obj.get("complemento").get("timbre_fiscal_digital") is not None

        # cfdi_relacionados
        assert dict_obj.get("cfdi_relacionados") is not None
        assert dict_obj.get("cfdi_relacionados").get("tipo_relacion") == "02"
        assert dict_obj.get("cfdi_relacionados").get("cfdi_relacionados") is not None
        assert len(dict_obj.get("cfdi_relacionados").get("cfdi_relacionados")) == 1
        cfdi_relacionado = dict_obj.get("cfdi_relacionados").get("cfdi_relacionados")[0]
        assert cfdi_relacionado.get("uuid") == "ED1752FE-E865-4FF2-BFE1-0F552E770DC9"

        # addenda
        assert dict_obj.get("addenda") is None


def test_raw_complete_cfdi33():
    with open(f"{base_dir}/cfdi33/cfdi33.xml") as file:
        cfdi = CFDI(file)
        raw_obj = cfdi.to_raw()

        assert type(raw_obj) == dict

        assert raw_obj.get("attributes").get("Version") == "3.3"
