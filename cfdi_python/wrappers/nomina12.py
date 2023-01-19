from dataclasses import dataclass

from cfdi_python.wrappers.utils import Complex


@dataclass
class SubContratacion(Complex):
    rfc_labora: str  # tdCFDI:t_RFC
    porcentaje_tiempo: float

    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc_labora = attrs.get("RfcLabora")
        self.porcentaje_tiempo = self.float_or_none(attrs.get("PorcentajeTiempo"))


@dataclass
class Receptor(Complex):
    curp: str  # tdCFDI:t_CURP
    tipo_contrato: str  # catNomina:c_TipoContrato
    tipo_regimen: str  # catNomina:c_TipoRegimen
    num_empleado: str
    periodicidad_pago: str  # catNomina:c_PeriodicidadPago
    clave_ent_fed: str  # catCFDI:c_Estado
    sub_contratacion: list[SubContratacion]

    num_seguridad_social: str = None
    fecha_inicio_rel_laboral: str = None  # tdCFDI:t_Fecha
    antiguedad: str = None
    sindicalizado: str = None
    tipo_jornada: str = None  # catNomina:c_TipoJornada
    departamento: str = None
    puesto: str = None
    riesgo_puesto: str = None  # catNomina:c_RiesgoPuesto
    banco: str = None  # catNomina:c_Banco
    cuenta_bancaria: str = None  # tdCFDI:t_CuentaBancaria
    salario_base_cot_apor: float = None  # tdCFDI:t_ImporteMXN
    salario_diario_integrado: float = None  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.curp = attrs.get("Curp")
        self.num_seguridad_social = attrs.get("NumSeguridadSocial")
        self.fecha_inicio_rel_laboral = attrs.get("FechaInicioRelLaboral")
        self.antiguedad = attrs.get("Antigüedad")
        self.tipo_contrato = attrs.get("TipoContrato")
        self.sindicalizado = attrs.get("Sindicalizado")
        self.tipo_jornada = attrs.get("TipoJornada")
        self.tipo_regimen = attrs.get("TipoRegimen")
        self.num_empleado = attrs.get("NumEmpleado")
        self.departamento = attrs.get("Departamento")
        self.puesto = attrs.get("Puesto")
        self.riesgo_puesto = attrs.get("RiesgoPuesto")
        self.periodicidad_pago = attrs.get("PeriodicidadPago")
        self.banco = attrs.get("Banco")
        self.cuenta_bancaria = attrs.get("CuentaBancaria")
        self.salario_base_cot_apor = self.float_or_none(attrs.get("SalarioBaseCotApor"))
        self.salario_diario_integrado = self.float_or_none(
            attrs.get("SalarioDiarioIntegrado")
        )
        self.clave_ent_fed = attrs.get("ClaveEntFed")

        children = self.get_first_child(data.get("children"))
        self.sub_contratacion = self.children_as_list(
            children, child="nomina12:SubContratacion", klass=SubContratacion
        )


@dataclass
class EntidadSNCF(Complex):
    origen_recurso: str  # catNomina:c_OrigenRecurso
    monto_recurso_propio: float = None  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.origen_recurso = attrs.get("OrigenRecurso")
        self.monto_recurso_propio = self.float_or_none(attrs.get("MontoRecursoPropio"))


@dataclass
class Emisor(Complex):
    registro_patronal: str = None
    curp: str = None  # tdCFDI:t_CURP
    rfc_patron_origen: str = None  # tdCFDI:t_RFC

    entidad_SNCF: EntidadSNCF = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.registro_patronal = attrs.get("RegistroPatronal")
        self.curp = attrs.get("Curp")
        self.rfc_patron_origen = attrs.get("RfcPatronOrigen")

        children = self.get_first_child(data.get("children"))
        if children.get("nomina12:EntidadSNCF"):
            self.entidad_SNCF = EntidadSNCF(children.get("nomina12:EntidadSNCF"))


@dataclass
class AccionesOTitulos(Complex):
    valor_mercado: float
    precio_al_otorgarse: float

    def __init__(self, data):
        attrs = data.get("attributes")

        self.valor_mercado = self.float_or_none(attrs.get("ValorMercado"))
        self.precio_al_otorgarse = self.float_or_none(attrs.get("PrecioAlOtorgarse"))


@dataclass
class HorasExtra(Complex):
    dias: int
    tipo_horas: str  # catNomina:c_TipoHoras
    horas_extra: int
    importe_pagado: float  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.dias = self.int_or_none(attrs.get("Dias"))
        self.tipo_horas = attrs.get("TipoHoras")
        self.horas_extra = self.int_or_none(attrs.get("HorasExtra"))
        self.importe_pagado = self.float_or_none(attrs.get("ImportePagado"))


