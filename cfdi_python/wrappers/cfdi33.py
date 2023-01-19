from dataclasses import dataclass

from cfdi_python.wrappers.nomina12 import Nomina
from cfdi_python.wrappers.timbreFiscalDigital11 import TimbreFiscalDigital
from cfdi_python.wrappers.utils import Complex


@dataclass
class Emisor:
    rfc: str  # tdCFDI:t_RFC
    regimen_fiscal: str  # catCFDI:c_RegimenFiscal
    nombre: str = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc = attrs.get("Rfc")
        self.regimen_fiscal = attrs.get("RegimenFiscal")
        self.nombre = attrs.get("Nombre")


@dataclass
class Receptor:
    rfc: str  # tdCFDI:t_RFC
    uso_cfdi: str  # catCFDI:c_UsoCFDI
    nombre: str = None
    num_reg_id_trib: str = None
    residencia_fiscal: str = None  # catCFDI:c_Pais

    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc = attrs.get("Rfc")
        self.uso_cfdi = attrs.get("UsoCFDI")
        self.nombre = attrs.get("Nombre")
        self.num_reg_id_trib = attrs.get("NumRegIdTrib")
        self.residencia_fiscal = attrs.get("ResidenciaFiscal")


@dataclass
class Complemento:
    """
    cfdi:Complemento > *

    Examples:
        In the XML:
            cfdi:Complemento
                > tfd:TimbreFiscalDigital
                > nomina12:Nomina
                > {any:any}

        As a model:
            cfdi.complemento.timbreFiscalDigital
            cfdi.complemento.nomina
            cfdi.complemento.{any}
    """

    timbre_fiscal_digital: TimbreFiscalDigital = None  # tfd:TimbreFiscalDigital
    nomina: Nomina | list[Nomina] = None  # nomina12:Nomina

    def __init__(self, data):
        if data.get("tfd:TimbreFiscalDigital"):
            self.timbre_fiscal_digital = TimbreFiscalDigital(
                data.get("tfd:TimbreFiscalDigital")
            )

        nomina = data.get("nomina12:Nomina")
        if nomina:
            if isinstance(nomina, list):  # can be more than one payroll
                nominas = []
                for n in nomina:
                    nominas.append(Nomina(n))
                self.nomina = nominas
            else:
                self.nomina = Nomina(nomina)


@dataclass
class Traslado(Complex):
    impuesto: str  # catCFDI:c_Impuesto
    tipo_factor: str  # catCFDI:c_TipoFactor
    tasa_o_cuota: float
    importe: float  # tdCFDI:t_Importe

    def __init__(self, data):
        attrs = data.get("attributes")

        self.impuesto = attrs.get("Impuesto")
        self.tipo_factor = attrs.get("TipoFactor")
        self.tasa_o_cuota = self.float_or_none(attrs.get("TasaOCuota"))
        self.importe = self.float_or_none(attrs.get("Importe"))


@dataclass
class ConceptoTaslado(Complex):
    base: float
    impuesto: str  # catCFDI:c_Impuesto
    tipo_factor: str  # catCFDI:c_TipoFactor
    tasa_o_cuota: float = None
    importe: float = None  # tdCFDI:t_Importe

    def __init__(self, data):
        attrs = data.get("attributes")

        self.base = self.float_or_none(attrs.get("Base"))
        self.impuesto = attrs.get("Impuesto")
        self.tipo_factor = attrs.get("TipoFactor")
        self.tasa_o_cuota = self.float_or_none(attrs.get("TasaOCuota"))
        self.importe = self.float_or_none(attrs.get("Importe"))


@dataclass
class Retencion(Complex):
    impuesto: str  # catCFDI:c_Impuesto
    importe: float  # tdCFDI:t_Importe

    def __init__(self, data):
        attrs = data.get("attributes")

        self.impuesto = attrs.get("Impuesto")
        self.importe = self.float_or_none(attrs.get("Importe"))


@dataclass
class RetencionConcepto(Complex):
    impuesto: str  # catCFDI:c_Impuesto
    tipo_factor: str  # catCFDI:c_TipoFactor
    tasa_o_cuota: float
    importe: float  # tdCFDI:t_Importe
    base: float

    def __init__(self, data):
        attrs = data.get("attributes")

        self.base = self.float_or_none(attrs.get("Base"))
        self.impuesto = attrs.get("Impuesto")
        self.tipo_factor = attrs.get("TipoFactor")
        self.tasa_o_cuota = self.float_or_none(attrs.get("TasaOCuota"))
        self.importe = self.float_or_none(attrs.get("Importe"))


