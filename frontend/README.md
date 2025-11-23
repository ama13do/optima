# Optima Frontend - React Application

Interfaz de usuario moderna construida con React, Vite y Tailwind CSS para interactuar con el sistema de análisis de datos Optima.

---

## 🎨 Tecnologías

- **React 19** - Librería UI moderna y eficiente
- **Vite** - Build tool ultra-rápido con HMR
- **Tailwind CSS** - Framework CSS utility-first
- **Axios** - Cliente HTTP para comunicación con API
- **Recharts** - Visualización de datos interactiva
- **Lucide React** - Iconos modernos y ligeros

---

## 🚀 Inicio Rápido

### Prerequisitos

- Node.js 18+ 
- npm o yarn
- Backend de Optima corriendo

### Instalación

```bash
# Instalar dependencias
npm install

# Modo desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview

# Linting
npm run lint
```

La aplicación estará disponible en: http://localhost:5173

---

## 📁 Estructura del Proyecto

```
frontend/
├── public/              # Assets estáticos
├── src/
│   ├── assets/         # Imágenes, iconos, etc.
│   ├── App.jsx         # Componente principal
│   ├── App.css         # Estilos del componente
│   ├── main.jsx        # Entry point
│   └── index.css       # Estilos globales + Tailwind
├── index.html          # HTML base
├── vite.config.js      # Configuración de Vite
├── tailwind.config.js  # Configuración de Tailwind
├── postcss.config.js   # PostCSS para Tailwind
├── eslint.config.js    # Configuración ESLint
└── package.json        # Dependencias y scripts
```

---

## 🎯 Características Principales

### 1. 📤 Upload de Archivos Multimodal

```jsx
// Soporta múltiples tipos de archivo
const fileTypes = [
  'image/*',
  'application/pdf',
  'text/csv',
  'application/json',
  'audio/*'
];
```

**Funcionalidad:**
- Drag & drop de archivos
- Selección múltiple
- Preview de archivos
- Validación de tipos

### 2. 🔍 Análisis de Datos

**Modos de análisis:**
- **Quick Check**: Análisis rápido con Gemini Flash
- **Deep Analysis**: Análisis exhaustivo con Gemini Pro
- **Bias Detection**: Detección de sesgos
- **Batch Processing**: Análisis de múltiples archivos

### 3. 🎙️ Interfaz de Voz

**Text-to-Speech:**
```jsx
const handleSpeak = async (text) => {
  const response = await axios.post(
    'http://localhost:8000/speak',
    { text },
    { responseType: 'blob' }
  );
  
  const audioUrl = URL.createObjectURL(response.data);
  const audio = new Audio(audioUrl);
  audio.play();
};
```

**Speech-to-Text:**
- Grabación de audio en navegador
- Transcripción automática con Gemini
- Feedback visual del proceso

### 4. 📊 Visualización de Resultados

**Gráficos interactivos:**
```jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

<BarChart data={metricsData}>
  <Bar dataKey="quality" fill="#10b981" />
  <Bar dataKey="bias" fill="#ef4444" />
</BarChart>
```

**Métricas mostradas:**
- Calidad de datos (0-100%)
- Nivel de sesgo detectado
- Usabilidad para IA
- Recomendaciones

### 5. 🎨 UI/UX Moderna

**Características de diseño:**
- Dark mode elegante
- Animaciones suaves
- Responsive design
- Sidebar colapsable
- Modals informativos
- Loading states

---

## 🔧 Configuración

### Configuración del Backend

Editar la URL del backend en `App.jsx`:

```jsx
const API_BASE_URL = 'http://localhost:8000';
// O para producción:
// const API_BASE_URL = 'http://45.77.163.127:8000';
```

### Variables de Entorno (Opcional)

Crear `.env` en la raíz del frontend:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Optima - Data Curator
```

Usar en el código:

```jsx
const API_URL = import.meta.env.VITE_API_URL;
```

---

## 🎨 Personalización de Estilos

### Tailwind Config

Modificar `tailwind.config.js`:

```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#10b981',
        secondary: '#3b82f6',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

### Clases Personalizadas

En `index.css`:

```css
@layer components {
  .btn-primary {
    @apply bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg;
  }
  
  .card {
    @apply bg-gray-800 rounded-xl p-6 shadow-xl;
  }
}
```

---

## 📱 Componentes Principales

### App.jsx

Componente principal con toda la lógica:

```jsx
function App() {
  // Estados
  const [files, setFiles] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [activeSection, setActiveSection] = useState('analisis');
  
  // Funciones
  const handleUpload = async () => { /* ... */ };
  const handleSpeak = async (text) => { /* ... */ };
  
  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar />
      <MainContent />
    </div>
  );
}
```

### Secciones

1. **Análisis**: Upload y procesamiento de archivos
2. **Voz**: Text-to-Speech interactivo
3. **Resultados**: Visualización de análisis previos
4. **Estadísticas**: Dashboard con métricas

---

