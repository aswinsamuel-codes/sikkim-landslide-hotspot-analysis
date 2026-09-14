import React from 'react';
import { GeoJSON } from 'react-leaflet';
import L from 'leaflet';

export default function LayerManager({
  inventoryData,
  densityData,
  temporalData,
  layers,
  selectedYear,
  onSelectFeature
}) {
  if (!inventoryData) return null;

  // Custom marker for GE Points
  const pointToLayer = (feature, latlng) => {
    return L.circleMarker(latlng, {
      radius: 5,
      fillColor: '#eab308',
      color: '#000000',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.9
    });
  };

  // Feature click handler helper & Leaflet popup binding
  const onEachFeature = (layerName) => (feature, layer) => {
    const props = feature.properties || {};
    const featId = props.original_feature_id || props.FID || props.id || 'SK_FEAT';
    const obsYr = props.observation_year || props.Year || 'Active / Baseline';

    layer.bindPopup(`
      <div style="font-family: Inter, sans-serif; font-size: 12px; color: #f8fafc;">
        <strong style="color: #38bdf8; display: block; margin-bottom: 4px; font-size: 13px;">${layerName}</strong>
        <div><strong>Source ID:</strong> ${props.source_id || 'ZENODO_8169506'}</div>
        <div><strong>Feature ID:</strong> ${featId}</div>
        <div><strong>Obs Year:</strong> ${obsYr}</div>
        <div style="color: #94a3b8; font-size: 10px; margin-top: 4px; border-top: 1px solid #334155; padding-top: 4px;">
          Click feature for full provenance inspection
        </div>
      </div>
    `, {
      className: 'custom-leaflet-popup'
    });

    layer.on('click', (e) => {
      onSelectFeature({
        ...feature,
        properties: {
          ...feature.properties,
          layer_name: layerName
        }
      });
    });
  };


  // Styles
  const boundaryStyle = {
    color: '#e2e8f0',
    weight: 2.5,
    fillColor: '#1e293b',
    fillOpacity: 0.15
  };

  const extentStyle = {
    color: '#10b981',
    weight: 2,
    fillColor: '#10b981',
    fillOpacity: 0.1,
    dashArray: '4, 4'
  };

  const gePolyStyle = {
    color: '#f87171',
    weight: 1,
    fillColor: '#ef4444',
    fillOpacity: 0.5
  };

  const cartosatPolyStyle = {
    color: '#22d3ee',
    weight: 1,
    fillColor: '#06b6d4',
    fillOpacity: 0.6
  };

  const cartosatUnionStyle = {
    color: '#facc15',
    weight: 2,
    fillColor: 'transparent',
    fillOpacity: 0,
    dashArray: '5, 5'
  };

  // Density Grid styling
  const densityStyle = (feature) => {
    const density = feature.properties.centroid_assigned_inventory_feature_density_per_km2 || 0;
    let fillColor = '#0f172a';
    let fillOpacity = 0.1;

    if (density > 0 && density <= 1) {
      fillColor = '#38bdf8';
      fillOpacity = 0.4;
    } else if (density > 1 && density <= 3) {
      fillColor = '#f59e0b';
      fillOpacity = 0.55;
    } else if (density > 3) {
      fillColor = '#ef4444';
      fillOpacity = 0.7;
    }

    return {
      color: '#334155',
      weight: 0.5,
      fillColor,
      fillOpacity
    };
  };

  // Coverage Grid styling
  const coverageStyle = (feature) => {
    const status = feature.properties.observation_status;
    let fillColor = '#1e293b';
    let fillOpacity = 0.2;

    if (status === 'OBSERVED') {
      fillColor = '#10b981';
      fillOpacity = 0.3;
    } else if (status === 'PARTIALLY_COVERED') {
      fillColor = '#f59e0b';
      fillOpacity = 0.3;
    } else if (status === 'DATA_NOT_HELD') {
      fillColor = '#0f172a';
      fillOpacity = 0.4;
    }

    return {
      color: '#475569',
      weight: 0.5,
      fillColor,
      fillOpacity
    };
  };

  // Temporal Layer Styling
  const temporalStyle = {
    color: '#38bdf8',
    weight: 1.5,
    fillColor: '#0284c7',
    fillOpacity: 0.6
  };

  return (
    <>
      {/* State Boundary */}
      {layers.boundary && inventoryData.sikkim_boundary && (
        <GeoJSON
          key="boundary"
          data={inventoryData.sikkim_boundary}
          style={boundaryStyle}
        />
      )}

      {/* Mapped Extent */}
      {layers.extent && inventoryData.mapped_extent && (
        <GeoJSON
          key="extent"
          data={inventoryData.mapped_extent}
          style={extentStyle}
          onEachFeature={onEachFeature('Mapped Observation Extent')}
        />
      )}

      {/* Observation Coverage Grid */}
      {layers.coverageGrid && densityData && (
        <GeoJSON
          key="coverage-grid"
          data={densityData}
          style={coverageStyle}
          onEachFeature={onEachFeature('Observation Coverage Grid')}
        />
      )}

      {/* Inventory Density Grid */}
      {layers.densityGrid && densityData && (
        <GeoJSON
          key="density-grid"
          data={densityData}
          style={densityStyle}
          onEachFeature={onEachFeature('Inventory Feature Density Grid')}
        />
      )}

      {/* GE Polygons */}
      {layers.gePolygons && inventoryData.ge_polygons && !selectedYear && (
        <GeoJSON
          key="ge-polygons"
          data={inventoryData.ge_polygons}
          style={gePolyStyle}
          onEachFeature={onEachFeature('Google Earth Landslide Polygon')}
        />
      )}

      {/* Cartosat Polygons */}
      {layers.cartosatPolygons && inventoryData.cartosat_polygons && !selectedYear && (
        <GeoJSON
          key="cartosat-polygons"
          data={inventoryData.cartosat_polygons}
          style={cartosatPolyStyle}
          onEachFeature={onEachFeature('Cartosat Landslide Polygon')}
        />
      )}

      {/* Cartosat Derived Unions */}
      {layers.cartosatDerivedUnions && inventoryData.cartosat_derived_unions && (
        <GeoJSON
          key="cartosat-unions"
          data={inventoryData.cartosat_derived_unions}
          style={cartosatUnionStyle}
          onEachFeature={onEachFeature('Cartosat Derived Scarp/Deposit Union')}
        />
      )}

      {/* GE Points */}
      {layers.gePoints && inventoryData.ge_points && !selectedYear && (
        <GeoJSON
          key="ge-points"
          data={inventoryData.ge_points}
          pointToLayer={pointToLayer}
          onEachFeature={onEachFeature('Google Earth Landslide Point')}
        />
      )}

      {/* Selected Observation Year Filter Layer */}
      {selectedYear && temporalData && (
        <GeoJSON
          key={`temporal-${selectedYear}`}
          data={temporalData}
          style={temporalStyle}
          pointToLayer={(feature, latlng) => L.circleMarker(latlng, {
            radius: 6,
            fillColor: '#38bdf8',
            color: '#000000',
            weight: 1,
            fillOpacity: 0.9
          })}
          onEachFeature={onEachFeature(`Zenodo ${selectedYear} Observation`)}
        />
      )}
    </>
  );
}
