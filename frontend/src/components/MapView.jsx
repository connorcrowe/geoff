import { LayersControl, MapContainer, TileLayer } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import GeoJsonLayer from "./GeoJsonLayer"

const layerColours = ["oklch(50.8% 0.118 165.612)", "oklch(50% 0.134 242.749)", "oklch(68.1% 0.162 75.834)", "oklch(44.4% 0.011 73.639)"];

export default function MapView({ layers, selectedFeatureId, onFeatureClick }) {
  return (
    <MapContainer center={[43.65, -79.38]} zoom={13} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap"
      />
      {layers.map((layer, i) => (
        <GeoJsonLayer
          key={i}
          geojson={layer.geojson}
          selectedFeatureId={selectedFeatureId}
          onFeatureClick={onFeatureClick}
          colour={layerColours[i % layerColours.length]}
        />
      ))}
    </MapContainer>
  )
}
