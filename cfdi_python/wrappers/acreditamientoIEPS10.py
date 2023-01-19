from dataclasses import dataclass


@dataclass
class AcreditamientoIEPS10:
    """
    targetNamespace: "http://www.sat.gob.mx/acreditamiento"

    Args:
        version (str): Atributo requerido que indica la versión del complemento
         concepto.
        tar (str): Atributo requerido para expresar la clave de la Terminal de
            Almacenamiento y Reparto (CVE TAR), conforme al catálogo publicado
            en la página de Internet del SAT, mismo que servirá para
            identificar la cuota por litro conforme a las tablas que publique
            la Secretaría de Hacienda y Crédito Público para determinar el
            monto del estímulo fiscal.
    """

    tar: str  # aieps:c_TAR
    version: str = "1.0"

    def __init__(self, raw_data):
        attrs = raw_data.get("attributes")

        self.tar = attrs.get("TAR")
        self.version = attrs.get("Version")
