import { useState, useEffect } from "react"
import MapView from "./components/MapView"
import PromptBar from "./components/PromptBar"
import ResultsPanel from "./components/ResultsPanel"
import Chips from "./components/Chips"
import MoreInfoModal from "./components/MoreInfoModal"

const API_BASE = import.meta.env.VITE_API_BASE_URL || ""

export default function App() {
  const [query, setQuery] = useState("")
  const [geojson, setGeojson] = useState(null)
  const [rows, setRows] = useState([])
  const [columns, setColumns] = useState([])
  const [resultsSize, setResultsSize] = useState("normal") // "collapsed" | "normal" | "expanded"
  const [examples, setExamples] = useState([])
  const [selectedFeatureId, setSelectedFeatureId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [isModalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/examples`)
      .then((res) => res.json())
      .then((data) => setExamples(data))
  }, [])

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${API_BASE}/api/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: query }),
      })

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`)
      }

      const data = await res.json()

      if (!data.geojson || !data.columns) {
        throw new Error("Invalid response from backend")
      }

      // Ensure features exist
      const featuresWithId =
        data.geojson?.features?.map((f, i) => ({
          ...f,
          id: i, // attach synthetic id
          properties: { ...f.properties, _id: i }, // store also in properties for reference
        })) || []

      const geojsonWithIds = { ...data.geojson, features: featuresWithId }

      // Map rows to objects with the same id
      const mappedRows =
        data.rows?.map((r, i) =>
          Array.isArray(r)
            ? { id: i, ...Object.fromEntries(data.columns.map((col, j) => [col, r[j]])) }
            : { id: i, ...r }
        ) || []

      setGeojson(geojsonWithIds)
      setColumns(data.columns || [])
      setRows(mappedRows)
      setSelectedFeatureId(null) // reset selection
    } catch (err) {
      console.error(err)
      setError("Something went wrong. Try rephrasing your query or try again later.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-screen h-screen relative overflow-hidden">

      {/* More Info Modal */}
      <button
        onClick={() => setModalOpen(true)}
        className="absolute top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 z-20"
      >
        More Info
      </button>
      <MoreInfoModal isOpen={isModalOpen} onClose={() => setModalOpen(false)} />

      {/* Map */}
      <div className="absolute inset-0 z-0">
        <MapView
          geojson={geojson}
          selectedFeatureId={selectedFeatureId}
          onFeatureClick={setSelectedFeatureId}
        />
      </div>

      {/* Logo / Branding */}
      <div className="absolute top-3 left-12 z-50 flex flex-col items-start bg-gray-900 p-3 rounded-lg shadow-md space-y-1 text-white">
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
        <span className="text-xs font-bold italic text-white">The Geospatial Fact Finder</span>
        { /*<div className="flex items-center space-x-2 text-sm italic">
          <span>Connor Crowe |</span>
          <a
            href="https://github.com/connorcrowe/geoff"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-500 hover:underline"
          >
            GitHub
          </a>
        </div> */}
      </div>

      {/* Chips */}
      <div className="absolute bottom-4 w-full flex justify-center z-10">
        <Chips examples={examples} setQuery={setQuery} />
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
      <div className="absolute bottom-32 left-1/2 -translate-x-1/2 w-full flex justify-center z-20">
        <ResultsPanel
          rows={rows}
          columns={columns}
          resultsSize={resultsSize}
          setResultsSize={setResultsSize}
          selectedFeatureId={selectedFeatureId}
          onRowClick={setSelectedFeatureId}
        />
      </div>
    </div>
  )
}
