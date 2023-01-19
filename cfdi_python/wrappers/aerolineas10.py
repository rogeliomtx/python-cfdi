from dataclasses import dataclass


@dataclass
class Cargo:
    codigo_cargo: str
    importe: str  # aerolineas:t_Importe


@dataclass
class Aerolineas:
    total_cargos: float  # aerolineas:t_Importe
    version: str
    tua: float  # aerolineas:t_Importe
    cargos: list[Cargo]
