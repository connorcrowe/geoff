import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import L from "leaflet"
import { useEffect } from "react"

function GeoJsonLayer({ geojson, selectedFeatureId, onFeatureClick }) {
  const map = useMap()

  useEffect(() => {
    if (!geojson) return
    const geoJsonLayer = L.geoJSON(geojson, {
      style: (feature) => ({
        color: feature.id === selectedFeatureId ? "yellow" : "blue",
        weight: feature.id === selectedFeatureId ? 5 : 2,
      }),
      onEachFeature: (feature, layer) => {
        layer.on("click", () => onFeatureClick(feature.id))
      },
    }).addTo(map)

    if (selectedFeatureId != null) {
      const feature = geojson.features.find(f => f.id === selectedFeatureId)
      if (feature) {
        const bounds = L.geoJSON(feature).getBounds()
        map.fitBounds(bounds, { maxZoom: 17 })
      }
    }

    return () => {
      geoJsonLayer.remove()
    }
  }, [geojson, selectedFeatureId, onFeatureClick, map])

  return null
}

export default function MapView({ geojson, selectedFeatureId, onFeatureClick }) {
  return (
    <MapContainer center={[43.65, -79.38]} zoom={13} style={{ height: "100%", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap" />
      {geojson && <GeoJsonLayer geojson={geojson} selectedFeatureId={selectedFeatureId} onFeatureClick={onFeatureClick} />}
    </MapContainer>
  )
}
