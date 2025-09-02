import { useState, useRef, useEffect } from "react"

export default function PromptBar({ query, setQuery, onSubmit, examples, loading, error }) {
  const [showExamples, setShowExamples] = useState(false)
  const [shuffledExamples, setShuffledExamples] = useState([])
  const containerRef = useRef(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setShowExamples(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleFocus = () => {
    // Shuffle examples each time input is focused
    const shuffled = [...examples].sort(() => Math.random() - 0.5)
    setShuffledExamples(shuffled)
    setShowExamples(true)
  }

  return (
    <div
      ref={containerRef}
      className="bg-gray-900 text-white px-4 py-2 rounded-2xl flex flex-col w-2/3 relative"
    >
      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={handleFocus}
          className={`bg-transparent outline-none flex-1 ${
            loading ? "text-gray-500" : "text-white" 
          }`}
          placeholder="Ask me about Toronto"
        />
        <button
          onClick={onSubmit}
          disabled={loading}
          className="flex items-center justify-center w-8 h-6"
        >
          {loading ? (
            <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
          ) : (
            "→"
          )}
        </button>
      </div>

      {/* Dropdown of examples */}
      {showExamples && (
        <div className="absolute bottom-full mb-2 left-0 right-0 bg-gray-800 rounded-xl shadow-lg p-2 max-h-48 overflow-y-auto z-20">
          {shuffledExamples.map((ex, i) => (
            <div
              key={i}
              onClick={() => {
                setQuery(ex.user_query)
                setShowExamples(false)
              }}
              className="px-3 py-2 hover:bg-gray-700 cursor-pointer rounded-md"
            >
              {ex.user_query}
            </div>
          ))}
        </div>
      )}

      {/* Error Indicator */}
      {error && (
        <div className="text-red-400 text-sm mt-2">
          {error}
        </div>
      )}
    </div>
  )
}
