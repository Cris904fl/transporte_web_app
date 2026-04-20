# 🌾 Problema de Transporte de Grano
## Colombia → Europa del Este | Aplicación Web en Python + Flask

---

## ▶ Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciar el servidor
```bash
python app.py
```

### 3. Abrir en el navegador
```
http://localhost:5000
```

---

## 📁 Estructura del proyecto
```
transporte_app/
├── app.py              ← Servidor Flask + algoritmo de Vogel
├── requirements.txt    ← Dependencias Python
├── README.md
└── templates/
    └── index.html      ← Página web interactiva (HTML + CSS + JS)
```

---

## 🧠 Funcionalidades

| Pestaña | Descripción |
|---------|-------------|
| 📋 Datos | Edita oferta, demanda y costos en tiempo real |
| ⚙️ Solución | Método de Vogel paso a paso + tabla de resultados |
| 🌐 Red de flujos | Visualización gráfica (canvas) de las rutas activas |
| ⚠️ Escasez | Simulador con slider + 3 criterios de distribución |
| 🧠 Habilidades | Competencias cognitivas y procedimiento metodológico |

---

## 📐 Tecnologías usadas

- **Python** — lógica del algoritmo de Vogel
- **Flask** — servidor web y API REST (`/resolver`, `/escasez`)
- **HTML/CSS/JavaScript** — interfaz interactiva
- **Canvas API** — visualización de la red de distribución

---

## 🔧 Personalización

Edita los datos iniciales en `app.py` o directamente en la interfaz web.
Los valores son completamente editables sin tocar el código.
