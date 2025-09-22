import { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || ""

export default function MoreInfoModal({ isOpen, onClose }) {
    const [schemas, setSchemas] = useState({});
    const [selectedDataset, setSelectedDataset] = useState(null);

    useEffect(() => {
        if (isOpen) {
            fetch(`${API_BASE}/api/schemas`)
                .then(res => res.json())
                .then(data => setSchemas(data));
        }
    }, [isOpen]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-gray-700 text-white w-11/12 md:w-3/4 lg:w-2/3 max-h-[80vh] rounded-lg p-6 overflow-y-auto flex flex-col">
            {/* Header */}
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">About Geoff</h2>
                <button onClick={onClose} className="text-gray-500 hover:text-gray-800">✕</button>
            </div>

            {/* Motivation / Description */}
            <p className="mb-4 text-sm">
                Geoff turns natural language questions into spatial SQL queries and mapped visualisations using an LLM. The goal is to bring faster answers to geospatial questions without requiring technical spatial sql knowledge.<br />
            </p>
            <div className="mb-4 flex gap-4 text-sm">
                <a href="https://github.com/connorcrowe/geoff" target="_blank" className="text-blue-400 hover:underline font-bold">GitHub Repo</a>
                <a href="https://github.com/connorcrowe/geoff/issues/new" target="_blank" className="text-blue-400 hover:underline font-bold">Request Feature/Dataset</a>
            </div>

            {/* Dataset Table */}
            <h2 className="text-xl font-bold">Datasets Available</h2>
            <p className="mb-4 text-sm">
                Geoff can try to answer questions relating to any field listed when clicking a dataset. Geoff can also answer questions about spatial relationships, like how large a neighbourhood is, or how far apart two parks are.
            </p>

            <div className="flex flex-col md:flex-row gap-4">
                {/* Dataset List */}
                <div className="text-sm md:w-1/3 w-full border-r pr-2 bg-gray-600">
                {Object.keys(schemas).map(dataset => (
                    <div
                    key={dataset}
                    className={`p-2 cursor-pointer rounded ${selectedDataset === dataset ? 'bg-blue-500' : ''}`}
                    onClick={() => setSelectedDataset(dataset)}
                    >
                    {dataset}
                    </div>
                ))}
                </div>

                {/* Dataset Fields */}
                <div className="text-sm flex-1 w-full bg-gray-600 p-2">
                {selectedDataset ? (
                    <table className="w-full text-sm">
                    <thead>
                        <tr className="text-left border-b">
                        <th className="pb-1">Field</th>
                        
                        <th className="pb-1">Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {schemas[selectedDataset].map(col => (
                        <tr key={col.name} className="border-b">
                            <td className="py-1">
                                {col.name}
                                <br />
                                <span className="text-gray-400 text-xs">{col.type}</span>
                            </td>
                            
                            <td className="py-1">{col.description}</td>
                        </tr>
                        ))}
                    </tbody>
                    </table>
                ) : (
                    <p className="text-gray-500">Select a dataset to see its fields</p>
                )}
                </div>
            </div>
            </div>
        </div>
    )
}