import { useMap } from "react-leaflet"
import { useEffect, useRef } from "react"
import L from "leaflet"

export default function GeoJsonLayer({ geojson, selectedFeatureId, onFeatureClick }) {
  const map = useMap()
  const layerRef = useRef(null)

  const nonHighlightColour = "oklch(50.8% 0.118 165.612)";

  // Create layer once per geojson
  useEffect(() => {
    if (!geojson) return

    const geoLayer = L.geoJSON(geojson, {
      style: (feature) => ({
        color: feature.id === selectedFeatureId ? "yellow" : nonHighlightColour,
        weight: feature.id === selectedFeatureId ? 5 : 2,
      }),
      onEachFeature: (feature, layer) => {
        layer.on("click", () => onFeatureClick(feature.id))
      },
      pointToLayer: (feature, latlng) =>
        L.circleMarker(latlng, {
          radius: 6,
          color: feature.id === selectedFeatureId ? "yellow" : nonHighlightColour,
          weight: 2,
          fillOpacity: 0.7,
        }),
    }).addTo(map)

    layerRef.current = geoLayer

    return () => {
      geoLayer.remove()
    }
  }, [geojson, onFeatureClick, map])

  // Update highlight + zoom when selection changes
  useEffect(() => {
    if (!layerRef.current) return

    layerRef.current.eachLayer((layer) => {
      const feature = layer.feature
      if (!feature) return
      const isSelected = feature.id === selectedFeatureId

      // Style
      if (layer.setStyle) {
        layer.setStyle({
          color: isSelected ? "yellow" : nonHighlightColour,
          weight: isSelected ? 5 : 2,
        })
      }
      if (layer.setRadius) {
        layer.setStyle?.({
          color: isSelected ? "yellow" : nonHighlightColour,
          weight: 2,
        })
        layer.setRadius(isSelected ? 8 : 6)
      }

      // Zoom to only the selected feature
      if (isSelected) {
        const bounds = layer.getBounds?.()
        if (bounds?.isValid?.()) {
          map.fitBounds(bounds, { maxZoom: 17 })
        } else if (layer.getLatLng) {
          map.setView(layer.getLatLng(), 17)
        }
      }
    })
  }, [selectedFeatureId, map])

  return null
}
