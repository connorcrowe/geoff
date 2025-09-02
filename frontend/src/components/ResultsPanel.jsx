import { useEffect, useRef } from "react"

export default function ResultsPanel({ rows, columns, resultsSize, setResultsSize, selectedFeatureId, onRowClick }) {
  if (!rows || rows.length === 0) return null

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
      className={`bg-gray-800 text-white rounded-xl shadow-lg w-2/3 transition-all flex flex-col ${getResultsHeight()}`}
    >
      {/* Header Bar with title/buttons */}
      <div className="flex justify-between items-center bg-gray-900 px-4 py-2 rounded-t-xl border-b border-gray-700 flex-shrink-0">
        <h2 className="font-bold text-sm">{rows.length} Results</h2>
        <div className="space-x-2">
          <button onClick={() => setResultsSize("collapsed")} className="bg-gray-600 px-2 py-1 rounded text-xs">Collapse</button>
          <button onClick={() => setResultsSize("normal")} className="bg-gray-600 px-2 py-1 rounded text-xs">Normal</button>
          <button onClick={() => setResultsSize("expanded")} className="bg-gray-600 px-2 py-1 rounded text-xs">Expand</button>
        </div>
      </div>

      {/* Scrollable Table */}
      <div className="overflow-auto flex-1">
        <table className="min-w-full text-left text-sm border-collapse table-auto">
          <thead className="bg-gray-700 sticky top-0 z-5">
            <tr>
              {columns.map((col) => (
                <th key={col} className="px-3 py-1 border-b border-gray-600">{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.id}
                ref={(el) => (rowRefs.current[row.id] = el)}
                className={`cursor-pointer ${
                  row.id === selectedFeatureId
                    ? "bg-yellow-600"
                    : row.id % 2 === 0
                    ? "bg-gray-800"
                    : "bg-gray-700"
                }`}
                onClick={() => onRowClick(row.id)}
              >
                {columns.map((col) => (
                  <td key={col} className="px-3 py-1 border-b border-gray-600">
                    {row[col]?.toString() || ""}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
