import sys
import joblib
import pandas as pd
from caracteristicas import extraer_caracteristicas

modelo = joblib.load("modelo.joblib")

def analizar_url(url):
    X = pd.DataFrame([extraer_caracteristicas(url)])
    prob = modelo.predict_proba(X)[0][1]
    if prob >= 0.7:
        veredicto = "PELIGROSA"
    elif prob >= 0.4:
        veredicto = "SOSPECHOSA"
    else:
        veredicto = "PARECE SEGURA"
    return prob, veredicto

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("URL: ")
    prob, veredicto = analizar_url(url)
    print(f"\nURL: {url}")
    print(f"Probabilidad de phishing: {prob:.0%}")
    print(f"Veredicto: {veredicto}")