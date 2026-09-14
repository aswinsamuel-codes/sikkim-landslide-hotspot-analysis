import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import LayerManager from './LayerManager';

export default function MapView({
  inventoryData,
  densityData,
  temporalData,
  layers,
  selectedYear,
  onSelectFeature
}) {
  // Sikkim center coordinates: [27.60, 88.50]
  const sikkimCenter = [27.60, 88.50];

  return (
    <div className="w-full h-full relative z-10 bg-slate-950">
      <MapContainer
        center={sikkimCenter}
        zoom={9}
        minZoom={8}
        maxZoom={15}
        scrollWheelZoom={true}
        style={{ width: '100%', height: '100%' }}
        zoomControl={true}
      >
        {/* Esri World Dark Gray Basemap */}
        <TileLayer
          attribution='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
          maxZoom={16}
        />


        {/* Modular Layer Manager Component */}
        <LayerManager
          inventoryData={inventoryData}
          densityData={densityData}
          temporalData={temporalData}
          layers={layers}
          selectedYear={selectedYear}
          onSelectFeature={onSelectFeature}
        />
      </MapContainer>
    </div>
  );
}
