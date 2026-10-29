import json
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

PROJECT_ID = "936b10d5-26de-4896-899c-13d69a46d77d"
URL = "https://us-south.ml.cloud.ibm.com"

with open("apikey.json") as f:
    datos = json.load(f)
API_KEY = datos.get("apikey") or datos.get("apiKey")

credenciales = Credentials(url=URL, api_key=API_KEY)

MODELOS = ["ibm/granite-4-h-small",
           "ibm/granite-3-3-8b-instruct",
           "ibm/granite-3-8b-instruct"]

for modelo_id in MODELOS:
    try:
        modelo = ModelInference(model_id=modelo_id,
                                credentials=credenciales,
                                project_id=PROJECT_ID)
        respuesta = modelo.chat(messages=[
            {"role": "user",
             "content": "Responde en una frase: ¿qué es el phishing?"}
        ])
        print("Modelo usado:", modelo_id)
        print(respuesta["choices"][0]["message"]["content"])
        break
    except Exception as e:
        print(f"{modelo_id} no funcionó: {str(e)[:150]}")