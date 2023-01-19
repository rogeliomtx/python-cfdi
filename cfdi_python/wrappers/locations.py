import os

from .xsds import xsd_dir

# ==========================================
# Timbre fiscal digital
# ==========================================
timbre_fiscal_digital10 = (
    "http://www.sat.gob.mx/TimbreFiscalDigital",
    os.path.join(xsd_dir, "timbreFiscalDigital10.xsd"),
)

timbre_fiscal_digital11 = (
    "http://www.sat.gob.mx/TimbreFiscalDigital",
    os.path.join(xsd_dir, "timbreFiscalDigital11.xsd"),
)

# ==========================================
# Recibo de pago de nómina
# ==========================================
nomina11 = (
    "http://www.sat.gob.mx/nomina",
    os.path.join(xsd_dir, "nomina11.xsd"),
)

nomina12b = (
    "http://www.sat.gob.mx/nomina12",
    os.path.join(xsd_dir, "nomina12b.xsd"),
)


# ==========================================
# Pagos
# ==========================================
pagos10 = (
    "http://www.sat.gob.mx/Pagos",
    os.path.join(xsd_dir, "pagos10.xsd"),
)

pagos20 = (
    "http://www.sat.gob.mx/Pagos20",
    os.path.join(xsd_dir, "pagos20.xsd"),
)
