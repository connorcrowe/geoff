export default function Chips({ examples, setQuery }) {
  if (!examples || examples.length === 0) return null

  // build first-example lookup and labels
  const lookup = {}
  examples.forEach((ex) => {
    ex.tables.forEach((t) => {
      if (!lookup[t]) {
        lookup[t] = ex.user_query
      }
    })
  })

  const chipLabels = Object.keys(lookup).map((t) => ({
    table: t,
    label: t.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
  }))

  return (
    <div className="flex justify-center gap-2 w-full">
      {chipLabels.map(({ label, table }) => (
        <button
          key={table}
          onClick={() => setQuery(lookup[table])}
          className="bg-gray-700 text-white px-3 py-1 rounded-xl"
        >
          {label}
        </button>
      ))}
    </div>
  )
}