@dataclass
class ConceptoImpuestos(Complex):
    """
    {
        cfdi:Impuestos: {
            cfdi:Traslados: {
                cfdi:Traslado: {} | []
            },
            cfdi:Retenciones {
                cfdi:Retencion: {} | []
            }
        }
    }
    """

    traslados: list[ConceptoTaslado]
    retenciones: list[Retencion]

    def __init__(self, data):
        self.traslados = self.children_as_list(
            data.get("cfdi:Traslados"),
            child="cfdi:Traslado",
            klass=ConceptoTaslado,
        )

        self.retenciones = self.children_as_list(
            data.get("cfdi:Retenciones"),
            child="cfdi:Retencion",
            klass=Retencion,
        )


@dataclass
class ConceptoCuentaPredial:
    numero: str

    def __init__(self, data):
        attrs = data.get("attributes")
        self.numero = attrs.get("Numero")


@dataclass
class ConceptoInformacionAduanera:
    numero_pedimento: str

    def __init__(self, data):
        attrs = data.get("attributes")
        self.numero_pedimento = attrs.get("NumeroPedimento")


@dataclass
class ConceptoParte(Complex):
    clave_prod_serv: str  # catCFDI:c_ClaveProdServ
    cantidad: float
    descripcion: str
    importe: float
    informacion_aduanera: list[ConceptoInformacionAduanera]
    no_identificacion: str = None
    valor_unitario: float = None  # tdCFDI:t_Importe
    unidad: str = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave_prod_serv = attrs.get("ClaveProdServ")
        self.no_identificacion = attrs.get("NoIdentificacion")
        self.cantidad = self.float_or_none(attrs.get("Cantidad"))
        self.descripcion = attrs.get("Descripcion")
        self.unidad = attrs.get("Unidad")
        self.valor_unitario = self.float_or_none(attrs.get("ValorUnitario"))
        self.importe = self.float_or_none(attrs.get("Importe"))

        children = self.get_first_child(data.get("children"))
        self.informacion_aduanera = self.children_as_list(
            children,
            child="cfdi:InformacionAduanera",
            klass=ConceptoInformacionAduanera,
        )


@dataclass
class Concepto(Complex):
    clave_prod_serv: str  # catCFDI:c_ClaveProdServ
    cantidad: float
    descripcion: str
    valor_unitario: float  # tdCFDI:t_Importe
    importe: float  # tdCFDI:t_Importe

    descuento: float = None  # tdCFDI:t_Importe
    unidad: str = None  # catCFDI:c_ClaveUnidad
    no_identificacion: str = None
    impuestos: ConceptoImpuestos = None
    complemento_concepto: dict | str = None  # todo: need more testing
    cuenta_predial: ConceptoCuentaPredial = None
    informacion_aduanera: list[ConceptoInformacionAduanera] = None
    parte: list[ConceptoParte] = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave_prod_serv = attrs.get("ClaveProdServ")
        self.cantidad = self.float_or_none(attrs.get("Cantidad"))
        self.clave_unidad = attrs.get("ClaveUnidad")
        self.descripcion = attrs.get("Descripcion")
        self.valor_unitario = self.float_or_none(attrs.get("ValorUnitario"))
        self.importe = self.float_or_none(attrs.get("Importe"))
        self.no_identificacion = attrs.get("NoIdentificacion")
        self.unidad = attrs.get("Unidad")
        self.descuento = self.float_or_none(attrs.get("Descuento"))

        if len(data.get("children", [])) > 0:
            children = self.get_first_child(data.get("children"))

            if children.get("cfdi:Impuestos"):
                self.impuestos = ConceptoImpuestos(children.get("cfdi:Impuestos"))

            self.complemento_concepto = children.get("cfdi:ComplementoConcepto")

            if children.get("cfdi:CuentaPredial"):
                self.cuenta_predial = ConceptoCuentaPredial(
                    children.get("cfdi:CuentaPredial")
                )

            self.informacion_aduanera = self.children_as_list(
                children,
                child="cfdi:InformacionAduanera",
                klass=ConceptoInformacionAduanera,
            )

            self.parte = self.children_as_list(
                children, child="cfdi:Parte", klass=ConceptoParte
            )


