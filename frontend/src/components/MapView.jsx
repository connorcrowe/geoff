import { MapContainer, TileLayer } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import GeoJsonLayer from "./GeoJsonLayer"

export default function MapView({ geojson, selectedFeatureId, onFeatureClick }) {
  return (
    <MapContainer center={[43.65, -79.38]} zoom={13} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap"
      />
      {geojson && (
        <GeoJsonLayer
          geojson={geojson}
          selectedFeatureId={selectedFeatureId}
          onFeatureClick={onFeatureClick}
        />
      )}
    </MapContainer>
  )
}