@dataclass
class Percepcion(Complex):
    clave: str
    concepto: str
    importe_exento: float  # tdCFDI:t_ImporteMXN
    importe_gravado: float  # tdCFDI:t_ImporteMXN
    tipo_percepcion: str  # catNomina:c_TipoPercepcion
    horas_extra: list[HorasExtra] = None
    acciones_o_titulos: list[AccionesOTitulos] = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe_exento = self.float_or_none(attrs.get("ImporteExento"))
        self.importe_gravado = self.float_or_none(attrs.get("ImporteGravado"))
        self.tipo_percepcion = attrs.get("TipoPercepcion")

        children = self.get_first_child(data.get("children"))
        self.acciones_o_titulos = self.children_as_list(
            children, child="nomina12:AccionesOTitulos", klass=AccionesOTitulos
        )
        self.horas_extra = self.children_as_list(
            children, child="nomina12:HorasExtra", klass=HorasExtra
        )


@dataclass
class JubilacionPensionRetiro(Complex):
    ingreso_acumulable: float  # tdCFDI:t_ImporteMXN
    ingreso_no_acumulable: float  # tdCFDI:t_ImporteMXN
    total_una_exhibicion: float = None  # tdCFDI:t_ImporteMXN
    total_parcialidad: float = None  # tdCFDI:t_ImporteMXN
    monto_diario: float = None  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_una_exhibicion = self.float_or_none(attrs.get("TotalUnaExhibicion"))
        self.ingreso_acumulable = self.float_or_none(attrs.get("IngresoAcumulable"))
        self.ingreso_no_acumulable = self.float_or_none(attrs.get("IngresoNoAcumulable"))
        self.total_parcialidad = self.float_or_none(attrs.get("TotalParcialidad"))
        self.monto_diario = self.float_or_none(attrs.get("MontoDiario"))


@dataclass
class Deduccion(Complex):
    clave: str
    concepto: str
    importe: float  # tdCFDI:t_ImporteMXN
    tipo_deduccion: str  # catNomina:c_TipoDeduccion

    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe = self.float_or_none(attrs.get("Importe"))
        self.tipo_deduccion = attrs.get("TipoDeduccion")


@dataclass
class Deducciones(Complex):
    deducciones: list[Deduccion]
    total_impuestos_retenidos: float = None  # tdCFDI:t_ImporteMXN
    total_otras_deducciones: float = None  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_impuestos_retenidos = self.float_or_none(
            attrs.get("TotalImpuestosRetenidos")
        )
        self.total_otras_deducciones = self.float_or_none(
            attrs.get("TotalOtrasDeducciones")
        )

        children = self.get_first_child(data.get("children"))
        self.deducciones = self.children_as_list(
            children, child="nomina12:Deduccion", klass=Deduccion
        )


@dataclass
class SeparacionIndemnizacion(Complex):
    total_pagado: float  # tdCFDI:t_ImporteMXN
    num_axos_servicio: int
    ultimo_sueldo_mens_ord: float  # tdCFDI:t_ImporteMXN
    ingreso_acumulable: float  # tdCFDI:t_ImporteMXN
    ingreso_no_acumulable: float  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_pagado = self.float_or_none(attrs.get("TotalPagado"))
        self.num_axos_servicio = self.int_or_none(attrs.get("NumAñosServicio"))
        self.ultimo_sueldo_mens_ord = self.float_or_none(attrs.get("UltimoSueldoMensOrd"))
        self.ingreso_acumulable = self.float_or_none(attrs.get("IngresoAcumulable"))
        self.ingreso_no_acumulable = self.float_or_none(attrs.get("IngresoNoAcumulable"))


@dataclass
class Percepciones(Complex):
    total_exento: float  # tdCFDI:t_ImporteMXN
    total_gravado: float  # tdCFDI:t_ImporteMXN

    percepciones: list[Percepcion]
    jubilacion_pension_retiro: JubilacionPensionRetiro = None
    separacion_indemnizacion: SeparacionIndemnizacion = None

    total_sueldos: float = None  # tdCFDI:t_ImporteMXN
    total_separacion_indemnizacion: float = None  # tdCFDI:t_ImporteMXN
    total_jubilacion_pension_retiro: float = None  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_exento = self.float_or_none(attrs.get("TotalExento"))
        self.total_gravado = self.float_or_none(attrs.get("TotalGravado"))
        self.total_jubilacion_pension_retiro = self.float_or_none(
            attrs.get("TotalJubilacionPensionRetiro")
        )
        self.total_sueldos = self.float_or_none(attrs.get("TotalSueldos"))
        self.total_separacion_indemnizacion = self.float_or_none(
            attrs.get("TotalSeparacionIndemnizacion")
        )

        # percepciones
        children = self.get_first_child(data.get("children"))
        self.percepciones = self.children_as_list(
            children, child="nomina12:Percepcion", klass=Percepcion
        )

        # jubilacionPensionRetiro
        if children.get("nomina12:JubilacionPensionRetiro"):
            self.jubilacion_pension_retiro = JubilacionPensionRetiro(
                children.get("nomina12:JubilacionPensionRetiro")
            )

        # separacionIndemnizacion
        if children.get("nomina12:SeparacionIndemnizacion"):
            self.separacion_indemnizacion = SeparacionIndemnizacion(
                children.get("nomina12:SeparacionIndemnizacion")
            )


