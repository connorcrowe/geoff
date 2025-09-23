import { useState, useEffect, useRef } from "react";

export default function Chips({ examples, setQuery }) {
  const [open, setOpen] = useState(false);
  const [showChips, setShowChips] = useState(true);
  const drawerRef = useRef();

  // Update whether to show chips based on screen width
  useEffect(() => {
    function updateChips() {
      const width = window.innerWidth;
      if (width < 640) setShowChips(false); // mobile: only button
      else setShowChips(true); // tablet/desktop: show chips
    }
    updateChips();
    window.addEventListener("resize", updateChips);
    return () => window.removeEventListener("resize", updateChips);
  }, []);

  // Close drawer if click outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (drawerRef.current && !drawerRef.current.contains(event.target)) {
        setOpen(false);
      }
    }
    if (open) document.addEventListener("mousedown", handleClickOutside);
    else document.removeEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  if (!examples || examples.length === 0) return null;

  // build first-example lookup and labels
  const lookup = {};
  examples.forEach((ex) => {
    ex.tables.forEach((t) => {
      if (!lookup[t]) lookup[t] = ex.user_query;
    });
  });

  const chipLabels = Object.keys(lookup).map((t) => ({
    table: t,
    label: t.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
  }));

  return (
    <>
      {/* Button + Chips */}
      <div className="flex items-center gap-2 overflow-x-auto no-scrollbar px-2">
        <button
          onClick={() => setOpen(true)}
          className="bg-emerald-900/90 text-white px-4 py-1 rounded-xl flex-shrink-0"
        >
          All Datasets
        </button>

        {showChips &&
          chipLabels.map(({ label, table }) => (
            <button
              key={table}
              onClick={() => setQuery(lookup[table])}
              className="bg-zinc-700 text-white px-3 py-1 rounded-xl text-s, hover:bg-zinc-600 flex-shrink-0"
            >
              {label}
            </button>
          ))}
      </div>

      {/* Bottom Sheet Drawer */}
      {open && (
        <div className="fixed inset-0 z-60 flex items-end bg-black bg-opacity-50">
          <div
            ref={drawerRef}
            className="bg-zinc-800 text-white w-full max-h-[60vh] rounded-t-2xl p-4 overflow-y-auto"
          >
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-lg font-bold">Datasets</h2>
              <button
                onClick={() => setOpen(false)}
                className="text-zinc-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {chipLabels.map(({ label, table }) => (
                <button
                  key={table}
                  onClick={() => {
                    setQuery(lookup[table]);
                    setOpen(false);
                  }}
                  className="bg-zinc-700 hover:bg-zinc-600 px-3 py-2 rounded-lg text-sm text-left"
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
