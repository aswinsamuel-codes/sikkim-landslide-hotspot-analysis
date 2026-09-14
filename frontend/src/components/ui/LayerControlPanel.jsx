import React from 'react';
import { Layers, Eye, EyeOff, MapPin, Grid, Shield, Calendar } from 'lucide-react';

export default function LayerControlPanel({ layers, onToggleLayer }) {
  return (
    <div className="w-80 glass-panel rounded-xl p-4 text-xs space-y-3 shadow-2xl border border-slate-800">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center space-x-2 text-slate-200 font-semibold">
          <Layers className="w-4 h-4 text-cyan-400" />
          <span>Interactive Layer Controls</span>
        </div>
        <span className="text-[10px] text-slate-400 font-mono">507 Baseline</span>
      </div>

      <div className="space-y-2">
        {/* State Boundary */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-slate-800/80 transition-all">
          <div className="flex items-center space-x-2.5">
            <div className="w-3 h-3 rounded-full border-2 border-slate-200 bg-slate-800"></div>
            <span className="text-slate-200 font-medium">State Boundary (GADM)</span>
          </div>
          <input
            type="checkbox"
            checked={layers.boundary}
            onChange={() => onToggleLayer('boundary')}
            className="w-4 h-4 accent-cyan-500 rounded cursor-pointer"
          />
        </label>

        {/* Mapped Extent */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-slate-800/80 transition-all">
          <div className="flex items-center space-x-2.5">
            <div className="w-3 h-3 rounded bg-emerald-500/40 border border-emerald-400"></div>
            <span className="text-slate-200 font-medium">Mapped Extent (~2,962 km²)</span>
          </div>
          <input
            type="checkbox"
            checked={layers.extent}
            onChange={() => onToggleLayer('extent')}
            className="w-4 h-4 accent-cyan-500 rounded cursor-pointer"
          />
        </label>

        {/* GE Polygons */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-slate-800/80 transition-all">
          <div className="flex items-center space-x-2.5">
            <div className="w-3 h-3 rounded bg-red-500/60 border border-red-400"></div>
            <div>
              <span className="text-slate-200 font-medium block">GE Landslide Polygons</span>
              <span className="text-[10px] text-slate-400">255 Primary Features</span>
            </div>
          </div>
          <input
            type="checkbox"
            checked={layers.gePolygons}
            onChange={() => onToggleLayer('gePolygons')}
            className="w-4 h-4 accent-cyan-500 rounded cursor-pointer"
          />
        </label>

        {/* GE Points */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-slate-800/80 transition-all">
          <div className="flex items-center space-x-2.5">
            <div className="w-3 h-3 rounded-full bg-yellow-400 border border-amber-600"></div>
            <div>
              <span className="text-slate-200 font-medium block">GE Landslide Points</span>
              <span className="text-[10px] text-slate-400">185 Primary Features</span>
            </div>
          </div>
          <input
            type="checkbox"
            checked={layers.gePoints}
            onChange={() => onToggleLayer('gePoints')}
            className="w-4 h-4 accent-cyan-500 rounded cursor-pointer"
          />
        </label>

        {/* Cartosat Polygons */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-slate-800/80 transition-all">
          <div className="flex items-center space-x-2.5">
            <div className="w-3 h-3 rounded bg-cyan-500/60 border border-cyan-400"></div>
            <div>
              <span className="text-slate-200 font-medium block">Cartosat Polygons</span>
              <span className="text-[10px] text-slate-400">67 Primary Features</span>
            </div>
          </div>
          <input
            type="checkbox"
            checked={layers.cartosatPolygons}
            onChange={() => onToggleLayer('cartosatPolygons')}
            className="w-4 h-4 accent-cyan-500 rounded cursor-pointer"
          />
        </label>

        {/* Cartosat Derived Unions */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-amber-500/30 transition-all">
          <div className="flex items-center space-x-2.5">
            <div className="w-3 h-3 rounded bg-yellow-500/20 border-2 border-dashed border-yellow-400"></div>
            <div>
              <span className="text-amber-200 font-medium block">Cartosat Derived Unions</span>
              <span className="text-[10px] text-amber-400/80">23 Derived Associations</span>
            </div>
          </div>
          <input
            type="checkbox"
            checked={layers.cartosatDerivedUnions}
            onChange={() => onToggleLayer('cartosatDerivedUnions')}
            className="w-4 h-4 accent-amber-500 rounded cursor-pointer"
          />
        </label>

        {/* Inventory Feature Density Grid */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-cyan-500/30 transition-all">
          <div className="flex items-center space-x-2.5">
            <Grid className="w-3.5 h-3.5 text-cyan-400" />
            <div>
              <span className="text-cyan-200 font-medium block">Inventory Feature Density</span>
              <span className="text-[10px] text-cyan-400/80">1 km² Centroid Grid</span>
            </div>
          </div>
          <input
            type="checkbox"
            checked={layers.densityGrid}
            onChange={() => onToggleLayer('densityGrid')}
            className="w-4 h-4 accent-cyan-500 rounded cursor-pointer"
          />
        </label>

        {/* Observation Coverage Map */}
        <label className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 cursor-pointer border border-emerald-500/30 transition-all">
          <div className="flex items-center space-x-2.5">
            <Shield className="w-3.5 h-3.5 text-emerald-400" />
            <div>
              <span className="text-emerald-200 font-medium block">Observation Coverage</span>
              <span className="text-[10px] text-emerald-400/80">OBSERVED / DATA_NOT_HELD</span>
            </div>
          </div>
          <input
            type="checkbox"
            checked={layers.coverageGrid}
            onChange={() => onToggleLayer('coverageGrid')}
            className="w-4 h-4 accent-emerald-500 rounded cursor-pointer"
          />
        </label>
      </div>

      <div className="text-[10px] text-slate-400 border-t border-slate-800 pt-2 leading-snug font-mono">
        Derived Cartosat unions (23) remain derived only and are EXCLUDED from inventory feature counts and density numerators.
      </div>
    </div>
  );
}
