\# Detector de estafas web (IA agéntica)



Proyecto del curso de IA agéntica de IBM SkillUp. Analiza una URL sin abrirla y dice si parece una página de phishing o estafa, explicando el motivo en español.



\## Cómo funciona



1\. `caracteristicas.py` extrae características del texto de la URL (longitud, HTTPS, guiones, IP, palabras sospechosas, etc.).

2\. Un modelo Random Forest (`entrenar.py`) calcula la probabilidad de phishing.

3\. Se contrasta con una lista de dominios confiables.

4\. watsonx.ai (modelo Granite) explica el veredicto en lenguaje sencillo.



\## Requisitos



\- Python 3

\- Cuenta de IBM Cloud con watsonx.ai y un servicio Watson Machine Learning asociado al proyecto



\## Instalación (cmd)



&#x20;   python -m venv venv

&#x20;   venv\\Scripts\\activate

&#x20;   pip install -r requirements.txt



\## Datos



Descarga el dataset PhiUSIIL Phishing URL del repositorio UCI Machine Learning y guárdalo como `dataset.csv` en esta carpeta.



\## Entrenar el modelo



&#x20;   python entrenar.py



\## Credenciales



1\. En IBM Cloud, ve a Administrar > Acceso (IAM) > Claves de API, crea una clave y descárgala como `apikey.json` en esta carpeta.

2\. En `agente.py` cambia `PROJECT\_ID` por el ID de tu proyecto de watsonx.



`apikey.json` está en `.gitignore`: no lo subas nunca a GitHub.



\## Uso



&#x20;   python agente.py "http://ejemplo.com"



\## Limitaciones



\- Solo analiza el texto de la URL, no el contenido de la página.

\- La lista de dominios confiables es fija y manual.

\- El modelo depende del dataset con el que se entrenó.

