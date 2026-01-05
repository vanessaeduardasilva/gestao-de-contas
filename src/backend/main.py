import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # Define o caminho para a pasta backend onde os arquivos devem estar
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Usa o arquivo que você baixou e renomeou
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def criar_lembrete_google(titulo, data_vencimento, valor):
    service = get_calendar_service()
    event = {
        'summary': f'PAGAMENTO: {titulo}',
        'description': f'Valor: R$ {valor}. Registrado via Organizerion.',
        'start': {'date': data_vencimento},
        'end': {'date': data_vencimento},
    }
    return service.events().insert(calendarId='primary', body=event).execute()