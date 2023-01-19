# CFDI a JSON (`json_cfdi`)

## Empezando

Desde PYPI
```
❯ pipenv install json_cfdi
```

Desde el código fuente
```
❯  git clone https://gitlab.com/workyhr/json_cfdi
❯  cd json_cfdi
❯  python3 setup.py install
```

## Testing <small>(Instalar y lanzar ambiente)</small>

```sh
# instalar virtualenv
❯ python -m pip install virtualenv

# crear ambiente
❯ virtualenv .env

# activar ambiente
❯ source .env/bin/activate

# instalar requerimientos
❯ python -m pip install -r requirements.txt

# levantar
❯ cd json_cfdi

# lanzar tests
❯ pytest tests/
```
## Descripción

Una forma consistente dev-friendly de procesar archivos xml y consultarlos en 
modelos python manejables y consistentes.
- Sin validaciones.
- Sin descarga adicional de catálogos del SAT (lo cual lo hace muy lento).
- Rápido.
- Fácil de usar.


Basado en la lista de CFDI y complementos del sat:
* CFDI `3.3` y `4.0` http://omawww.sat.gob.mx/tramitesyservicios/Paginas/anexo_20_version3-3.htm
* complementos: http://omawww.sat.gob.mx/factura/Paginas/emite_complementosdefactura.htm

Se hicieron tests haciendo uso de estos recursos, muchas gracias :)
* https://www.cryptosys.net/firmasat/cfdv40-examples.html
* https://www.cryptosys.net/firmasat/cfdv33-examples.html

## Versiones de CFDI
- CFDI
  - `3.3` http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd
  - `4.0` http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd

## Uso
### Instalación
```sh
pip install json_cfdi
```

### Uso

#### `cfdi.to_model()`
Util para procesar los xmls como objetos python.
```python
from json_cfdi import CFDI

with open("nomina-john.xml") as file:
    cfdi = CFDI(file)
    model = cfdi.to_model()  # acceder al contenido en forma de objeto python
    model.version  # '4.0'
    model.receptor.nombre  # John Doe    
    model.emisor.nombre  # Company SA de CV
```

#### `cfdi.to_json()`
```python
from json_cfdi import CFDI

with open("nomina-john.xml") as file:
    cfdi = CFDI(file)
    json_obj = cfdi.to_json()  # acceder al contenido en forma de objeto python
    type(json_obj)  # <str>
```

#### `cfdi.to_dict()`
Espacialmente útil para microservicios.
```python
from json_cfdi import CFDI

with open("nomina-john.xml") as file:
    cfdi = CFDI(file)
    dict_obj = cfdi.to_dict()  # acceder al contenido en forma de objeto python
    dict_obj.get("version")  # '4.0'
    dict_obj.get("receptor").get("nombre")  # John Doe    
    dict_obj.get("emisor").get("nombre")  # Company SA de CV
```

#### `cfdi.to_raw()`
Util para extraer la información tal cual se obtiene de la interpretación 
de los XSD's.
```python
from json_cfdi import CFDI

with open("nomina-john.xml") as file:
    cfdi = CFDI(file)
    raw_obj = cfdi.to_raw()  # acceder al contenido en forma de objeto python
    raw_obj.get("attributes").get("Version")  # '4.0'
    raw_obj.get("children")[0].get("Receptor").get("Nombre")  # John Doe    
```

### Personalización
Para leer correctamente el archivo es necesario cargar los XSD adecuados al 
tipo de complementos que contenga el CFDI.

```python
from json_cfdi import CFDI
from json_cfdi.wrappers.locations import nomina12b
from json_cfdi.wrappers.schemas import get_context

context = get_context()
context["locations"] += [nomina12b]  # cargar el contexto de nomina1.2

# version 3.3
with open("cfdi33-nomina-john.xml") as file:
    cfdi33 = CFDI(file, context=context)

# version 4.0
with open("cfdi40-nomina-john.xml") as file:
    cfdi40 = CFDI(file, version=4, context=context)
```

