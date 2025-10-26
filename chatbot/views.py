import os
import json
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage, ChatSession


# 🔹 Carrega as variáveis do .env
load_dotenv()

# 🔹 Lê a chave da OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 🔹 Contexto da CoderTec
CODERTEC_CONTEXT = """
A CoderTec é especializada em Automação, Inteligência Artificial e Ciência de Dados.
Desenvolvemos sites, dashboards e soluções web com Python, Django, Streamlit e automações inteligentes.
Atendemos profissionais da saúde e pequenas empresas.
Oferecemos serviços de:
- Desenvolvimento Web
- Dashboards de Dados
- Agentes de IA
- Automação de Processos
"""

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    data = json.loads(request.body)
    message = data.get("message", "")
    context = data.get("context", "geral")
    user_name = data.get("user_name", "")
    business_type = data.get("business_type", "")
    
    # 🔹 Cria ou recupera sessão
    session, created = ChatSession.objects.get_or_create(
        user_name=user_name or None,
        business_type=business_type or None,
        context=context
    )

     # 🔹 Guarda mensagem do usuário
    ChatMessage.objects.create(session=session, sender="user", message=message)

    # 🔹 Gera resposta (você pode manter a sua lógica atual)
    reply = gerar_resposta_contextual(message, context)

    # 🔹 Guarda resposta do bot
    ChatMessage.objects.create(session=session, sender="bot", message=reply)

    return JsonResponse({"reply": reply})

    # 🔹 Monta o prompt com contexto
    prompt = f"""
Você é o assistente virtual da CoderTec.
Responda de forma amigável, objetiva e em português, com base neste contexto:

{CODERTEC_CONTEXT}

Usuário: {user_message}
"""

    # 🔹 Requisição à API da OpenAI
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4o-mini",  # modelo rápido e barato
            "messages": [
                {"role": "system", "content": "Você é o assistente da CoderTec."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.6,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        # 🔹 Se algo der errado, mostra o erro
        if response.status_code != 200:
            print("❌ Erro OpenAI:", response.text)
            return JsonResponse({"reply": "Desculpe, ocorreu um erro ao acessar a IA."})

        data = response.json()
        answer = data["choices"][0]["message"]["content"].strip()

        return JsonResponse({"reply": answer})

    except Exception as e:
        print("❌ Falha OpenAI:", e)
        return JsonResponse({"reply": f"Erro ao acessar a IA: {e}"})


def gerar_resposta_contextual(msg, contexto):
    msg_lower = msg.lower()
    respostas = {
        "automacao": "Automatizamos relatórios, integrações e fluxos com IA.",
        "dashboards": "Criamos dashboards interativos em Power BI, Streamlit e Plotly.",
        "ciencia-de-dados": "Analisamos dados e aplicamos Machine Learning para gerar insights estratégicos.",
        "desenvolvimento-web": "Criamos sites, aplicação web completa, landing pages e muito mais",
        "geral": "Sou o assistente da CoderTec — posso te ajudar com sites, automações e IA."
    }

    if "preço" in msg_lower or "valor" in msg_lower:
        return "Cada projeto é personalizado 😊 posso entender sua necessidade para estimar um orçamento."
    return respostas.get(contexto, respostas["geral"])
