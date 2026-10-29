from flask import Flask, request, jsonify
from agente import analizar

app = Flask(__name__)

PAGINA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Detector de estafas web</title>
<style>
  body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0;
         margin: 0; padding: 40px 16px; }
  .caja { max-width: 700px; margin: 0 auto; }
  h1 { margin-bottom: 4px; }
  p.sub { color: #94a3b8; margin-top: 0; }
  input { width: 100%; box-sizing: border-box; padding: 14px; font-size: 16px;
          border-radius: 8px; border: 1px solid #334155; background: #1e293b;
          color: #e2e8f0; }
  button { margin-top: 12px; padding: 12px 24px; font-size: 16px; border: 0;
           border-radius: 8px; background: #2563eb; color: white; cursor: pointer; }
  button:disabled { background: #475569; cursor: wait; }
  #resultado { margin-top: 24px; padding: 20px; border-radius: 10px;
               background: #1e293b; display: none; }
  .veredicto { font-size: 22px; font-weight: bold; margin: 0 0 8px 0; }
  .verde { color: #4ade80; } .amarillo { color: #facc15; } .rojo { color: #f87171; }
  #explicacion { line-height: 1.5; white-space: pre-wrap; }
  small { color: #94a3b8; }
</style>
</head>
<body>
<div class="caja">
  <h1>Detector de estafas web</h1>
  <p class="sub">Pega un enlace sospechoso. Se analiza solo su texto, sin abrir la página.</p>
  <input id="url" type="text" placeholder="https://ejemplo.com/pagina">
  <button id="boton" onclick="enviar()">Analizar</button>
  <div id="resultado">
    <p id="veredicto" class="veredicto"></p>
    <p id="prob"></p>
    <p id="explicacion"></p>
  </div>
  <p><small>Proyecto del curso de IA agéntica de IBM. Es una ayuda, no una garantía.</small></p>
</div>
<script>
async function enviar() {
  const url = document.getElementById("url").value.trim();
  const boton = document.getElementById("boton");
  const caja = document.getElementById("resultado");
  if (!url) { return; }
  boton.disabled = true;
  boton.textContent = "Analizando...";
  try {
    const r = await fetch("/analizar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    const d = await r.json();
    const v = document.getElementById("veredicto");
    caja.style.display = "block";
    if (d.error) {
      v.className = "veredicto rojo";
      v.textContent = d.error;
      document.getElementById("prob").textContent = "";
      document.getElementById("explicacion").textContent = "";
    } else {
      let color = "verde";
      if (d.veredicto.includes("PELIGROSA")) { color = "rojo"; }
      else if (d.veredicto.includes("SOSPECHOSA")) { color = "amarillo"; }
      v.className = "veredicto " + color;
      v.textContent = d.veredicto;
      document.getElementById("prob").textContent =
        "Probabilidad de phishing: " + d.probabilidad + "%";
      document.getElementById("explicacion").textContent = d.explicacion;
    }
  } catch (e) {
    caja.style.display = "block";
    document.getElementById("veredicto").textContent = "Error de conexión.";
  }
  boton.disabled = false;
  boton.textContent = "Analizar";
}
document.getElementById("url").addEventListener("keydown", function (e) {
  if (e.key === "Enter") { enviar(); }
});
</script>
</body>
</html>"""


@app.route("/")
def inicio():
    return PAGINA


@app.route("/analizar", methods=["POST"])
def ruta_analizar():
    datos = request.get_json(silent=True) or {}
    url = str(datos.get("url", "")).strip()
    if not url:
        return jsonify({"error": "Escribe una URL."}), 400
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    try:
        prob, veredicto, explicacion = analizar(url)
    except Exception:
        return jsonify({"error": "No se pudo analizar la URL. Intenta de nuevo."}), 500
    return jsonify({"probabilidad": round(prob * 100),
                    "veredicto": veredicto,
                    "explicacion": explicacion})


if __name__ == "__main__":
    app.run(debug=False)