Si necesitar cargar XSDs que no tengan soporte por `json_cfdi` siempre 
puedes cargar tus propios archivos:
```python
from json_cfdi import CFDI
from json_cfdi.wrappers.schemas import get_context

context = get_context()
context["locations"] += [
  ("http://www.sat.gob.mx/nomina12", "path/a/nomina12.xsd"),
  ...
]

with open("nomina-john.xml") as file:
    cfdi = CFDI(file, context=context)
```

### Addendas
No hay soporte para addendas ya que requiere que se den de alta `locations` 
que no son parte de estandar de CFDI o complementos del SAT.

Aún así deberías poder cargar tus propios contextos y acceder a ellos 
usando `obj.addenda`. La información que obtegas será en formato JSON.

```python
from json_cfdi import CFDI
from json_cfdi.wrappers.schemas import get_context

context = get_context()
context["locations"] += [
  ("http://www.tuempresa.com/addenda", "path/a/addenda.xsd"),
  ...
]

with open("nomina-con-addenda-john.xml") as file:
    cfdi = CFDI(file, context=context)
    model = cfdi.to_model()
    
    model.addenda  # {...} en formato json
```

## Complementos
> se pueden cargar complementos de forma personalizada (ver sección de 
**uso** arriba).

<details>
<summary>Tabla de complementos</summary>

