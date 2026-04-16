# Simulador de productos COF_ES

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-brightgreen)

Aplicación Streamlit para simular los datos financieros de cualquier producto: cálculo de cuotas, cuadro de amortización, TAE y ejemplo representativo.

---

## Estructura del Proyecto

- **README\.MD**
- **requirements.txt**
- **Simulacion_amortizable_unitaria.py** - Interfaz principal con el simulador operaciones unitarias para los productos amortizables.

- **/bin/**
  - **COFES\_\_\_TAE.py** - Funciones comunes para el cómputo de la TAE.
  - **COFES\_\_\_tools.py** - Funciones comunes a todos los simuladores.
  - **COFES\_\_SIM_4CB.py** - Funciones para el simulador de facilidades de pago.
  - **COFES\_\_SIM_AMO.py** - Funciones para el simulador de productos amortizables.
  - **COFES\_\_SIM_RCC.py** - Funciones para el simulador de productos revolving.

- **/data/**
  - **COFES_00_PRODUCTOS_DICCIONARIO.csv** - Contiene el detalle de los productos amortizables.
  - **COFES_01_Date_Blocage.csv** - Contiene el listado de fechas de cierre contable.

- **/pages/**
  - **1_Simulacion_4CB.py** — Simulador unitario y masivo para facilidades de pago.
  - **2_Simulacion_NFOIS_unitaria.py** — (En pruebas) Simulador unitario para los productos NFOIS.
  - **3_Simulacion_revolving_unitaria.py** — (En pruebas) Simulador unitario para los productos revolving.
  - **4_Simulacion_amortizable_masiva.py** — Simulador masivo para los productos amortizables.

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
xlsxwriter
```

Ejecuta la aplicación:

```bash
# Ejecuta la aplicación
streamlit run Simulacion_amortizable_unitaria.py
```

---

## 📦 Dependencias

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://pypi.org/project/numpy/)
- [xlsxwriter](https://pypi.org/project/xlsxwriter/)

---

### 👥 Contribuyentes

<img src="https://github.com/fjhidalgo-coding.png" width="24" height="24"> [fjhidalgo-coding](https://github.com/fjhidalgo-coding)
<img src="https://github.com/mildredbr-design.png" width="24" height="24"> [mildredbr-design](https://github.com/mildredbr-design)

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

### v1.0.0 Versión estable (20256-04-20)

**Mejoras implementadas:**

- Simulador para los productos revolving.
- Simulador para los productos NFOIS.
- Simulador para las facilidades de pago 4CB (cálculo unitario y masivo).
- Simulador masivo para los productos amortizables.
- Adaptación de los simuladores de amortizable a los productos AUTO / MOTO Balloon.

**Fixed bugs:**

- Precisión del cálculo de la TAE.
- Remplazo de las variables `float` por variables `Decimal`.
- Calcular el nº de días del año en función del vencimiento evaluado en lugar de en función de la fecha de financiación al calcular la fracción de tiempo para la TAE en los años bisiestos.
- Cálculo por días de la prima de seguro capitalizada durante la carencia de un préstamo CFUSION cuando ésta supera el mes de duración.
- Carencia diferida con TIN 0,00% para el producto `B 2460050001 - Compra a Plazos Vorwerk`.
- Error en los cálculos del primer vencimiento y en los redondeos.

**Closed issues:**

- Adaptación a Streamlit 1.56.0 (conversión de los DataFrame Pandas a `String` para evitar errores con Arrow).
- Descarga de los resultados en Excel.
- Actualizar el límite del porcentaje máximo para la comisión de apertura.
- Formateo de los decimales y las fechas.

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
