import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from caracteristicas import extraer_caracteristicas

COL_URL = "URL"
COL_ETIQUETA = "label"
ETIQUETA_PHISHING = 0   # en PhiUSIIL: 0 = phishing, 1 = legítima

df = pd.read_csv("dataset.csv")
df = df[[COL_URL, COL_ETIQUETA]].dropna().sample(20000, random_state=42)

print("Extrayendo características...")
X = pd.DataFrame([extraer_caracteristicas(u) for u in df[COL_URL]])
y = (df[COL_ETIQUETA].values == ETIQUETA_PHISHING).astype(int)  # 1 = phishing

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

modelo = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
modelo.fit(X_train, y_train)

print(classification_report(y_test, modelo.predict(X_test),
                            target_names=["legítima", "phishing"]))
joblib.dump(modelo, "modelo.joblib")
print("Modelo guardado en modelo.joblib")