## 🚀 Deployment

### Build para Producción

```bash
npm run build
```

Esto genera la carpeta `dist/` con archivos optimizados.

### Deploy en Vultr

**Opción 1: Servir con Node.js**

```bash
# En el servidor Vultr
cd /var/www/optima/frontend
npm install
npm run build

# Servir con servidor estático
npm install -g serve
serve -s dist -l 80
```

**Opción 2: Nginx**

```nginx
server {
    listen 80;
    server_name tortadetamal.fit;
    
    root /var/www/optima/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy al backend
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Opción 3: Docker**

```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Deploy en GoDaddy con Vultr

1. **Configurar DNS en GoDaddy:**
   - Tipo A: `@` → `45.77.163.127`
   - Tipo A: `www` → `45.77.163.127`

2. **Configurar servidor:**
```bash
# Instalar nginx
sudo apt update
sudo apt install nginx

# Copiar build
sudo cp -r dist/* /var/www/html/

# Reiniciar nginx
sudo systemctl restart nginx
```

---

## 🎨 Componentes de UI

### Button Component

```jsx
const Button = ({ children, variant = 'primary', onClick, loading }) => (
  <button
    onClick={onClick}
    disabled={loading}
    className={`
      px-6 py-3 rounded-lg font-semibold transition-all
      ${variant === 'primary' && 'bg-emerald-500 hover:bg-emerald-600'}
      ${variant === 'secondary' && 'bg-blue-500 hover:bg-blue-600'}
      ${loading && 'opacity-50 cursor-not-allowed'}
    `}
  >
    {loading ? <Loader2 className="animate-spin" /> : children}
  </button>
);
```

### Card Component

```jsx
const Card = ({ title, children, icon: Icon }) => (
  <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
    {Icon && <Icon className="text-emerald-400 mb-4" size={32} />}
    {title && <h3 className="text-xl font-bold mb-4">{title}</h3>}
    {children}
  </div>
);
```

### FileUpload Component

```jsx
const FileUpload = ({ onFileSelect, multiple = true }) => (
  <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center">
    <Upload className="mx-auto mb-4 text-gray-400" size={48} />
    <input
      type="file"
      multiple={multiple}
      onChange={onFileSelect}
      className="hidden"
      id="file-upload"
    />
    <label htmlFor="file-upload" className="cursor-pointer">
      Click para subir archivos
    </label>
  </div>
);
```

---

## 🧪 Testing

### Testing Manual

```bash
# Iniciar dev server
npm run dev

# Probar funcionalidades:
# 1. Upload de archivos
# 2. Análisis de datos
# 3. Text-to-Speech
# 4. Visualización de resultados
```

### Testing Automatizado (Opcional)

```bash
# Instalar Vitest
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Agregar script en package.json
"scripts": {
  "test": "vitest"
}
```

**Ejemplo de test:**

```jsx
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders upload section', () => {
  render(<App />);
  const uploadButton = screen.getByText(/subir/i);
  expect(uploadButton).toBeInTheDocument();
});
```

---

## 📊 Performance

### Optimizaciones Implementadas

1. **Lazy Loading de Componentes**
```jsx
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

2. **Memoización**
```jsx
const expensiveCalculation = useMemo(() => 
  calculateMetrics(data), 
  [data]
);
```

3. **Debouncing de Inputs**
```jsx
const debouncedSearch = useDebounce(searchTerm, 500);
```

### Métricas de Build

```bash
npm run build

# Output típico:
# dist/index.html                   0.5 kB
# dist/assets/index-abc123.css      15 kB
# dist/assets/index-xyz789.js       142 kB
```

---

## 🐛 Troubleshooting

### Error: CORS

Si ves errores CORS en consola:

```js
// Verificar que el backend tenga CORS habilitado
// En backend/main.py debe existir:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: Module not found

```bash
# Limpiar cache y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Error: Vite build falla

```bash
# Verificar versión de Node
node --version  # Debe ser 18+

# Limpiar y rebuild
npm run clean  # Si existe el script
npm run build
```

---

## 🔗 Enlaces Útiles

- **Live Demo**: http://tortadetamal.fit/
- **API**: http://45.77.163.127:8000/docs
- **Vite Docs**: https://vitejs.dev/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Recharts**: https://recharts.org/

---

## 🎓 Recursos de Aprendizaje

- [React Hooks](https://react.dev/reference/react)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS Cheatsheet](https://tailwindcomponents.com/cheatsheet/)
- [Axios Documentation](https://axios-http.com/docs/intro)

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Desarrolla y prueba tus cambios
4. Commit: `git commit -m 'Add: nueva funcionalidad'`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Crea un Pull Request

### Guías de Estilo

- Usar componentes funcionales con hooks
- Seguir convenciones de Tailwind CSS
- Mantener componentes pequeños y reutilizables
- Comentar lógica compleja
- Usar nombres descriptivos para variables y funciones

---

**Construido con ❤️ usando React, Vite y Tailwind CSS**
