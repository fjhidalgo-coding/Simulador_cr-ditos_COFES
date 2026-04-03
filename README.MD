# Simulador de Préstamos Amortizables COF_ES

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-brightgreen)

Aplicación Streamlit para simular productos amortizables de COF_ES: cálculo de cuotas, cuadro de amortización, TAE y ejemplo representativo.

---

## Estructura del Proyecto

- **requirements.txt**
- **app_simulador_CLB.py** - Interfaz principal con el simulador operaciones unitarias
- **/pages/**
  - **1_Simulación_masiva.py** — Simulación masiva de operaciones.
  - **2_Simulación_curso_vida.py** — (En construcción) Simulación de operaciones en curso de vida del préstamo.
- **/data/**
  - **COFES_00_PRODUCTOS_DICCIONARIO.csv** - Contiene el detalle de los productos
  - **COFES_01_Date_Blocage.csv** - Contiene el listado de fechas de cierre contable

- **/bin/**
  - **COFES\_\_SIM_AMO_Consola.py** - Funciones para realizar las simulaciones de préstamo

---

## 🚀 Instalación

Creación y activación del entorno virtual e instalación de las dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
source .venv/Scripts/activate
pip install -r requirements.txt
```

requirements.txt:

```
streamlit
pandas
numpy
```

Ejecuta la aplicación:

```bash
# Ejecuta la aplicación
streamlit run Simulacion_amortizable_unitaria.py
```

---

## 📝 Uso

1. Selecciona el producto de crédito en la barra lateral.
2. Personaliza fechas, importe, plazo, tipo de interés y otros parámetros.
3. Configura el seguro y la comisión de apertura si el producto lo permite.
4. Para productos con segunda secuencia financiera, activa la opción y configura los valores.
5. Visualiza los resultados en las pestañas:
   - **Secuencias financieras**: Resumen de vencimientos y cuotas.
   - **Ejemplo representativo**: Texto explicativo del préstamo simulado.
   - **Cuadro de amortización**: Detalle mensual de pagos, intereses y capital.
   - **Detalle TAE**: Cálculo de la TAE y VAN.

---

## 🛠️ Principales Funcionalidades

| Funcionalidad           | Descripción                             |
| ----------------------- | --------------------------------------- |
| Simulación de préstamos | Diferentes productos y condiciones      |
| Cálculo automático      | Cuotas, intereses, comisiones y seguros |
| Visualización           | Cuadros de amortización y TAE           |
| Ejemplo representativo  | Información clara para el cliente       |
| Interfaz interactiva    | Personalización de parámetros           |

---

## 📦 Dependencias

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://pypi.org/project/numpy/)

---

## 🎨 Personalización

Puedes modificar los productos, seguros y parámetros en el módulo `COFES__SIM_AMO_Consola.py` para adaptarlo a nuevas ofertas o condiciones.

---

### 👥 Contribuyentes

<img src="https://github.com/fjhidalgo-coding.png" width="24" height="24"> [fjhidalgo-coding](https://github.com/fjhidalgo-coding)
<img src="https://github.com/mildredbr-design.png" width="24" height="24"> [mildredbr-design](https://https://github.com/mildredbr-design)

---

### 🤝 Cómo contribuir

1.  Crea un issue en este repositorio explicando la propuesta de cambio.
2.  Haz un fork del repositorio.
3.  Crea una nueva rama (`git checkout -b feature/AmazingFeature`).
4.  Haz tus cambios y haz el commit (`git commit -m 'Add some AmazingFeature'`).
5.  Sube tus cambios a la rama (`git push origin feature/AmazingFeature`).
6.  Abre un Pull Request en este repositorio.

---

## Changelog

### v1.0.0.BETA (2025-10-20)

**Mejoras implementadas:**

- Refactorización en Python + Streamlit (publicación en [Cloud Streamlit](https://cofes-app-simulador-clb.streamlit.app/)).
- Añadir posibilidad de Option+ con segunda secuencia % respecto al financiado.
- Generar el ejemplo representativo de manera automática.

**Fixed bugs:**

- ~~El cálculo de la TAE --> Error en las CAP capitalizadas~~.
- El cálculo de la prima de seguro AUTO NO debe redondear en el paso final de los cálculos sino en el cálculo de la prima por asegurado.
- Error en los intereses cuando el contrato tiene carencia ya que duplicamos el contador al contabilidad los intereses capitalizados.
- Cuando seleccionamos el producto OPTION+ gratuito, el simulador no aplica interés en la segunda secuencia.
- Error cálculo fecha primer vencimiento en CFUSION forzando un mínimo de 14 días desde la financiación.
- Error cálculo prima de seguro de CFUSION cuando la fecha de financiación corresponde a un día de pago.

**Closed issues:**

- Comprobar que calculamos el descuento partner con las reglas facilitadas en el SA52221677.
- Modificamos el límite máximo de CAP a 500,00€ (antes 90,00€).
- Supresión del suelo en las comisiones de apertura.
- Date de blocage del año 2024 (SA52299989).
- Date de blocage del año 2025 (SA56843696).
- Date de blocage del año 2026.

### v0.6.1 (2022-12-27)

**Closed issues:**

- Date de blocage del año 2023.

### v0.6 (2022-02-28)

**Mejoras implementadas:**

- Adaptación del cálculo de la prima de seguro al proyecto ADE2T (2 asegurados en CPROYECTO y CFUSION con bonificación de la prima).
- Adaptación a la recapitalización (forzada) de la comisión de apertura partners (PTPA0143).
- Permitir recálculos de financiaciones de hasta 360 mensualidades.

### v0.5.2 (2021-11-03)

**Fixed bugs:**

- Corrección en el cómputo de días del cálculo de la TAE para los vencimientos cuya fecha valor es la fecha de financiación (TAE mal simulada en los meses de enero posteriores a un año bisiesto).

### v0.5.1 (2021-09-20)

**Fixed bugs:**

- Cálculo correcto de la prima de seguro del periodo de carencia para CFUSION + CPROYECTO (SA45573947).

### v0.5 (2021-05-18)

**Mejoras implementadas:**

- Refactorización del simulador.
- Nueva configuración de productos que facilita la adaptación a los nuevos productos amortizables.
- Adaptación al Crédito Fusión.
- Adaptación al Crédito AUTO.
- Adaptación al Vorwerk Option Plus.
- Cálculo automático de las fechas ADC-1 y ADC+1.
- Cálculo masivos de simulaciones de crédito.
- Añadir campo de Importe Mínimo / Máximo de la CA (en cálculo masivo + individual forzado + parametrización).
- Recapitalización de la comisión de apertura y cálculo de la cuota con comisión de apertura recapitalizada.

**Fixed bugs:**

- Cálculo de intereses incorrecto en el primer vencimiento tras una carencia en los productos Vorwerk.
- Cálculo correcto de la fecha del primer recibo de CFUSION + CPROYECTO (sin carencia).
- Corrección redondeo aplicado en el cálculo de la mensualidad de un contrato Anivestreno / Vorwerk Option Plus.

**Closed issues:**

- Date de blocage del año 2020.
- Date de blocage del año 2021.
- Date de blocage del año 2022.

### v0.4 (2020-05-19)

**Mejoras implementadas:**

- Inclusión del seguro en la cuota TAE cuando éste sea obligatorio.

### v0.3.3 (2018-06-25)

**Closed issues:**

- Date de blocage del año 2019.

### v0.3.2 (2017-12-22)

**Mejoras implementadas:**

- Mejora lógica asociada al cálculo de los intereses y seguros ordinarios con la finalidad de simplificarla.

**Fixed bugs:**

- Según SA34319500, los intereses (¿y seguro?) de carencia a recapitalizar se calculan mes a mes redondeándolos.

### v0.3.1 (2017-12-18)

**Fixed bugs:**

- Corrección en la validación asociada al campo "F_Blocage posterior a la financiación" ya que no estaba validando la fecha ADC de la colección correspondiente.
- Control TIN 0,00% Partner.

### v0.3 (2017-12-05)

**Mejoras implementadas:**

- Calcular el descuento de los productos gratuitos.
- En función de una "configuración" asociada al producto, calcular la CAP truncada o redondeada.
- Mejora en la prioridad de alertas informativas. La alerta asociada a la TAE debe tener más prioridad.
- Validación de las fechas de ADC con una lista coleccionable.

**Fixed bugs:**

- Cálculo de los intereses del 1er vencimiento cuando financiación = fecha échéance se calcula por días naturales en lugar de por periodos.
- Para los productos Vorwerk no se puede calcular différés ya que aumentaría el importe de la primera mensualidad.

### v0.2 (2017-11-26)

**Mejoras implementadas:**

- Adaptación del simulador a los productos con cuota discontinua con comisión de apertura.
- Cálculo automático de la TAE con una macro.

**Fixed bugs:**

- Ajuste última cuota ordinaria forzando el vencimiento de todo el capital disminuyendo el interés devengado.
- Ajuste última cuota "leasing" forzando el vencimiento de todo el capital disminuyendo el interés devengado.
- Redondeado del valor residual cuando éste es calculado con un porcentaje.

### v0.1 (2017-10-16)

**Mejoras implementadas:**

- Versión inicial del simulador en excel para los productos con cuota discontinua ("leasing").
- Simulador de cuotas y de cuadros de amortización.
- Cálculo de los vencimientos de carencia normal y carencia diferida.

---

**Nota:**  
Este simulador es una herramienta para comprobar los cálculos del sistema y no constituye una oferta vinculante. Los resultados pueden variar según las condiciones reales del contrato.

---
