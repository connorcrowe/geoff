import { useEffect, useRef } from "react"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";
const layerColours = ["#006045", "#d08700", "#57534d", "#0069a8"];
const HIGHLIGHT_COLOR = "#eab308"; // yellow-500

export default function MapView({ layers, selectedFeatureId, onFeatureClick }) {
  const mapContainer = useRef(null)
  const map = useRef(null)

  // Initialize map
  useEffect(() => {
    if (map.current) return // Initialize only once

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://tiles.openfreemap.org/styles/bright", 
      center: [-79.38, 43.65],
      zoom: 11
    })

  }, [])

  // Add/update layers
  useEffect(() => {
    if (!map.current) return

    const mapInstance = map.current

    // Wait for style to load before adding layers
    const addLayers = () => {
      // Remove old data layers and sources
      const existingLayers = mapInstance.getStyle().layers
      existingLayers.forEach(layer => {
        if (layer.id.includes('-fill') || layer.id.includes('-line') || layer.id.includes('-circle')) {
          if (mapInstance.getLayer(layer.id)) {
            mapInstance.removeLayer(layer.id)
          }
        }
      })

      const existingSources = Object.keys(mapInstance.getStyle().sources)
      existingSources.forEach(sourceId => {
        if (sourceId.match(/^[0-9a-f-]{36}$/)) { // UUID pattern
          if (mapInstance.getSource(sourceId)) {
            mapInstance.removeSource(sourceId)
          }
        }
      })

      // Add new layers
      layers.forEach((layer, i) => {
        if (!layer.tile_url) return

        const baseUrl = API_BASE || window.location.origin
        const tileUrl = layer.tile_url.startsWith('http') 
          ? layer.tile_url 
          : `${baseUrl}${layer.tile_url}`

        const colour = layerColours[i % layerColours.length]

        // Add source
        mapInstance.addSource(layer.layer_id, {
          type: "vector",
          tiles: [tileUrl],
          minzoom: 0,
          maxzoom: 22
        })

        // Add fill layer for polygons
        mapInstance.addLayer({
          id: `${layer.layer_id}-fill`,
          type: "fill",
          source: layer.layer_id,
          "source-layer": layer.name,
          filter: ["==", ["geometry-type"], "Polygon"],
          paint: {
            "fill-color": colour,
            "fill-opacity": 0.4
          }
        })

        // Add line layer
        mapInstance.addLayer({
          id: `${layer.layer_id}-line`,
          type: "line",
          source: layer.layer_id,
          "source-layer": layer.name,
          filter: ["in", ["geometry-type"], ["literal", ["LineString", "Polygon"]]],
          paint: {
            "line-color": colour,
            "line-width": 2
          }
        })

        // Add circle layer for points
        mapInstance.addLayer({
          id: `${layer.layer_id}-circle`,
          type: "circle",
          source: layer.layer_id,
          "source-layer": layer.name,
          filter: ["==", ["geometry-type"], "Point"],
          paint: {
            "circle-radius": 6,
            "circle-color": colour,
            "circle-stroke-width": 2,
            "circle-stroke-color": "#fff"
          }
        })

        // Handle clicks
        mapInstance.on("click", `${layer.layer_id}-fill`, (e) => {
          if (e.features && e.features[0]) {
            onFeatureClick(e.features[0].id)
          }
        })

        mapInstance.on("click", `${layer.layer_id}-line`, (e) => {
          if (e.features && e.features[0]) {
            onFeatureClick(e.features[0].id)
          }
        })

        mapInstance.on("click", `${layer.layer_id}-circle`, (e) => {
          if (e.features && e.features[0]) {
            onFeatureClick(e.features[0].id)
          }
        })

        // Cursor changes
        mapInstance.on("mouseenter", `${layer.layer_id}-fill`, () => {
          mapInstance.getCanvas().style.cursor = "pointer"
        })
        mapInstance.on("mouseleave", `${layer.layer_id}-fill`, () => {
          mapInstance.getCanvas().style.cursor = ""
        })

        mapInstance.on("mouseenter", `${layer.layer_id}-line`, () => {
          mapInstance.getCanvas().style.cursor = "pointer"
        })
        mapInstance.on("mouseleave", `${layer.layer_id}-line`, () => {
          mapInstance.getCanvas().style.cursor = ""
        })

        mapInstance.on("mouseenter", `${layer.layer_id}-circle`, () => {
          mapInstance.getCanvas().style.cursor = "pointer"
        })
        mapInstance.on("mouseleave", `${layer.layer_id}-circle`, () => {
          mapInstance.getCanvas().style.cursor = ""
        })
      })
    }

    if (mapInstance.isStyleLoaded()) {
      addLayers()
    } else {
      mapInstance.once("load", addLayers)
    }
  }, [layers, onFeatureClick])

  // Handle feature selection highlighting
  useEffect(() => {
    if (!map.current) return

    const mapInstance = map.current

    if (!mapInstance.isStyleLoaded()) return

    // Remove existing highlight layers
    const highlightLayers = ['highlight-fill', 'highlight-line', 'highlight-circle']
    highlightLayers.forEach(layerId => {
      if (mapInstance.getLayer(layerId)) {
        mapInstance.removeLayer(layerId)
      }
    })

    if (selectedFeatureId == null) return

    // Add highlight layers for the selected feature
    layers.forEach((layer) => {
      if (!layer.tile_url) return

      const sourceId = layer.layer_id

      // Add highlight fill layer for polygons
      if (!mapInstance.getLayer('highlight-fill')) {
        mapInstance.addLayer({
          id: 'highlight-fill',
          type: 'fill',
          source: sourceId,
          'source-layer': layer.name,
          filter: ['all',
            ['==', ['geometry-type'], 'Polygon'],
            ['==', ['id'], selectedFeatureId]
          ],
          paint: {
            'fill-color': HIGHLIGHT_COLOR,
            'fill-opacity': 0.6
          }
        })
      }

      // Add highlight line layer
      if (!mapInstance.getLayer('highlight-line')) {
        mapInstance.addLayer({
          id: 'highlight-line',
          type: 'line',
          source: sourceId,
          'source-layer': layer.name,
          filter: ['all',
            ['in', ['geometry-type'], ['literal', ['LineString', 'Polygon']]],
            ['==', ['id'], selectedFeatureId]
          ],
          paint: {
            'line-color': HIGHLIGHT_COLOR,
            'line-width': 3
          }
        })
      }

      // Add highlight circle layer for points
      if (!mapInstance.getLayer('highlight-circle')) {
        mapInstance.addLayer({
          id: 'highlight-circle',
          type: 'circle',
          source: sourceId,
          'source-layer': layer.name,
          filter: ['all',
            ['==', ['geometry-type'], 'Point'],
            ['==', ['id'], selectedFeatureId]
          ],
          paint: {
            'circle-radius': 8,
            'circle-color': HIGHLIGHT_COLOR,
            'circle-stroke-width': 3,
            'circle-stroke-color': '#fff'
          }
        })
      }
    })
  }, [selectedFeatureId, layers])

  return <div className="map" ref={mapContainer} style={{ width: "100%", height: "100%" }} />
}
