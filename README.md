# Sistema Experto para Diagnóstico de Plagas en Cultivos 🌱

## Descripción

Aplicación desarrollada en **Streamlit** que utiliza un **sistema experto basado en reglas (Experta)** para diagnosticar plagas agrícolas según los síntomas observados en los cultivos.  
El sistema razona con **encadenamiento hacia adelante** y explica las reglas activadas para mantener transparencia y trazabilidad.

---

## Objetivos

- Diagnosticar la plaga más probable según los síntomas ingresados.  
- Recomendar una acción inicial de tratamiento.  
- Explicar el razonamiento utilizado (“por qué eligió esa plaga”).  
- Promover decisiones informadas y responsables en agricultura.
---
## Interfaz:

- Seleccionar el cultivo.
- Ingresar los síntomas observados.
- Presionar “Diagnosticar”.
- Ver la plaga probable, acción recomendada y reglas activadas.


## 🚀 Cómo clonar y ejecutar el proyecto

### 1. Clonar el repositorio

```bash
    git clone https://github.com/Pandaman08/proyecto_plagas.git
```
```bash
    cd proyecto_plagas
```
### 2. Crear un entorno virtual (recomendado)
- ⚠️ Importante: Usa Python 3.10, 3.11 o 3.12.
- No uses Python 3.14 (incompatible con experta y frozendict).
- En Windows (PowerShell): 
```bash 
    python -m venv plagas
```
- Con conda:
```bash
    conda create -n plaga python=3.11
```
### 3. Activar el entorno:
-Usando python -m venv
```bash
    plagas\Scripts\Activate.ps1
```
-💡 Si recibes un error de ejecución de scripts, ejecuta primero: 
```bash
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    plagas\Scripts\Activate.ps1
```
- Usando conda:
```bash
    conda activate plagas
```
### 4. Instalar dependencias
```bash
    pip install -r requirements.txt
```

### 5. Ejecutar la aplicación
```bash
    streamlit run app.py
```