@dataclass
class Impuestos(Complex):
    total_impuestos_trasladados: float = None  # tdCFDI:t_Importe
    total_impuestos_retenidos: float = None  # tdCFDI:t_Importe
    traslados: list[Traslado] = None
    retenciones: list[Retencion] = None

    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_impuestos_trasladados = self.float_or_none(
            attrs.get("TotalImpuestosTrasladados")
        )
        self.total_impuestos_retenidos = self.float_or_none(
            attrs.get("TotalImpuestosRetenidos")
        )

        # getting children
        children = self.get_first_child(data.get("children"))

        self.retenciones = self.children_as_list(
            children.get("cfdi:Retenciones"),
            child="cfdi:Retencion",
            klass=Retencion,
        )

        self.traslados = self.children_as_list(
            children.get("cfdi:Traslados"),
            child="cfdi:Traslado",
            klass=Traslado,
        )


@dataclass
class CfdiRelacionado:
    uuid: str

    def __init__(self, data):
        attrs = data.get("attributes")
        self.uuid = attrs.get("UUID")


@dataclass
class CfdiRelacionados(Complex):
    tipo_relacion: str  # catCFDI:c_TipoRelacion
    cfdi_relacionado: list[CfdiRelacionado]

    def __init__(self, data):
        attrs = data.get("attributes")

        self.tipo_relacion = attrs.get("TipoRelacion")

        # children
        children = self.get_first_child(data.get("children"))
        self.cfdi_relacionados = self.children_as_list(
            children, child="cfdi:CfdiRelacionado", klass=CfdiRelacionado
        )


@dataclass
class CFDI(Complex):
    """
    CFDI V3.3
    http://www.sat.gob.mx/cfd/3
    """

    supported_versions = ["3.3"]
    schema_location: str
    fecha: str  # tdCFDI:t_FechaH
    sello: str
    no_certificado: str
    certificado: str
    sub_total: float  # tdCFDI:t_Importe
    moneda: str  # catCFDI:c_Moneda
    total: float  # tdCFDI:t_Importe
    tipo_de_comprobante: str  # catCFDI:c_TipoDeComprobante
    lugar_expedicion: str  # catCFDI:c_CodigoPostal
    emisor: Emisor
    receptor: Receptor
    conceptos: list[Concepto]

    serie: str = None
    folio: str = None
    forma_pago: str = None  # catCFDI:c_FormaPago
    condiciones_de_pago: str = None
    descuento: float = None  # tdCFDI:t_Importe
    tipo_cambio: float = None
    metodo_pago: str = None  # catCFDI:c_MetodoPago
    confirmacion: str = None
    version: str = "3.3"
    impuestos: Impuestos = None
    addenda: dict | str = None
    cfdi_relacionados: list[CfdiRelacionados] = None
    complemento: Complemento = None

    def __init__(self, raw_data):
        attrs = raw_data.get("attributes")

        self.schema_location = attrs.get("xsi:schemaLocation")
        self.version = attrs.get("Version")

        self.check_version()

        self.serie = attrs.get("Serie")
        self.folio = attrs.get("Folio")
        self.fecha = attrs.get("Fecha")
        self.sello = attrs.get("Sello")
        self.forma_pago = attrs.get("FormaPago")
        self.no_certificado = attrs.get("NoCertificado")
        self.certificado = attrs.get("Certificado")
        self.sub_total = self.float_or_none(attrs.get("SubTotal"))
        self.moneda = attrs.get("Moneda")
        self.total = self.float_or_none(attrs.get("Total"))
        self.tipo_de_comprobante = attrs.get("TipoDeComprobante")
        self.metodo_pago = attrs.get("MetodoPago")
        self.lugar_expedicion = attrs.get("LugarExpedicion")
        self.condiciones_de_pago = attrs.get("CondicionesDePago")
        self.descuento = self.float_or_none(attrs.get("Descuento"))
        self.tipo_cambio = self.float_or_none(attrs.get("TipoCambio"))
        self.confirmacion = attrs.get("Confirmacion")

        # getting children
        children = self.get_first_child(raw_data.get("children"))

        self.emisor = Emisor(children.get("cfdi:Emisor"))
        self.receptor = Receptor(children.get("cfdi:Receptor"))

        # getting conceptos
        self.conceptos = self.children_as_list(
            children.get("cfdi:Conceptos"),
            child="cfdi:Concepto",
            klass=Concepto,
        )

        if children.get("cfdi:Impuestos"):
            self.impuestos = Impuestos(children.get("cfdi:Impuestos"))

        # getting all complementos
        if children.get("cfdi:Complemento"):
            self.complemento = Complemento(children.get("cfdi:Complemento"))

        self.cfdi_relacionados = self.children_as_list(
            children, child="cfdi:CfdiRelacionados", klass=CfdiRelacionados
        )

        # it might require extra location configuration
        self.addenda = children.get("cfdi:Addenda", None)

    def check_version(self):
        if self.version not in self.supported_versions:
            raise Exception(f"Version {self.version} not supported")
