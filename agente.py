import json
import sys
import warnings
import joblib
import pandas as pd
import tldextract
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from caracteristicas import extraer_caracteristicas

warnings.filterwarnings("ignore")

PROJECT_ID = "936b10d5-26de-4896-899c-13d69a46d77d"
URL_SERVICIO = "https://us-south.ml.cloud.ibm.com"
MODELO_ID = "ibm/granite-4-h-small"

DOMINIOS_CONFIABLES = {"google.com", "github.com", "bbva.mx", "mercadolibre.com.mx",
                       "microsoft.com", "apple.com", "amazon.com", "wikipedia.org",
                       "uat.edu.mx", "ibm.com"}

clasificador = joblib.load("modelo.joblib")

with open("apikey.json") as f:
    datos = json.load(f)
API_KEY = datos.get("apikey") or datos.get("apiKey")

llm = ModelInference(model_id=MODELO_ID,
                     credentials=Credentials(url=URL_SERVICIO, api_key=API_KEY),
                     project_id=PROJECT_ID)


def analizar(url):
    # Agente 1: extrae características de la URL
    caracteristicas = extraer_caracteristicas(url)

    # Agente 2: el modelo de ML calcula la probabilidad de phishing
    prob = clasificador.predict_proba(pd.DataFrame([caracteristicas]))[0][1]

    # Agente 3: contrasta con la lista de dominios confiables
    ext = tldextract.extract(url)
    dominio = f"{ext.domain}.{ext.suffix}"
    confiable = dominio in DOMINIOS_CONFIABLES

    if confiable:
        veredicto = "SEGURA (dominio confiable)"
    elif prob >= 0.7:
        veredicto = "PELIGROSA"
    elif prob >= 0.4:
        veredicto = "SOSPECHOSA"
    else:
        veredicto = "PARECE SEGURA"

    # Agente 4: el LLM explica el resultado
    prompt = f"""Eres un asistente de ciberseguridad que ayuda a personas sin conocimientos técnicos.
Analizaste esta dirección web sin abrirla, solo por su texto:

URL: {url}
Probabilidad de phishing según el modelo: {prob:.0%}
Dominio en la lista de confiables: {"sí" if confiable else "no"}
Veredicto: {veredicto}
Características detectadas: {json.dumps(caracteristicas, ensure_ascii=False)}

Explica en español, en máximo 4 frases cortas, por qué se llegó a ese veredicto y qué debería hacer el usuario.
Usa solo los datos de arriba y no inventes información sobre la página. Aclara que el análisis se basó únicamente en la dirección."""

    respuesta = llm.chat(messages=[{"role": "user", "content": prompt}],
                         params={"max_tokens": 300})
    explicacion = respuesta["choices"][0]["message"]["content"]
    return prob, veredicto, explicacion


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("URL: ")
    prob, veredicto, explicacion = analizar(url)
    print(f"\nURL: {url}")
    print(f"Probabilidad de phishing: {prob:.0%}")
    print(f"Veredicto: {veredicto}")
    print(f"\nExplicación:\n{explicacion}")