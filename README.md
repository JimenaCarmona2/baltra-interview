# Technical Assessment - Recruiting Analytics

## Requisitos
- Python 3.11.5
- Cuenta de Gmail
- API Key de Anthropic

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JimenaCarmona2/baltra-interview.git
   cd baltra-interview
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\Activate # Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copia el archivo de configuración de ejemplo y edítalo con tus datos:
   ```bash
   cp .env.example .env
   # Edita .env con tu API key y credenciales SMTP
   ```

## Uso

1. Coloca tus archivos `candidates.csv` y `candidate_funnel_logs.csv` en la raíz del proyecto.
2. Ejecuta el script principal:
   ```bash
   python email_automation.py
   ```
   Esto generará el análisis y enviará el reporte por correo.

## Notas
- Si usas Gmail, debes generar una contraseña de aplicación para SMTP.
- El análisis usa una skill personalizada de Claude (Anthropic).