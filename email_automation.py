import anthropic
import dotenv
import smtplib
import schedule
import time
import json
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from datetime import datetime

dotenv.load_dotenv()

client = anthropic.Anthropic(
    api_key=dotenv.get_key(".env", "ANTHROPIC_API_KEY")
)

# AI generated email template
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; color: #333; line-height: 1.6; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        .summary { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .funnel-stage { margin: 15px 0; }
        .stage-name { font-weight: bold; color: #2c3e50; }
        .stage-bar { 
            background: #3498db; 
            height: 30px; 
            border-radius: 5px; 
            display: flex; 
            align-items: center; 
            padding-left: 10px;
            color: white;
            font-weight: bold;
        }
        .stage-info { margin-top: 5px; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Reporte Mensual de Reclutamiento Baltra</h1>
        <p><strong>Fecha:</strong> {{ report_date }}</p>
        
        <div class="summary">
            <h2>Resumen General</h2>
            <p style="font-size: 24px; margin: 0;"><strong>Total de Candidatos:</strong> {{ total_candidates }}</p>
        </div>
        
        <h2>Desglose por Etapa del Funnel</h2>
        {% for stage_name, stage_data in funnel_stages.items() %}
        <div class="funnel-stage">
            <div class="stage-name">{{ stage_name }}</div>
            <div class="stage-bar" style="width: {{ stage_data.percentage }}%;">
                {{ stage_data.count }} candidatos
            </div>
            <div class="stage-info">{{ stage_data.percentage }}% del total</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def generate_report():
    candidates_file = client.beta.files.upload(
        file=open("candidates.csv", "rb"),
    )
    logs_file = client.beta.files.upload(
        file=open("candidate_funnel_logs.csv", "rb"),
    )

    response = client.beta.messages.create(
        model=dotenv.get_key(".env", "ANTHROPIC_MODEL"),
        betas=["code-execution-2025-08-25", "skills-2025-10-02", "files-api-2025-04-14"],
        temperature=0.0,
        max_tokens=4096,
        container={
            "skills": [
                {
                    "type": "custom",
                    "skill_id": "skill_019YX6mXMD6a2JxgJ8U2Ms58",
                    "version": "1770078546833257"
                }
            ]
        },
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Use the recruiting-analytics skill to analyze the funnel data in these two CSV files and return the JSON summary. Just return the JSON summary. Do not include any other text."},
                {"type": "container_upload", "file_id": candidates_file.id},
                {"type": "container_upload", "file_id": logs_file.id}
            ]
        }],
        tools=[{
            "type": "code_execution_20250825",
            "name": "code_execution"
        }]
    )

    results = extract_json_from_bash_result(response)
    if not results:
        print("No se pudo extraer el JSON del resultado.")
        return
    
    template = Template(EMAIL_TEMPLATE)
    html_content = template.render(
        report_date=results.get('report_date', datetime.now().strftime("%Y-%m-%d")),
        total_candidates=results['total_candidates'],
        funnel_stages=results['funnel_stages']
    )
    return html_content, results

# AI generated helper function to extract JSON from bash result
def extract_json_from_bash_result(response):
    bash_blocks = [block for block in response.content if block.__class__.__name__ == 'BetaBashCodeExecutionToolResultBlock']
    if not bash_blocks:
        return None
    last_block = bash_blocks[-1]
    # stdout can be on .content.stdout or .stdout depending on the SDK
    stdout = getattr(getattr(last_block, 'content', last_block), 'stdout', None)
    if not stdout:
        return None
    match = re.search(r'\{[\s\S]*\}', stdout)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None

def send_email(html_content):
    smtp_server = dotenv.get_key(".env", "SMTP_SERVER")
    smtp_port = int(dotenv.get_key(".env", "SMTP_PORT"))
    smtp_user = dotenv.get_key(".env", "SMTP_USER")
    smtp_password = dotenv.get_key(".env", "SMTP_PASSWORD")
    smtp_recipient = dotenv.get_key(".env", "SMTP_RECIPIENT")
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Reporte mensual de reclutamiento Baltra - {datetime.now().strftime('%B %Y')}"
    msg['From'] = smtp_user
    msg['To'] = smtp_recipient
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
    
    print(f"Email enviado exitosamente a {smtp_recipient}")

def send_monthly_report():
    html_content, _ = generate_report()
    send_email(html_content)

schedule.every(30).days.do(send_monthly_report)

if __name__ == '__main__':
    html_content, _ = generate_report()
    send_email(html_content)
    while True:
        schedule.run_pending()
        time.sleep(60)