import { useState, useEffect } from "react"
import MapView from "./components/MapView"
import PromptBar from "./components/PromptBar"
import ResultsPanel from "./components/ResultsPanel"
import Chips from "./components/Chips"
import MoreInfoModal from "./components/MoreInfoModal"

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

export default function App() {
  const [query, setQuery] = useState("");
  const [layers, setLayers] = useState([]);
  const [selectedLayerIndex, setSelectedLayerIndex] = useState(0);
  const [selectedFeatureId, setSelectedFeatureId] = useState(null);
  

  const [resultsSize, setResultsSize] = useState("normal"); // "collapsed" | "normal" | "expanded"
  const [examples, setExamples] = useState([]);
  const [schemas, setSchemas] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isModalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/examples`)
      .then((res) => res.json())
      .then((data) => setExamples(data))
  }, []);

  useEffect(() => {
  fetch(`${API_BASE}/api/schemas`)
    .then((res) => res.json())
    .then((data) => setSchemas(data));
}, []);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/api/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: query }),
      });

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const data = await res.json()

      if (!data.layers || !Array.isArray(data.layers)) {
        throw new Error("Invalid response: no layers found");
      }

      const layersWithIds = data.layers.map((layer, layerIdx) => {
        const featuresWithId = layer.geojson?.features?.map((f, i) => ({
          ...f,
          id: `${layerIdx}-${i}`, // unique cross-layer id
          properties: { ...f.properties, _id: `${layerIdx}-${i}` },
        })) || [];

        const mappedRows = layer.rows?.map((r, i) => ({
          id: `${layerIdx}-${i}`,
          ...Object.fromEntries(layer.columns.map((c, j) => [c, r[j]]))
        })) || [];

        return {
          ...layer,
          geojson: { ...layer.geojson, features: featuresWithId },
          rows: mappedRows,
        }
      })

      setLayers(layersWithIds);
      setSelectedLayerIndex(0);
      setSelectedFeatureId(null);
    
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Try rephrasing your query or try again later.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-screen h-screen relative overflow-hidden">

      {/* More Info Modal */}
      <button
        onClick={() => setModalOpen(true)}
        className="absolute top-4 right-4 bg-emerald-900/90 text-white px-4 py-2 rounded hover:bg-blue-700 z-20"
      >
        More Info
      </button>
      <MoreInfoModal schemas = {schemas} isOpen={isModalOpen} onClose={() => setModalOpen(false)} />

      {/* Map */}
      <div className="absolute inset-0 z-0">
        <MapView
          layers={layers}
          selectedFeatureId={selectedFeatureId}
          onFeatureClick={setSelectedFeatureId}
        />
      </div>

      {/* Logo / Branding */}
      <div className="absolute top-3 left-12 z-50 flex flex-col items-start bg-zinc-800 p-3 rounded-lg shadow-md space-y-1 text-white">
        <div className="flex items-center space-x-2">
          {/* Tiny map pin icon */}
          <svg
            className="w-5 h-5 text-white"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5s2.5 1.12 2.5 2.5S13.38 11.5 12 11.5z"/>
          </svg>
          <span className="text-xl font-bold text-white">GEOFF</span>
        </div>
        <span className="text-xs font-bold italic text-white text-emerald-400">The Geospatial Fact Finder</span>
      </div>

      {/* Dataset Buttons */}
      <div className="absolute bottom-4 w-full flex justify-center z-50">
        <Chips schemas={schemas} setQuery={setQuery} />
      </div>

      {/* Prompt Bar */}
      <div className="absolute bottom-16 w-full flex justify-center z-30">
        <PromptBar
          query={query}
          setQuery={setQuery}
          onSubmit={handleSubmit}
          examples={examples}
          loading={loading}
          error={error}
        />
      </div>

      {/* Results Panel*/}
      <div className="absolute bottom-28 left-1/2 -translate-x-1/2 w-full flex justify-center z-20">
        <ResultsPanel
          layers={layers}
          resultsSize={resultsSize}
          setResultsSize={setResultsSize}
          selectedFeatureId={selectedFeatureId}
          onRowClick={setSelectedFeatureId}
        />
      </div>
    </div>
  )
}
