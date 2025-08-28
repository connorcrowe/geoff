import { useState, useEffect } from "react"
import MapView from "./components/MapView"
import PromptBar from "./components/PromptBar"
import ResultsPanel from "./components/ResultsPanel"

export default function App() {
  const [query, setQuery] = useState("")
  const [geojson, setGeojson] = useState(null)
  const [rows, setRows] = useState([])
  const [columns, setColumns] = useState([])
  const [resultsSize, setResultsSize] = useState("normal") // "collapsed" | "normal" | "expanded"
  const [examples, setExamples] = useState([])
  const [selectedFeatureId, setSelectedFeatureId] = useState(null)

  useEffect(() => {
    // prefetch once
    fetch("http://localhost:8000/examples")
      .then((res) => res.json())
      .then((data) => setExamples(data))
  }, [])

const handleSubmit = async () => {
  const res = await fetch("http://localhost:8000/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: query }),
  })
  const data = await res.json()

  // Ensure features exist
  const featuresWithId = data.geojson?.features?.map((f, i) => ({
    ...f,
    id: i, // attach synthetic id
    properties: { ...f.properties, _id: i }, // store also in properties for reference
  })) || []

  const geojsonWithIds = { ...data.geojson, features: featuresWithId }

  // Map rows to objects with the same id
  const mappedRows = data.rows?.map((r, i) =>
    Array.isArray(r)
      ? { id: i, ...Object.fromEntries(data.columns.map((col, j) => [col, r[j]])) }
      : { id: i, ...r }
  ) || []

  setGeojson(geojsonWithIds)
  setColumns(data.columns || [])
  setRows(mappedRows)
  setSelectedFeatureId(null) // reset selection
}

  return (
    <div className="w-screen h-screen relative">
      {/* Map */}
      <div className="absolute inset-0 z-0">
        <MapView
          geojson={geojson}
          selectedFeatureId={selectedFeatureId}
          onFeatureClick={setSelectedFeatureId}
        />
      </div>

      {/* Prompt Bar */}
      <div className="absolute bottom-4 w-full flex justify-center z-20">
        <PromptBar
          query={query}
          setQuery={setQuery}
          onSubmit={handleSubmit}
          examples={examples}
        />
      </div>

      {/* Chips */}
      <div className="absolute bottom-16 w-full flex justify-center gap-2 z-10">
        {["EMS Stations", "Bike lanes", "Fire stations", "Parks", "Police Stations", "Neighbourhoods", "Schools"].map((c) => (
          <button
            key={c}
            onClick={() => setQuery(c)}
            className="bg-gray-700 text-white px-3 py-1 rounded-xl"
          >
            {c}
          </button>
        ))}
      </div>

      {/* Results */}
      <ResultsPanel
        rows={rows}
        columns={columns}
        resultsSize={resultsSize}
        setResultsSize={setResultsSize}
        selectedFeatureId={selectedFeatureId}
        onRowClick={setSelectedFeatureId}
      />
    </div>
  )
}
