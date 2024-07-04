 <h1 align="center">API-Google-Agenda</h1>
<h4>Objetivo do Script</h4>
<p>O script "Google Agenda CSV" foi desenvolvido para extrair eventos de todos os calendários do Google Calendar de um usuário, verificando conflitos entre eventos e salvando todas as informações relevantes em um arquivo CSV. Esta abordagem facilita a análise e o compartilhamento de dados de agenda em formatos amigáveis e amplamente compatíveis, como o CSV.</p>

<h4>Funcionalidades Principais</h4>
<ol>
  <li><b>Autenticação e Autorização:</b></li>
    <ul>
      <li>Utiliza a API do Google Calendar para acessar e extrair dados de eventos.</li>
      <li>Autentica o usuário via OAuth 2.0, salvando o token de acesso em um arquivo token.pickle para reutilização em futuras execuções.</li>
    </ul>
  <br>
  <li><b>Extração de Eventos:</li></b>
    <ul>
      <li>Obtém eventos de todos os calendários associados ao usuário.</li>
      <li>Filtra eventos irrelevantes, como feriados, para focar em eventos significativos.</li>
    </ul>
    <br>
  <li><b>Verificação de Conflitos:</li></b>
    <ul>
      <li>Verifica se há sobreposição de horários entre eventos para identificar conflitos.</li>
    </ul>
    <br>
  <li><b>Cálculo de Duração:</li></b>
    <ul>
      <li>Calcula a duração de cada evento em minutos.</li>
    </ul>
    <br>
  <li><b>Salvamento em CSV:</b></li>
    <ul>
      <li>Salva os dados dos eventos, incluindo título, datas, duração, criador, e descrição, em um arquivo CSV especificado pelo usuário.</li>
    </ul>
</ol>
<br>
<h2>Execução do Script</h2>
<h4><b>Pré-requisitos</b></h4>
<ul>
  <li>Python instalado</li>
  <li>Bibliotecas Python necessárias: <b>google-auth</b>, <b>google-auth-oauthlib</b>, <b>google-auth-httplib2</b>, <b>google-api-python-client</b>, <b>csv</b>.</li>
</ul>
<h4>Passos para Configuração</h4>
<ol>
  <li>Obtenção das Credenciais do Google API:</li>
  <p>Para interagir com a API do Google Calendar, você precisará de credenciais OAuth 2.0. Siga os passos abaixo para obter essas credenciais:</p>
  <ul>
    <li>Acesse o <a href= "https://console.cloud.google.com/?hl=pt-br"> Google Cloud Console.</a></li>
    <br>
    <li>Crie um novo projeto ou selecione um projeto existente.</li>
    <br>
    <li>Navegue até "APIs e Serviços" > "Tela de consentimento OAuth" e configure a tela de consentimento se ainda não o fez.</li>
    <br>
    <li>Vá para "Credenciais" e clique em "Criar credenciais" > "ID do cliente OAuth 2.0".</li>
    <br>
    <li>Escolha o tipo de aplicativo (por exemplo, Aplicativo de Área de Trabalho).</li>
    <br>
    <li>Após criar as credenciais, faça o download do arquivo JSON. Este arquivo contém o client_id, project_id e client_secret que serão usados pelo script.</li>
  </ul>
 <br>
  <li>Configuração do Script:</li>
  <p>Salve o arquivo JSON das credenciais no mesmo diretório do script e modifique o script para usar este arquivo. Aqui está um exemplo da estrutura do arquivo JSON:</p>
<code>{
  "installed": {
    "client_id": "SEU_CLIENT_ID",
    "project_id": "SEU_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "SEU_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
</code>
<br>
 <li>Execução do Script:</li>
 <p>Execute o script no terminal ou ambiente de desenvolvimento Python:</p>
 <code>python google_agenda_csv.py</code>
 <br><br>
 <p>Durante a primeira execução, uma janela do navegador será aberta para você autenticar e autorizar o acesso aos seus calendários do Google. O token de acesso será salvo no arquivo token.pickle para reutilização.</p>
 <br>
 <li>Exemplo de Uso:</li>
<p>Abaixo está um exemplo de como o script salva eventos no arquivo CSV especificado:</p>
 <code># Caminho do arquivo onde os dados serão salvos
file_path = 'caminho/para/seu/arquivo/google_calendar_events.csv'
save_events_to_csv(all_events, file_path)</code>
<br><br>
<p>Você pode modificar file_path para qualquer diretório e nome de arquivo desejado.</p>
</ol>
<h2>Conclusão</h2>
<p>O script "Google Agenda CSV" é uma ferramenta útil para extrair, analisar e compartilhar dados de eventos do Google Calendar. Ele permite uma visão detalhada dos eventos, verifica conflitos e facilita a manipulação dos dados através do formato CSV. Siga os passos de configuração cuidadosamente para garantir que o script funcione corretamente.</p>
