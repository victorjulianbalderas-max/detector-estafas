import re
import tldextract
from urllib.parse import urlparse

PALABRAS_SOSPECHOSAS = ["login", "verify", "secure", "account", "update",
                        "banco", "premio", "gratis", "bloqueada", "urgente"]

def extraer_caracteristicas(url):
    # Quitamos el "www." para que el modelo no use ese atajo
    url = re.sub(r"^(https?://)www\.", r"\1", url.strip(), flags=re.IGNORECASE)

    parsed = urlparse(url)
    ext = tldextract.extract(url)
    dominio = parsed.netloc

    return {
        "longitud_url": len(url),
        "usa_https": int(parsed.scheme == "https"),
        "usa_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", dominio))),
        "num_guiones": dominio.count("-"),
        "num_subdominios": len(ext.subdomain.split(".")) if ext.subdomain else 0,
        "tiene_arroba": int("@" in url),
        "num_puntos": url.count("."),
        "palabras_sospechosas": sum(p in url.lower() for p in PALABRAS_SOSPECHOSAS),
    }

if __name__ == "__main__":
    for u in ["https://www.google.com",
              "http://192.168.1.5/login-verify-account.php",
              "http://banco-seguro-premio-gratis.xyz/update"]:
        print(u)
        print(extraer_caracteristicas(u))
        print()