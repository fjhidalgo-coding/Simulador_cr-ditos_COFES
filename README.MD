# Simulador de Préstamos Amortizables COF_ES

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-brightgreen)

Aplicación desarrollada en **Streamlit** para simular operaciones de productos amortizables de COF_ES. Permite configurar las condiciones de un préstamo, visualizar el cuadro de amortización, el cálculo de la TAE y obtener un ejemplo representativo del producto seleccionado.

---

## Estructura del Proyecto

- **app_simulador_CLB.py**  
  Archivo principal de la aplicación Streamlit. Gestiona la interfaz de usuario, la entrada de datos y la visualización de resultados.

- **COFES\_\_SIM_AMO_Consola.py**  
  Módulo con la lógica de simulación y cálculo de préstamos, generación de cuadros de amortización y cálculo de TAE.

---

## 🚀 Instalación

```bash
# Instala dependencias
pip install streamlit pandas
```

Coloca los archivos en una carpeta y ejecuta la aplicación:

```bash
# Ejecuta la aplicación
streamlit run app_simulador_CLB.py
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

---

## 🎨 Personalización

Puedes modificar los productos, seguros y parámetros en el módulo `COFES__SIM_AMO_Consola.py` para adaptarlo a nuevas ofertas o condiciones.

---

### 👥 Contribuyentes

<img src="https://github.com/fjhidalgo-coding.png" width="24" height="24"> [fjhidalgo-coding](https://github.com/fjhidalgo-coding)

---

### 🤝 Cómo contribuir

1.  Crea un issue en este repositorio explicando la propuesta de cambio.
2.  Haz un fork del repositorio.
3.  Crea una nueva rama (`git checkout -b feature/AmazingFeature`).
4.  Haz tus cambios y haz el commit (`git commit -m 'Add some AmazingFeature'`).
5.  Sube tus cambios a la rama (`git push origin feature/AmazingFeature`).
6.  Abre un Pull Request en este repositorio.

---

**Nota:**  
Este simulador es una herramienta para comprobar los cálculos del sistema y no constituye una oferta vinculante. Los resultados pueden variar según las condiciones reales del contrato.

---