@dataclass
class SubsidioAlEmpleo(Complex):
    subsidio_causado: float  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.subsidio_causado = self.float_or_none(attrs.get("SubsidioCausado"))


@dataclass
class CompensacionSaldosAFavor(Complex):
    saldo_a_favor: float
    axo: int
    remanente_saldo_favor: float

    def __init__(self, data):
        attrs = data.get("attributes")

        self.saldo_a_favor = self.float_or_none(attrs.get("SaldoAFavor"))
        self.axo = self.int_or_none(attrs.get("Año"))
        self.remanente_sal_fav = self.float_or_none(attrs.get("RemanenteSalFav"))


@dataclass
class OtroPago(Complex):
    tipo_otro_pago: str  # catNomina:c_TipoOtroPago
    clave: str
    concepto: str
    importe: float  # tdCFDI:t_ImporteMXN
    subsidio_al_empleo: SubsidioAlEmpleo = None
    compensacion_saldos_a_favor: CompensacionSaldosAFavor = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.tipo_otro_pago = attrs.get("TipoOtroPago")
        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe = self.float_or_none(attrs.get("Importe"))

        children = self.get_first_child(data.get("children"))
        if children.get("nomina12:SubsidioAlEmpleo"):
            self.subsidio_al_empleo = SubsidioAlEmpleo(
                children.get("nomina12:SubsidioAlEmpleo")
            )

        if children.get("nomina12:CompensacionSaldosAFavor"):
            self.compensacion_saldos_a_favor = CompensacionSaldosAFavor(
                children.get("nomina12:CompensacionSaldosAFavor")
            )


@dataclass
class Incapacidad(Complex):
    dias_incapacidad: int
    tipo_incapacidad: str  # catNomina:c_TipoIncapacidad
    importe_monetario: float = None  # tdCFDI:t_ImporteMXN

    def __init__(self, data):
        attrs = data.get("attributes")

        self.dias_incapacidad = self.int_or_none(attrs.get("DiasIncapacidad"))
        self.tipo_incapacidad = attrs.get("TipoIncapacidad")
        self.importe_monetario = self.float_or_none(attrs.get("ImporteMonetario"))


@dataclass
class Nomina(Complex):
    tipo_nomina: str  # catNomina:c_TipoNomina
    fecha_pago: str  # tdCFDI:t_Fecha
    fecha_inicial_pago: str  # tdCFDI:t_Fecha
    fecha_final_pago: str  # tdCFDI:t_Fecha
    num_dias_pagados: float
    receptor: Receptor

    verison: str = "1.2"
    emisor: Emisor = None
    percepciones: Percepciones = None
    deducciones: Deducciones = None
    otros_pagos: list[OtroPago] = None
    incapaicidades: list[Incapacidad] = None
    total_percepciones: float = None  # tdCFDI:t_ImporteMXN
    total_deducciones: float = None  # tdCFDI:t_ImporteMXN
    total_otros_pagos: float = None  # tdCFDI:t_ImporteMXN

    supported_versions = ["1.2"]

    def __init__(self, raw_data):
        attrs = raw_data.get("attributes")

        self.version = attrs.get("Version")

        self.check_version()

        self.tipo_nomina = attrs.get("TipoNomina")

        self.fecha_pago = attrs.get("FechaPago")
        self.fecha_final_pago = attrs.get("FechaFinalPago")
        self.fecha_inicial_pago = attrs.get("FechaInicialPago")

        self.num_dias_pagados = self.float_or_none(attrs.get("NumDiasPagados"))
        self.total_percepciones = self.float_or_none(attrs.get("TotalPercepciones"))
        self.total_deducciones = self.float_or_none(attrs.get("TotalDeducciones"))
        self.total_otros_pagos = self.float_or_none(attrs.get("TotalOtrosPagos"))

        # getting children
        children = self.get_first_child(raw_data.get("children"))

        self.receptor = Receptor(children.get("nomina12:Receptor"))

        if children.get("nomina12:Emisor"):
            self.emisor = Emisor(children.get("nomina12:Emisor"))

        if children.get("nomina12:Percepciones"):
            self.percepciones = Percepciones(children.get("nomina12:Percepciones"))

        if children.get("nomina12:Deducciones"):
            self.deducciones = Deducciones(children.get("nomina12:Deducciones"))

        self.otros_pagos = self.children_as_list(
            children.get("nomina12:OtrosPagos"),
            child="nomina12:OtroPago",
            klass=OtroPago,
        )

        self.incapacidades = self.children_as_list(
            children.get("nomina12:Incapacidades"),
            child="nomina12:Incapacidad",
            klass=Incapacidad,
        )

    def check_version(self):
        if self.version not in self.supported_versions:
            raise Exception(f"Version {self.version} not supported")
