from dataclasses import dataclass


@dataclass
class Origen:
    id_origen: str = None
    rfc_remitente: str = None  # tdCFDI:t_RFC
    nombre_remitente: str = None
    num_reg_id_trib: str = None
    residencia_fiscal: str = None  # catCFDI:c_Pais
    num_estacion: str = None  # catCartaPorte:c_Estaciones
    nombre_estacion: str = None
    navegacion_trafico: str = None
    fecha_hora_salida: str = None  # tdCFDI:t_FechaH


@dataclass
class Destino:
    fecha_hora_prog_llegada: str  # tdCFDI:t_FechaH"
    id_destino: str = None
    rfc_destinatario: str = None  # tdCFDI:t_RFC"
    nombre_destinatario: str = None
    num_reg_id_trib: str = None
    residencia_fiscal: str = None  # catCFDI:c_Pais"
    num_estacion: str = None  # catCartaPorte:c_Estaciones"
    nombre_estacion: str = None
    navegacion_trafico: str = None


@dataclass
class Domicilio:
    calle: str  # tdCFDI:t_Descrip100
    estado: str
    pais: str  # type="catCFDI:c_Pais
    codigo_postal: str
    numero_exterior: str = None  # tdCFDI:t_NumeroDomicilio
    numero_interior: str = None  # tdCFDI:t_NumeroDomicilio
    colonia: str = None  # tdCFDI:t_Descrip120
    localidad: str = None  # tdCFDI:t_Descrip120
    referencia: str = None  # tdCFDI:t_Referencia
    municipio: str = None  # tdCFDI:t_Descrip120


@dataclass
class Ubicacion:
    tipo_estacion: str = None  # catCartaPorte:c_TipoEstacion
    distancia_recorrida: float = None

    origen: Origen = None
    destino: Destino = None
    domicilio: Domicilio = None


@dataclass
class CantidadTransporta:
    Cantidad: str
    IDOrigen: str
    IDDestino: str
    CvesTransporte: str = None  # catCartaPorte:c_CveTransporte


@dataclass
class DetalleMercancia:
    UnidadPeso: str  # catCartaPorte:c_ClaveUnidadPeso
    PesoBruto: str
    PesoNeto: str
    PesoTara: str
    NumPiezas: str = None


@dataclass
class Mercancia:
    PesoEnKg: int

    cantidadTransporta: CantidadTransporta = None
    detalleMercancia: DetalleMercancia = None

    BienesTransp: str = None  # catCartaPorte:c_ClaveProdServCP
    ClaveSTCC: str = None  # catCartaPorte:c_ClaveProdSTCC
    Descripcion: str = None
    Cantidad: str = None
    ClaveUnidad: str = None  # catCFDI:c_ClaveUnidad
    Unidad: str = None
    Dimensiones: str = None
    MaterialPeligroso: str = None
    CveMaterialPeligroso: str = None  # catCartaPorte:c_MaterialPeligroso
    Embalaje: str = None  # catCartaPorte:c_TipoEmbalaje
    DescripEmbalaje: str = None
    ValorMercancia: str = None  # tdCFDI:t_Importe
    Moneda: str = None  # catCFDI:c_Moneda
    FraccionArancelaria: str = None  # catComExt:c_FraccionArancelaria
    UUIDComercioExt: str = None


@dataclass
class CartaPorte:
    version: str
    transp_internac: str
    ubicaciones: list[Ubicacion]
    mercancias: list[Mercancia]

    entrada_salida_merc: str = None
    via_entrada_salida: str = None  # catCartaPorte:c_CveTransporte
    total_dist_rec: float = None