| Complemento                                                | version          | soporte | cfdi                          | url                                                                                                          |
|------------------------------------------------------------|------------------|---------|-------------------------------|--------------------------------------------------------------------------------------------------------------|
| Recibo de pago de nómina                                   | `1.2` Revisión C | ✅       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina12.xsd                                                 |
| Recibo de pago de nómina                                   | `1.2`            | ✅       | `3.3`                         | http://omawww.sat.gob.mx/tramitesyservicios/Paginas/documentos/nomina12_.xsd                                 |
| Recibo de pago de nómina                                   | `1.1`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina11.xsd                                                 |
| Timbre Fiscal Digital                                      | `1.1`            | ✅       | `3.3`                         | https://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd                     |
| Timbre Fiscal Digital                                      | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigital.xsd                         |
| Acreditamiento IEPS                                        | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/acreditamiento/AcreditamientoIEPS10.xsd                             |
| Aerolíneas                                                 | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/aerolineas/aerolineas.xsd                                           |
| Certificado de Destrucción                                 | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/certificadodestruccion/certificadodedestruccion.xsd                 |
| Comercio Exterior                                          | `1.1` Revisión D | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/ComercioExterior11/ComercioExterior11.xsd                           |
| Comercio Exterior                                          | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/ComercioExterior/ComercioExterior10.xsd                             |
| Complemento Carta Porte                                    | `2.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/CartaPorte/CartaPorte20.xsd                                         |
| Complemento Carta Porte                                    | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/CartaPorte/CartaPorte.xsd                                           |
| Compra venta de divisas                                    | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2` `3.3` | http://www.sat.gob.mx/sitio_internet/cfd/divisas/divisas.xsd                                                 |
| Consumo de combustibles                                    | `1.1`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/consumodecombustibles/consumodeCombustibles11.xsd                   |
| Consumo de combustibles                                    | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/consumodecombustibles/consumodeCombustibles.xsd                     |
| Donatarias                                                 | `1.1`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/donat/donat11.xsd                                                   |
| Donatarias                                                 | `1.0`            | ❌       | `2.0` `3.0`                   | http://www.sat.gob.mx/sitio_internet/cfd/donat/donat.xsd                                                     |
| Estado de cuenta de combustibles de monederos electrónicos | `1.2`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/EstadoDeCuentaCombustible/ecc12.xsd                                 |
| Estado de cuenta de combustibles de monederos electrónicos | `1.1`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/EstadoDeCuentaCombustible/ecc11.xsd                                 |
| Estado de cuenta de combustibles de monederos electrónicos | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2`       | http://www.sat.gob.mx/sitio_internet/cfd/ecc/ecc.xsd                                                         |
| Complemento de Hidrocarburos (ingresos)                    | `1.0`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/IngresosHidrocarburos10/IngresosHidrocarburos.xsd                   |
| Complemento de Hidrocarburos (gastos)                      | `1.0`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/GastosHidrocarburos10/GastosHidrocarburos10.xsd                     |
| INE                                                        | `1.1`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/ine/ine11.xsd                                                       |
| INE                                                        | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/ine/ine10.xsd                                                       |
| Instituciones educativas privadas                          | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2` `3.3` | http://www.sat.gob.mx/sitio_internet/cfd/iedu/iedu.xsd                                                       |
| Leyendas fiscales                                          | `1.0`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/leyendasFiscales/leyendasFisc.xsd                                   |
| Notarios Públicos                                          | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/notariospublicos/notariospublicos.xsd                               |
| Obras de arte plásticas y antigüedades                     | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/arteantiguedades/obrasarteantiguedades.xsd                          |
| Otros derechos e impuestos                                 | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2` `3.3` | http://www.sat.gob.mx/sitio_internet/cfd/implocal/implocal.xsd                                               |
| Pago en especie                                            | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/pagoenespecie/pagoenespecie.xsd                                     |
| Persona física integrante de coordinado                    | `1.0`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/pfic/pfic.xsd                                                       |
| Recepción de pagos                                         | `2.0`            | ❌       | `3.3` `4.0`                   | http://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos20.xsd                                                   |
| Recepción de pagos                                         | `1.0`            | ❌       | `3.3` `4.0`                   | http://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos10.xsd                                                   |
| Comercio Exterior                                          | `1.1` revisión D | ❌       | `3.3` `4.0`                   | http://www.sat.gob.mx/sitio_internet/cfd/ComercioExterior11/ComercioExterior11.xsd                           |
| Comercio Exterior                                          | `1.0'`           | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/ComercioExterior/ComercioExterior10.xsd                             |
| Complemento Carta Porte                                    | `2.0`            | ❌       | -                             | http://www.sat.gob.mx/sitio_internet/cfd/CartaPorte/CartaPorte20.xsd                                         |
| Complemento Carta Porte                                    | `1.0`            | ❌       | -                             | http://www.sat.gob.mx/sitio_internet/cfd/CartaPorte/CartaPorte.xsd                                           |
| Compra venta de divisas                                    | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2` `3.3` | http://www.sat.gob.mx/sitio_internet/cfd/divisas/divisas.xsd                                                 |
| Consumo de combustibles                                    | `1.1`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/consumodecombustibles/consumodeCombustibles11.xsd                   |
| Consumo de combustibles                                    | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/consumodecombustibles/consumodeCombustibles.xsd                     |
| Donatarias                                                 | `1.1`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/donat/donat11.xsd                                                   |
| Donatarias                                                 | `1.0`            | ❌       | `2.0` `3.0`                   | http://www.sat.gob.mx/sitio_internet/cfd/donat/donat.xsd                                                     |
| Estado de cuenta de combustibles de monederos electrónicos | `1.2`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/EstadoDeCuentaCombustible/ecc12.xsd                                 |
| Estado de cuenta de combustibles de monederos electrónicos | `1.1`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/EstadoDeCuentaCombustible/ecc11.xsd                                 |
| Estado de cuenta de combustibles de monederos electrónicos | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2`       | http://www.sat.gob.mx/sitio_internet/cfd/ecc/ecc.xsd                                                         |
| Complemento de Hidrocarburos (gastos)                      | `1.0`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/GastosHidrocarburos10/GastosHidrocarburos10.xsd                     |
| Complemento de Hidrocarburos (ingresos)                    | `1.0`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/IngresosHidrocarburos10/IngresosHidrocarburos.xsd                   |
| INE                                                        | `1.1`            | ❌       | `3.3`                         | http://www.sat.gob.mx/sitio_internet/cfd/ine/ine11.xsd                                                       |
| INE                                                        | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/ine/ine10.xsd                                                       |
| Instituciones educativas privadas                          | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2` `3.3` | http://www.sat.gob.mx/sitio_internet/cfd/iedu/iedu.xsd                                                       |
| Leyendas fiscales                                          | `1.0`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/leyendasFiscales/leyendasFisc.xsd                                   |
| Notarios Públicos                                          | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/notariospublicos/notariospublicos.xsd                               |
| Obras de arte plásticas y antigüedades                     | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/arteantiguedades/obrasarteantiguedades.xsd                          |
| Otros derechos e impuestos                                 | `1.0`            | ❌       | `2.0` `2.2` `3.0` `3.2` `3.3` | http://www.sat.gob.mx/sitio_internet/cfd/implocal/implocal.xsd                                               |
| Pago en especie                                            | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/pagoenespecie/pagoenespecie.xsd                                     |
| Persona física integrante de coordinado                    | `1.0`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/pfic/pfic.xsd                                                       |
| Renovación y sustitución de vehículos                      | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/renovacionysustitucionvehiculos/renovacionysustitucionvehiculos.xsd |
| Sector de ventas al detalle (Detallista)                   | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/detallista/detallista.xsd                                           |
| Servicios parciales de construcción                        | `1.0`            | ❌       | -                             | http://www.sat.gob.mx/sitio_internet/cfd/servicioparcialconstruccion/servicioparcialconstruccion.xsd         |
| SPEI de tercero a tercero                                  | `1.0`            | ❌       | `3.2`                         | http://www.sat.gob.mx/sitio_internet/cfd/spei/spei.xsd                                                       |
| Teceros                                                    | `1.1`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/terceros/terceros11.xsd                                             |
| Turista pasajero extranjero                                | `1.0`            | ❌       | `2.2` `3.2` `3.3`             | http://www.sat.gob.mx/sitio_internet/cfd/TuristaPasajeroExtranjero/TuristaPasajeroExtranjero.xsd             |
| Vales de despensa                                          | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/valesdedespensa/valesdedespensa.xsd                                 |
| Vehículo usado                                             | `1.0`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/vehiculousado/vehiculousado.xsd                                     |
| Venta de vehículos                                         | `1.1`            | ❌       | `3.2` `3.3`                   | http://www.sat.gob.mx/sitio_internet/cfd/ventavehiculos/ventavehiculos11.xsd                                 |
| Venta de vehículos                                         | `1.0`            | ❌       | `2.2` `3.2`                   | http://www.sat.gob.mx/sitio_internet/cfd/ventavehiculos/ventavehiculos.xsd                                   |

</details>

### Otros

CFDI (factura) de retenciones
Es un comprobante que ampara las retenciones efectuadas y los pagos realizados a residentes nacionales y en el extranjero.
Cuando en el desarrollo de tu actividad económica estés obligado a incluir en un CFDI las retenciones de impuestos que efectúas, o por los pagos realizados, incluye los complementos:

<details>
<summary>Tabla de complementos</summary>

| Complemento                   | version | soporte | cfdi | url                                                                                                      |
|-------------------------------|---------|---------|------|----------------------------------------------------------------------------------------------------------|
| Enajenación de acciones       | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/enajenaciondeacciones/enajenaciondeacciones.xsd           |
| Dividendos                    | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/dividendos/dividendos.xsd                                 |
| Intereses                     | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/intereses/intereses.xsd                                   |
| Arrendamiento                 | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/arrendamientoenfideicomiso/arrendamientoenfideicomiso.xsd |
| Pagos a extranjeros           | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/pagosaextranjeros/pagosaextranjeros.xsd                   |
| Premios                       | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/premios/premios.xsd                                       |
| Fideicomisos no empresariales | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial/fideicomisonoempresarial.xsd     |
| Planes de retiro              | `1.1`   | ❌       | `*`  | https://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro11/planesderetiro11.xsd                    |
| Intereses Hipotecarios        | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/intereseshipotecarios/intereseshipotecarios.xsd           |
| Operaciones con derivados     | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/operacionesconderivados/operacionesconderivados.xsd       |
| Sector financiero             | `1.0`   | ❌       | `*`  | http://www.sat.gob.mx/esquemas/retencionpago/1/sectorfinanciero/sectorfinanciero.xsd                     |
| Plataformas Tecnológicas      | -       | ❌       | -    | -                                                                                                        |
</details>
