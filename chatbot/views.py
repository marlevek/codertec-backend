import os
import json
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    # 🔸 Validação do JSON recebido
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except Exception:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not user_message:
        return JsonResponse({"error": "Mensagem vazia"}, status=400)

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
