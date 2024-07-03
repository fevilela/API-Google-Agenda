import os.path
import datetime
import pickle
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Se modificando esses SCOPES, apague o arquivo token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def generate_event_key(event):
    """Gera uma chave única para um evento usando seus atributos principais."""
    return (event.get('id', ''), event.get('summary', ''))

def is_conflicting(event1, event2):
    """Verifica se dois eventos estão em conflito."""
    start1 = event1['start'].get('dateTime', event1['start'].get('date'))
    end1 = event1['end'].get('dateTime', event1['end'].get('date'))
    start2 = event2['start'].get('dateTime', event2['start'].get('date'))
    end2 = event2['end'].get('dateTime', event2['end'].get('date'))

    # Convertendo para datetime com fuso horário para comparação
    start1 = datetime.datetime.fromisoformat(start1.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)
    end1 = datetime.datetime.fromisoformat(end1.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)
    start2 = datetime.datetime.fromisoformat(start2.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)
    end2 = datetime.datetime.fromisoformat(end2.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)

    # Verifica se há sobreposição
    return max(start1, start2) < min(end1, end2)

def calculate_event_duration(start, end):
    """Calcula a duração do evento em minutos."""
    start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)
    end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)
    duration = end_dt - start_dt
    return duration.total_seconds() / 60

def get_full_name_from_email(email):
    """Extrai e formata o nome completo a partir do email."""
    name_part = email.split('@')[0]
    name_part = name_part.replace('.', ' ')
    return ' '.join(word.capitalize() for word in name_part.split())

def save_events_to_csv(events, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Titulo', 'Data Inicio', 'Data Final', 'Nome Criador', 'Email Criador', 'Conflito', 'Evento ID', 'DuracaoMinutos'])
        
        for event in events:
            event_id = event.get('id', '')
            titulo = event.get('summary', '')
            data_inicio = event['start'].get('dateTime', event['start'].get('date'))
            data_final = event['end'].get('dateTime', event['end'].get('date'))
            
            criador_email = event.get('creator', {}).get('email', '')
            criador_nome = get_full_name_from_email(criador_email)

            if not criador_email or not criador_nome:
                organizer = event.get('organizer', {})
                criador_email = organizer.get('email', '')
                criador_nome = get_full_name_from_email(criador_email)

            conflito = any(is_conflicting(event, e) for e in events if e != event)
            duracao = calculate_event_duration(data_inicio, data_final)

            data_inicio_iso = datetime.datetime.fromisoformat(data_inicio.replace('Z', '+00:00')).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if data_inicio else None
            data_final_iso = datetime.datetime.fromisoformat(data_final.replace('Z', '+00:00')).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if data_final else None

            writer.writerow([titulo, data_inicio_iso, data_final_iso, criador_nome, criador_email, conflito, event_id, duracao])

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": "seu-id-cliente",
                    "project_id": "seu-projeto-id",
                    "auth_uri": "sua-uri",
                    "token_uri": "sua-uri",
                    "auth_provider_x509_cert_url": "sua-url",
                    "client_secret": "seu-client-secret",
                    "redirect_uris": ["sua-uris"]
                }
            }, SCOPES)
            creds = flow.run_local_server()

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])

    start_date = datetime.datetime(datetime.datetime.now().year, 1, 1).isoformat() + 'Z'
    end_date = datetime.datetime(datetime.datetime.now().year, 12, 31).isoformat() + 'Z'

    print('Getting the upcoming events from all calendars')

    all_events = []
    seen_event_keys = set()

    for calendar in calendars:
        calendar_id = calendar['id']
        events_result = service.events().list(calendarId=calendar_id, timeMin=start_date,
                                              timeMax=end_date, maxResults=2500, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        for event in events:
            if 'Holidays' not in event.get('creator', {}).get('displayName', '') and 'Holidays' not in event.get('organizer', {}).get('displayName', ''):
                event_key = generate_event_key(event)
                if event_key not in seen_event_keys:
                    seen_event_keys.add(event_key)
                    all_events.append(event)

    if not all_events:
        print('No upcoming events found.')
        return

    # Caminho do arquivo onde os dados serão salvos
    file_path = 'caminho_que_você_quer_salvar/google_calendar_events.csv'

    save_events_to_csv(all_events, file_path)

if __name__ == '__main__':
    main()
