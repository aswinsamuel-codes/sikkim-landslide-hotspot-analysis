import React, { useState, useEffect } from 'react';
import Header from './components/ui/Header';
import DisclaimerBanner from './components/ui/DisclaimerBanner';
import LayerControlPanel from './components/ui/LayerControlPanel';
import TimelineControl from './components/ui/TimelineControl';
import FeatureInspector from './components/ui/FeatureInspector';
import InformationPanel from './components/ui/InformationPanel';
import MapView from './components/map/MapView';

import {
  fetchHealth,
  fetchInventoryFeatures,
  fetchTemporalYears,
  fetchTemporalLayer,
  fetchDensityGrid
} from './api/client';

export default function App() {
  const [health, setHealth] = useState(null);
  const [inventoryData, setInventoryData] = useState(null);
  const [densityData, setDensityData] = useState(null);
  const [temporalTimeline, setTemporalTimeline] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [temporalLayerData, setTemporalLayerData] = useState(null);
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [isInfoOpen, setIsInfoOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Active layer visibility toggles
  const [layers, setLayers] = useState({
    boundary: true,
    extent: true,
    gePolygons: true,
    gePoints: true,
    cartosatPolygons: true,
    cartosatDerivedUnions: true,
    densityGrid: false,
    coverageGrid: false,
  });

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true);
        const [healthRes, invRes, densityRes, tempTimelineRes] = await Promise.all([
          fetchHealth().catch(() => null),
          fetchInventoryFeatures(),
          fetchDensityGrid(),
          fetchTemporalYears(),
        ]);

        setHealth(healthRes);
        setInventoryData(invRes);
        setDensityData(densityRes);
        setTemporalTimeline(tempTimelineRes);
      } catch (err) {
        console.error('Error loading GIS data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadInitialData();
  }, []);

  // Handle year selection
  const handleSelectYear = async (year) => {
    if (selectedYear === year) {
      setSelectedYear(null);
      setTemporalLayerData(null);
      return;
    }

    try {
      setSelectedYear(year);
      const data = await fetchTemporalLayer(year);
      setTemporalLayerData(data);
    } catch (err) {
      console.warn(`Year ${year} fetch notice:`, err.message);
      setTemporalLayerData(null);
    }
  };

  const handleClearYear = () => {
    setSelectedYear(null);
    setTemporalLayerData(null);
  };

  const handleToggleLayer = (layerKey) => {
    setLayers((prev) => ({
      ...prev,
      [layerKey]: !prev[layerKey],
    }));
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-950">
      {/* Top Navigation Header */}
      <Header health={health} onOpenInfo={() => setIsInfoOpen(true)} />

      {/* Mandatory Disclaimer Banner */}
      <DisclaimerBanner />

      {/* Main Interactive Workspace */}
      <div className="flex-1 relative w-full h-full overflow-hidden">
        {/* Fullscreen Leaflet GIS Map */}
        {loading ? (
          <div className="w-full h-full flex items-center justify-center bg-slate-950 text-cyan-400 space-x-3 font-mono">
            <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
            <span>Loading Sikkim Baseline Spatial Layers...</span>
          </div>
        ) : error ? (
          <div className="w-full h-full flex items-center justify-center bg-slate-950 text-red-400 p-6 text-center">
            <div className="max-w-md p-6 glass-panel rounded-xl border border-red-500/40 space-y-3">
              <h3 className="font-bold text-lg text-red-300">Data Connection Error</h3>
              <p className="text-xs text-slate-300">{error}</p>
              <p className="text-[11px] text-slate-400">Ensure backend server is running on http://localhost:8000</p>
            </div>
          </div>
        ) : (
          <MapView
            inventoryData={inventoryData}
            densityData={densityData}
            temporalData={temporalLayerData}
            layers={layers}
            selectedYear={selectedYear}
            onSelectFeature={(feat) => setSelectedFeature(feat)}
          />
        )}

        {/* Floating Controls Overlay: Top Left Layer Control Panel */}
        <div className="absolute top-4 left-4 z-20">
          <LayerControlPanel
            layers={layers}
            onToggleLayer={handleToggleLayer}
          />
        </div>

        {/* Floating Controls Overlay: Top Right Feature Inspector */}
        {selectedFeature && (
          <div className="absolute top-4 right-4 z-20">
            <FeatureInspector
              feature={selectedFeature}
              onClose={() => setSelectedFeature(null)}
            />
          </div>
        )}

        {/* Floating Controls Overlay: Bottom Extensible 15-Year Timeline Slider */}
        <div className="absolute bottom-6 left-4 right-4 max-w-5xl mx-auto z-20">
          <TimelineControl
            timeline={temporalTimeline}
            selectedYear={selectedYear}
            onSelectYear={handleSelectYear}
            onClearYear={handleClearYear}
          />
        </div>
      </div>

      {/* Specification & Metrics Drawer Modal */}
      <InformationPanel
        isOpen={isInfoOpen}
        onClose={() => setIsInfoOpen(false)}
      />
    </div>
  );
}
