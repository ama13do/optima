import { useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import {
  Upload,
  FileText,
  CheckCircle,
  AlertTriangle,
  Loader2,
  Volume2,
  Activity,
  Home,
  Cpu,
  MessageSquare,
  Download,
  Eye,
  X,
  Menu,
} from "lucide-react";

function App() {
  // --- ESTADOS ---
  const [files, setFiles] = useState(null);
  const [prompt, setPrompt] = useState(
    "Analiza la calidad de estos datos, detecta si hay sesgos de género/raza y dime si sirven para entrenar una IA."
  );
  const [loading, setLoading] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [results, setResults] = useState([]);
  const [activeSection, setActiveSection] = useState("analisis");
  const [showJsonModal, setShowJsonModal] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // --- 1. SUBIR ARCHIVOS A VULTR + GEMINI ---
  const handleUpload = async () => {
    if (!files) return alert("⚠️ Por favor selecciona archivos primero.");

    setLoading(true);
    const formData = new FormData();
    formData.append("prompt", prompt);

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      const response = await axios.post(
        "http://45.77.163.127:8000/analyze-batch",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResults(response.data.results);
    } catch (error) {
      console.error(error);
      alert(
        "❌ Error de conexión. Asegúrate que el backend (pantalla negra) esté corriendo."
      );
    } finally {
      setLoading(false);
    }
  };

  // --- 2. GENERAR VOZ CON ELEVENLABS ---
  const handleSpeak = async (text) => {
    if (!text || speaking) return;
    setSpeaking(true);

    try {
      const response = await axios.post(
        "http://45.77.163.127:8000/speak",
        { text: text },
        { responseType: "blob" }
      );

      const audioUrl = window.URL.createObjectURL(new Blob([response.data]));
      const audio = new Audio(audioUrl);
      audio.play();

      audio.onended = () => setSpeaking(false);
    } catch (error) {
      console.error("Error reproduciendo audio:", error);
      setSpeaking(false);
    }
  };

  // --- 3. DESCARGAR JSON ---
  const handleDownloadJson = () => {
    const jsonStr = JSON.stringify(results, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `dataclean-results-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // --- MENÚ ITEMS ---
  const menuItems = [
    { id: "analisis", label: "Análisis", icon: Home },
    { id: "entrenar", label: "Entrenar", icon: Cpu },
    { id: "chatbot", label: "Chatbot", icon: MessageSquare },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500 selection:text-white flex">
      {/* SIDEBAR */}
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } bg-slate-900 border-r border-slate-800 transition-all duration-300 overflow-hidden flex-shrink-0`}
      >
        <div className="p-6 h-full flex flex-col">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-1">
              DataClean AI
            </h2>
            <p className="text-xs text-slate-500">Hackathon 2025</p>
          </div>

          <nav className="flex-1 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveSection(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                    activeSection === item.id
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-900/50"
                      : "text-slate-400 hover:bg-slate-800 hover:text-white"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="pt-6 border-t border-slate-800">
            <div className="bg-slate-800/50 rounded-xl p-4 text-xs text-slate-400">
              <p className="font-semibold text-white mb-1">Tech Stack</p>
              <p>Vultr • Gemini • ElevenLabs</p>
            </div>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-auto">
        <div className="p-6 md:p-10">
          {/* HEADER CON TOGGLE SIDEBAR */}
          <header className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 transition-colors"
              >
                <Menu className="w-5 h-5" />
              </button>

              {results.length > 0 && activeSection === "analisis" && (
                <div className="flex gap-2">
                  <button
                    onClick={() => setShowJsonModal(true)}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 transition-colors text-sm"
                  >
                    <Eye className="w-4 h-4" />
                    Ver JSON
                  </button>
                  <button
                    onClick={handleDownloadJson}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 transition-colors text-sm font-medium"
                  >
                    <Download className="w-4 h-4" />
                    Descargar
                  </button>
                </div>
              )}
            </div>

            <div className="text-center">
              <div className="inline-block p-2 px-4 rounded-full bg-blue-900/30 border border-blue-500/30 mb-4">
                <span className="text-xs font-bold text-blue-400 tracking-widest uppercase">
                  {menuItems.find((m) => m.id === activeSection)?.label}
                </span>
              </div>
              <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
                {activeSection === "analisis" && "Análisis de Datasets"}
                {activeSection === "entrenar" && "Entrenar Modelo IA"}
                {activeSection === "chatbot" && "Chatbot Inteligente"}
              </h1>
            </div>
          </header>

          {/* CONTENIDO SEGÚN SECCIÓN */}
          {activeSection === "analisis" && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* BARRA LATERAL (INPUTS) */}
              <div className="lg:col-span-4 space-y-6">
                <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-sm sticky top-6">
                  <div className="mb-6">
                    <label className="block text-sm font-bold mb-2 text-blue-300 uppercase tracking-wider">
                      1. Prompt del Ingeniero
                    </label>
                    <textarea
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl p-4 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition shadow-inner text-slate-300"
                      rows="4"
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                    />
                  </div>

                  <div className="mb-6">
                    <label className="block text-sm font-bold mb-2 text-blue-300 uppercase tracking-wider">
                      2. Dataset (Img/PDF)
                    </label>
                    <div className="border-2 border-dashed border-slate-700 rounded-xl p-8 text-center hover:bg-slate-800/50 hover:border-blue-500/50 transition cursor-pointer relative group bg-slate-950/50">
                      <input
                        type="file"
                        multiple
                        onChange={(e) => setFiles(e.target.files)}
                        className="absolute inset-0 opacity-0 cursor-pointer z-10"
                      />
                      <div className="group-hover:scale-110 transition-transform duration-200">
                        <Upload className="mx-auto h-10 w-10 text-slate-500 group-hover:text-blue-400 mb-3" />
                      </div>
                      <p className="text-sm text-slate-400 font-medium">
                        {files ? (
                          <span className="text-emerald-400 font-bold">
                            ✅ {files.length} archivos cargados
                          </span>
                        ) : (
                          "Arrastra o haz click aquí"
                        )}
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={handleUpload}
                    disabled={loading}
                    className={`w-full font-bold py-4 rounded-xl flex items-center justify-center transition-all shadow-lg transform active:scale-95
                      ${
                        loading
                          ? "bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700"
                          : "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-blue-900/20 border border-blue-500/20"
                      }
                    `}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="animate-spin mr-2 h-5 w-5" />
                        Procesando con Gemini...
                      </>
                    ) : (
                      <>
                        <span className="mr-2">🚀</span> Ejecutar Análisis
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* RESULTADOS */}
              <div className="lg:col-span-8 space-y-6">
                {results.length === 0 && !loading && (
                  <div className="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-slate-800 rounded-3xl bg-slate-900/30 text-slate-600 p-10">
                    <div className="bg-slate-900 p-6 rounded-full mb-4">
                      <Activity className="h-10 w-10 opacity-50" />
                    </div>
                    <p className="text-lg font-medium">
                      El panel de resultados aparecerá aquí
                    </p>
                    <p className="text-sm opacity-60">
                      Sube archivos para ver la magia de la IA
                    </p>
                  </div>
                )}

                {results.length > 0 && (
                  <>
                    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-sm">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold text-white flex items-center gap-2">
                          <Activity className="h-6 w-6 text-blue-500" />
                          Análisis de Datos
                        </h3>
                        <span className="text-xs bg-slate-800 px-3 py-1 rounded-full text-slate-400 border border-slate-700">
                          Powered by Recharts
                        </span>
                      </div>

                      <div className="w-full h-80">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={[
                              {
                                name: "Apto IA",
                                value: results.filter(
                                  (r) =>
                                    r.analysis?.usable_for_training === true
                                ).length,
                                color: "#10b981",
                              },
                              {
                                name: "Con Sesgos",
                                value: results.filter(
                                  (r) =>
                                    r.analysis?.biases &&
                                    r.analysis.biases !== "None"
                                ).length,
                                color: "#f59e0b",
                              },
                              {
                                name: "Baja Calidad",
                                value: results.filter((r) =>
                                  (r.analysis?.data_quality || "")
                                    .toString()
                                    .toLowerCase()
                                    .includes("baja")
                                ).length,
                                color: "#ef4444",
                              },
                            ]}
                            margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              stroke="#334155"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="name"
                              stroke="#64748b"
                              axisLine={false}
                              tickLine={false}
                              dy={10}
                            />
                            <YAxis
                              stroke="#64748b"
                              axisLine={false}
                              tickLine={false}
                              allowDecimals={false}
                            />
                            <Tooltip
                              contentStyle={{
                                backgroundColor: "#0f172a",
                                border: "1px solid #334155",
                                borderRadius: "12px",
                                color: "white",
                              }}
                              cursor={{ fill: "#1e293b", opacity: 0.5 }}
                            />
                            <Bar
                              dataKey="value"
                              radius={[8, 8, 0, 0]}
                              barSize={60}
                            >
                              {[
                                { color: "#10b981" },
                                { color: "#f59e0b" },
                                { color: "#ef4444" },
                              ].map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 gap-4">
                      {results.map((item, idx) => (
                        <div
                          key={idx}
                          className="group bg-slate-900 p-5 rounded-2xl border border-slate-800 hover:border-blue-500/50 transition-all duration-300 shadow-md hover:shadow-blue-900/10"
                        >
                          <div className="flex items-start gap-4">
                            <div className="h-12 w-12 rounded-xl bg-slate-800 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-900/20 transition-colors">
                              <FileText className="h-6 w-6 text-slate-400 group-hover:text-blue-400" />
                            </div>

                            <div className="flex-1 min-w-0">
                              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                                <h4
                                  className="font-bold text-white truncate pr-4"
                                  title={item.filename}
                                >
                                  {item.filename}
                                </h4>

                                <button
                                  onClick={() =>
                                    handleSpeak(
                                      `Archivo ${idx + 1}. ${
                                        item.analysis?.summary || "Sin datos"
                                      }. Calidad: ${item.analysis?.data_quality}`
                                    )
                                  }
                                  disabled={speaking}
                                  className="self-start sm:self-auto text-xs font-medium bg-indigo-500/10 hover:bg-indigo-500 text-indigo-300 hover:text-white px-4 py-2 rounded-full flex items-center gap-2 transition-all"
                                >
                                  <Volume2
                                    className={`w-3.5 h-3.5 ${
                                      speaking ? "animate-pulse" : ""
                                    }`}
                                  />
                                  {speaking ? "Escuchando..." : "Escuchar"}
                                </button>
                              </div>

                              <p className="text-sm text-slate-400 leading-relaxed mb-3">
                                {item.analysis?.summary || "Procesando..."}
                              </p>

                              <div className="flex flex-wrap gap-2">
                                {item.analysis?.usable_for_training ? (
                                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                    <CheckCircle className="w-3 h-3 mr-1.5" />
                                    Listo para Entreno
                                  </span>
                                ) : (
                                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/20">
                                    <AlertTriangle className="w-3 h-3 mr-1.5" />
                                    No apto
                                  </span>
                                )}

                                {item.analysis?.biases &&
                                  item.analysis.biases !== "None" && (
                                    <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
                                      ⚠️ Sesgo:{" "}
                                      {typeof item.analysis.biases === "string"
                                        ? item.analysis.biases.substring(
                                            0,
                                            20
                                          ) + "..."
                                        : "Detectado"}
                                    </span>
                                  )}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            </div>
          )}

          {/* SECCIÓN ENTRENAR */}
          {activeSection === "entrenar" && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-slate-900/80 p-8 rounded-2xl border border-slate-800 shadow-xl">
                <div className="text-center mb-8">
                  <div className="inline-block p-4 rounded-2xl bg-blue-900/30 mb-4">
                    <Cpu className="w-12 h-12 text-blue-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-2">
                    Entrenar Modelo de IA
                  </h2>
                  <p className="text-slate-400">
                    Configura y entrena tu modelo con los datos validados
                  </p>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-bold mb-2 text-blue-300 uppercase tracking-wider">
                      Tipo de Modelo
                    </label>
                    <select className="w-full bg-slate-950 border border-slate-700 rounded-xl p-4 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-300">
                      <option>Clasificación de Imágenes</option>
                      <option>Detección de Objetos</option>
                      <option>Procesamiento de Lenguaje Natural</option>
                      <option>Regresión</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-bold mb-2 text-blue-300 uppercase tracking-wider">
                      Épocas de Entrenamiento
                    </label>
                    <input
                      type="number"
                      defaultValue={100}
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl p-4 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-300"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-bold mb-2 text-blue-300 uppercase tracking-wider">
                      Tasa de Aprendizaje
                    </label>
                    <input
                      type="number"
                      step="0.001"
                      defaultValue={0.001}
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl p-4 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-300"
                    />
                  </div>

                  <button className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-4 rounded-xl flex items-center justify-center transition-all shadow-lg">
                    <Cpu className="w-5 h-5 mr-2" />
                    Iniciar Entrenamiento
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* SECCIÓN CHATBOT */}
          {activeSection === "chatbot" && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-slate-900/80 rounded-2xl border border-slate-800 shadow-xl overflow-hidden">
                <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white/20 rounded-lg">
                      <MessageSquare className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h2 className="text-xl font-bold text-white">
                        Asistente IA
                      </h2>
                      <p className="text-sm text-blue-100">
                        Pregunta sobre tus datasets
                      </p>
                    </div>
                  </div>
                </div>

                <div className="p-6 h-96 overflow-y-auto bg-slate-950/50">
                  <div className="space-y-4">
                    <div className="flex gap-3">
                      <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                        <MessageSquare className="w-4 h-4 text-white" />
                      </div>
                      <div className="bg-slate-800 rounded-2xl rounded-tl-none p-4 max-w-md">
                        <p className="text-sm text-slate-300">
                          ¡Hola! Soy tu asistente de análisis de datos. Puedo
                          ayudarte a entender tus datasets, detectar sesgos y
                          preparar datos para entrenamiento.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-slate-900/50 border-t border-slate-800">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Escribe tu pregunta..."
                      className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-slate-300"
                    />
                    <button className="px-6 py-3 bg-blue-600 hover:bg-blue-500 rounded-xl font-medium transition-colors">
                      Enviar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* MODAL JSON */}
      {showJsonModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 rounded-2xl border border-slate-800 max-w-4xl w-full max-h-[80vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between p-6 border-b border-slate-800">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Eye className="w-5 h-5 text-blue-400" />
                Resultados JSON
              </h3>
              <button
                onClick={() => setShowJsonModal(false)}
                className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-6 overflow-auto flex-1">
              <pre className="text-xs text-slate-300 bg-slate-950 p-4 rounded-xl overflow-x-auto">
                {JSON.stringify(results, null, 2)}
              </pre>
            </div>
            <div className="p-4 border-t border-slate-800 flex justify-end gap-2">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(
                    JSON.stringify(results, null, 2)
                  );
                  alert("✅ JSON copiado al portapapeles");
                }}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm"
              >
                Copiar
              </button>
              <button
                onClick={handleDownloadJson}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg transition-colors text-sm font-medium"
              >
                Descargar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;