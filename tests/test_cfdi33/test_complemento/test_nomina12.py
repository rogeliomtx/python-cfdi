from cfdi_python import CFDI
from tests.assets import base_dir
from cfdi_python.wrappers.schemas import get_context
from cfdi_python.wrappers.locations import nomina12b


def test_complete_nomina12():
    context = get_context()
    context["locations"] += [nomina12b]

    with open(f"{base_dir}/cfdi33/complemento/nomina12.xml") as file:
        cfdi = CFDI(file, context=context)
        model = cfdi.to_model()

        assert model.version == "3.3"

        # complemento
        assert model.complemento is not None
        assert model.complemento.nomina is not None
        assert model.complemento.timbre_fiscal_digital is not None

        # nomina
        nomina = model.complemento.nomina
        assert nomina.version == "1.2"

        assert nomina.tipo_nomina == "O"
        assert nomina.fecha_pago == "2016-10-15"
        assert nomina.fecha_final_pago == "2016-10-15"
        assert nomina.fecha_inicial_pago == "2016-10-01"
        assert nomina.num_dias_pagados == 15
        assert nomina.total_percepciones == 123.45
        assert nomina.total_deducciones == 123.45
        assert nomina.total_otros_pagos == 123.45

        # emisor
        assert nomina.emisor is not None
        assert nomina.emisor.registro_patronal == "E23-12345-12-1"
        assert nomina.emisor.curp == "OAAJ840102HJCVRN00"
        assert nomina.emisor.rfc_patron_origen == "AAA010101AAA"

        assert nomina.emisor.entidad_SNCF is not None
        assert nomina.emisor.entidad_SNCF.origen_recurso == "IP"
        assert nomina.emisor.entidad_SNCF.monto_recurso_propio == 123.45

        # receptor
        assert nomina.receptor is not None
        assert nomina.receptor.curp == "OAAJ840102HJCVRN00"
        assert nomina.receptor.num_seguridad_social == "123456789012345"
        assert nomina.receptor.fecha_inicio_rel_laboral == "2013-04-11"
        assert nomina.receptor.antiguedad == "P3Y2M23D"
        assert nomina.receptor.tipo_contrato == "01"
        assert nomina.receptor.sindicalizado == "Sí"
        assert nomina.receptor.tipo_jornada == "02"
        assert nomina.receptor.tipo_regimen == "03"
        assert nomina.receptor.num_empleado == "001"
        assert nomina.receptor.departamento == "001"
        assert nomina.receptor.puesto == "Programador"
        assert nomina.receptor.riesgo_puesto == "3"
        assert nomina.receptor.periodicidad_pago == "04"
        assert nomina.receptor.banco == "002"
        assert nomina.receptor.cuenta_bancaria == "1234567890"
        assert nomina.receptor.salario_base_cot_apor == 123.45
        assert nomina.receptor.salario_diario_integrado == 123.45
        assert nomina.receptor.clave_ent_fed == "AGU"

        # receptor.sub_contratacion
        assert nomina.receptor.sub_contratacion is not None
        assert len(nomina.receptor.sub_contratacion) == 2

        sub_contratacion = nomina.receptor.sub_contratacion[0]
        assert sub_contratacion.rfc_labora == "AAA010101AAA"
        assert sub_contratacion.porcentaje_tiempo == 23.45

        sub_contratacion = nomina.receptor.sub_contratacion[1]
        assert sub_contratacion.rfc_labora == "BBB010101AAA"
        assert sub_contratacion.porcentaje_tiempo == 13.45

        # percepciones
        assert nomina.percepciones is not None
        assert nomina.percepciones.total_exento == 123.45
        assert nomina.percepciones.total_gravado == 123.45
        assert nomina.percepciones.total_jubilacion_pension_retiro == 123.45
        assert nomina.percepciones.total_sueldos == 123.45

        # percepciones.jubilacion_pension_retiro
        assert nomina.percepciones.jubilacion_pension_retiro is not None
        jpr = nomina.percepciones.jubilacion_pension_retiro
        assert jpr.total_una_exhibicion == 223.45
        assert jpr.ingreso_acumulable == 223.45
        assert jpr.ingreso_no_acumulable == 223.45

        # percepciones.separacion_indemnizacion
        assert nomina.percepciones.separacion_indemnizacion is not None
        separacion_indemnizacion = nomina.percepciones.separacion_indemnizacion
        assert separacion_indemnizacion.total_pagado == 323.45
        assert separacion_indemnizacion.num_axos_servicio == 7
        assert separacion_indemnizacion.ultimo_sueldo_mens_ord == 323.45
        assert separacion_indemnizacion.ingreso_acumulable == 323.45
        assert separacion_indemnizacion.ingreso_no_acumulable == 323.45

        # percepciones.percepciones
        assert nomina.percepciones.percepciones is not None
        assert len(nomina.percepciones.percepciones) == 2

        percepcion = nomina.percepciones.percepciones[0]
        assert percepcion.clave == "AAA"
        assert percepcion.concepto == "Sueldo Regular"
        assert percepcion.importe_exento == 90
        assert percepcion.importe_gravado == 89
        assert percepcion.tipo_percepcion == "001"

        # percepciones.percepciones.acciones_o_titulos
        assert percepcion.acciones_o_titulos is not None
        assert percepcion.acciones_o_titulos.valor_mercado == 12345.67
        assert percepcion.acciones_o_titulos.precio_al_otorgarse == 123.45

        # percepciones.percepciones.horas_extra
        assert percepcion.horas_extra is not None
        assert len(percepcion.horas_extra) == 2

        assert percepcion.horas_extra[0].dias == 2
        assert percepcion.horas_extra[0].tipo_horas == "01"
        assert percepcion.horas_extra[0].horas_extra == 8
        assert percepcion.horas_extra[0].importe_pagado == 228.45

        assert percepcion.horas_extra[1].dias == 2
        assert percepcion.horas_extra[1].tipo_horas == "02"
        assert percepcion.horas_extra[1].horas_extra == 8
        assert percepcion.horas_extra[1].importe_pagado == 228.45

        # deducciones
        assert nomina.deducciones is not None
        assert nomina.deducciones.total_impuestos_retenidos == 123.45
        assert nomina.deducciones.total_otras_deducciones == 123.45

        # deducciones.deducciones
        assert nomina.deducciones.deducciones is not None
        assert len(nomina.deducciones.deducciones) == 2

        assert nomina.deducciones.deducciones[0].clave == "XXX"
        assert nomina.deducciones.deducciones[0].concepto == "Deduccion Semanal"
        assert nomina.deducciones.deducciones[0].importe == 10
        assert nomina.deducciones.deducciones[0].tipo_deduccion == "001"

        assert nomina.deducciones.deducciones[1].clave == "YYY"
        assert nomina.deducciones.deducciones[1].concepto == "Deduccion Semanal"
        assert nomina.deducciones.deducciones[1].importe == 10
        assert nomina.deducciones.deducciones[1].tipo_deduccion == "100"

        # otros_pagos
        assert nomina.otros_pagos is not None
        assert len(nomina.otros_pagos) == 2

        assert nomina.otros_pagos[0].tipo_otro_pago == "001"
        assert nomina.otros_pagos[0].clave == "003"
        assert nomina.otros_pagos[0].concepto == "Otro pago 111"
        assert nomina.otros_pagos[0].importe == 1234.56

        # otros_pagos.subsidio_al_empleo
        assert nomina.otros_pagos[0].subsidio_al_empleo is not None
        subsidio_al_empleo = nomina.otros_pagos[0].subsidio_al_empleo
        assert subsidio_al_empleo.subsidio_causado == 1234.56

        # otros_pagos.compensacion_saldos_a_favor
        assert nomina.otros_pagos[0].compensacion_saldos_a_favor is not None
        saf = nomina.otros_pagos[0].compensacion_saldos_a_favor
        assert saf.saldo_a_favor == 12345.67
        assert saf.axo == 2016
        assert saf.remanente_sal_fav == 1234.56

        # incapacidades
        assert nomina.incapacidades is not None
        assert len(nomina.incapacidades) == 2

        assert nomina.incapacidades[0].dias_incapacidad == 1
        assert nomina.incapacidades[0].tipo_incapacidad == "01"
        assert nomina.incapacidades[0].importe_monetario == 22.45

        assert nomina.incapacidades[1].dias_incapacidad == 2
        assert nomina.incapacidades[1].tipo_incapacidad == "02"
        assert nomina.incapacidades[1].importe_monetario == 22.45
