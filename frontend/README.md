# 💻 Optima Frontend (UI)

Interfaz de usuario moderna y reactiva construida para facilitar la auditoría de datos. Diseñada con un enfoque "Dark Mode" profesional para ingenieros de datos.

## 🌐 URLs de Producción

* **Production:** __http://tortadetamal.fit/__
* **Vultr:** __http://45.77.163.127__
* **API Backend:** __http://45.77.163.127:8000/docs__

---

## ✨ Características

* **Upload Drag & Drop:** Soporte para múltiples archivos simultáneos.
* **Visualización de Datos:** Gráficas en tiempo real con `Recharts`.
* **Voice Interaction:**
    * **Input:** Dictado por voz usando la Web Speech API nativa.
    * **Output:** Reproducción de audio streaming desde el backend.
* **Diseño Responsivo:** Construido con Tailwind CSS.

---

## 🛠️ Instalación

Asegúrate de tener Node.js instalado (v18+ recomendado).

1.  **Instalar dependencias:**
    ```bash
    npm install
    ```

2.  **Configuración de Conexión:**
    Verifica en `src/App.jsx` la URL del backend.
    * **Local:** `http://127.0.0.1:8000`
    * **Producción (Vultr):** `http://45.77.163.127:8000`

---

## 🚀 Ejecución

**Modo Desarrollo:**
```bash
npm run dev
```

Accede a **http://localhost:5173**

**Construir para Producción:**

Genera los archivos estáticos optimizados en la carpeta `dist/`.

```bash
npm run build
```

---

## 📦 Deploy (Despliegue)

Para subir los cambios al servidor Vultr (Nginx):

```bash
# Desde la carpeta frontend
npm run build
scp -r dist root@45.77.163.127:/var/www/html
```
