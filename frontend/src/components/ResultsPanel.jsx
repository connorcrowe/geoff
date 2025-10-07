import { useState, useEffect, useRef } from "react"

export default function ResultsPanel({ layers, resultsSize, setResultsSize, selectedFeatureId, onRowClick }) {
  if (!layers || layers.length === 0) return null

  const [expandedLayers, setExpandedLayers] = useState(() =>
    Object.fromEntries(layers.map((l) => [l.name, true]))
  )

  const toggleLayer = (name) => {
    setExpandedLayers((prev) => ({ ...prev, [name]: !prev[name] }))
  }

  const rowRefs = useRef({})

  useEffect(() => {
    if (selectedFeatureId != null && rowRefs.current[selectedFeatureId]) {
      rowRefs.current[selectedFeatureId].scrollIntoView({
        behavior: "smooth",
        block: "center",
      })
    }
  }, [selectedFeatureId])

  const getResultsHeight = () => {
    switch (resultsSize) {
      case "collapsed": return "h-24"
      case "expanded": return "h-96"
      default: return "h-48"
    }
  }

    return (
    <div
      className={`bg-zinc-800 text-white rounded-xl shadow-lg w-11/12 sm:w-4/5 md:w-2/3 transition-all flex flex-col ${getResultsHeight()}`}
    >
      {/* Header */}
      <div className="flex justify-between items-center bg-zinc-900 px-4 py-2 rounded-t-xl border-b border-zinc-700 flex-shrink-0">
        <h2 className="font-bold text-xs md:text-sm">
          {layers.reduce((sum, l) => sum + l.rows.length, 0)} Results across {layers.length} layers
        </h2>
        <div className="space-x-2">
          <button onClick={() => setResultsSize("collapsed")} className="bg-zinc-600 px-2 py-1 rounded text-xs">Collapse</button>
          <button onClick={() => setResultsSize("normal")} className="bg-zinc-600 px-2 py-1 rounded text-xs">Normal</button>
          <button onClick={() => setResultsSize("expanded")} className="bg-zinc-600 px-2 py-1 rounded text-xs">Expand</button>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="overflow-auto flex-1 divide-y divide-zinc-700">
        {layers.map((layer) => (
          <div key={layer.name}>
            {/* Layer header */}
            <div
              className="flex justify-between items-center bg-zinc-700 px-3 py-2 cursor-pointer hover:bg-zinc-600"
              onClick={() => toggleLayer(layer.name)}
            >
              <span className="font-semibold text-xs md:text-sm">
                {layer.name} ({layer.rows.length})
              </span>
              <span className="text-xs">{expandedLayers[layer.name] ? "▼" : "▶"}</span>
            </div>

            {/* Table */}
            {expandedLayers[layer.name] && (
              <div className="overflow-auto max-h-64">
                <table className="min-w-full text-left text-xs md:text-sm border-collapse table-auto">
                  <thead className="bg-zinc-700 sticky top-0 z-5">
                    <tr>
                      {layer.columns.map((col) => (
                        <th key={col} className="px-3 py-1 border-b border-zinc-600">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {layer.rows.map((row) => (
                      <tr
                        key={row.id}
                        ref={(el) => (rowRefs.current[row.id] = el)}
                        className={`cursor-pointer ${
                          row.id === selectedFeatureId
                            ? "bg-yellow-600"
                            : row.id % 2 === 0
                            ? "bg-zinc-800"
                            : "bg-zinc-700"
                        }`}
                        onClick={() => onRowClick(row.id)}
                      >
                        {layer.columns.map((col) => (
                          <td key={col} className="px-3 py-1 border-b border-zinc-600">
                            {row[col]?.toString() || ""}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
