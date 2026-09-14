import React from 'react';
import { X, Database, ShieldCheck, MapPin, Grid, BarChart3, AlertCircle } from 'lucide-react';

export default function InformationPanel({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="w-full max-w-2xl glass-panel-accent rounded-2xl p-6 text-slate-200 space-y-6 shadow-2xl border border-cyan-500/30 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30">
              <Database className="w-6 h-6 text-cyan-400" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-100 tracking-tight">
                Sikkim Historical Landslide Baseline Metrics
              </h2>
              <p className="text-xs text-slate-400">
                Phase 5 Locked Baseline & Provenance Audit Specifications
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Primary Feature Breakdown */}
        <div className="space-y-3">
          <h3 className="text-xs uppercase font-mono font-semibold tracking-wider text-cyan-400 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-cyan-400" /> Primary Historical Inventory Baseline
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
              <div className="text-xl font-bold font-mono text-slate-100">507</div>
              <div className="text-[11px] text-slate-400 font-medium">Primary Source Features</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/80 border border-red-900/40 text-center">
              <div className="text-xl font-bold font-mono text-red-400">255</div>
              <div className="text-[11px] text-slate-400 font-medium">GE Polygons</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/80 border border-yellow-900/40 text-center">
              <div className="text-xl font-bold font-mono text-yellow-400">185</div>
              <div className="text-[11px] text-slate-400 font-medium">GE Points</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/80 border border-cyan-900/40 text-center">
              <div className="text-xl font-bold font-mono text-cyan-400">67</div>
              <div className="text-[11px] text-slate-400 font-medium">Cartosat Polygons</div>
            </div>
          </div>
        </div>

        {/* Derived Associations Rule */}
        <div className="p-4 rounded-xl bg-amber-950/40 border border-amber-500/40 text-xs space-y-1.5">
          <div className="font-semibold text-amber-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            Derived Spatial Association Rule (23 Cartosat Unions)
          </div>
          <p className="text-amber-200/80 leading-relaxed">
            The 23 Cartosat scarp/deposit unions are project-derived spatial associations. They MUST NOT be added to primary inventory feature counts, density numerators, or recurrence calculations.
          </p>
        </div>

        {/* Grid & Area Metrics */}
        <div className="space-y-3">
          <h3 className="text-xs uppercase font-mono font-semibold tracking-wider text-cyan-400 flex items-center gap-2">
            <Grid className="w-4 h-4 text-cyan-400" /> 1 km Analysis Grid & Spatial Coverage
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-[11px] text-slate-400">Total Grid Cells</div>
              <div className="text-base font-bold font-mono text-slate-100">7,355</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/80 border border-emerald-900/40">
              <div className="text-[11px] text-emerald-400">OBSERVED Cells</div>
              <div className="text-base font-bold font-mono text-emerald-300">2,820</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-[11px] text-slate-400">DATA_NOT_HELD Cells</div>
              <div className="text-base font-bold font-mono text-slate-400">4,437</div>
            </div>
          </div>
        </div>

        {/* State Boundary & Area Conservation */}
        <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 text-xs space-y-2 font-mono">
          <div className="flex justify-between">
            <span className="text-slate-400">Sikkim State Boundary Area (GADM v4.1):</span>
            <span className="text-slate-200 font-bold">~7,081.54 km²</span>
          </div>
          <div className="flex justify-between border-t border-slate-800 pt-1.5">
            <span className="text-slate-400">Grid Intersection Area:</span>
            <span className="text-slate-200 font-bold">~7,079.48 km²</span>
          </div>
          <div className="flex justify-between border-t border-slate-800 pt-1.5">
            <span className="text-slate-400">Zenodo Mapped Extent Footprint:</span>
            <span className="text-emerald-400 font-bold">~2,962.15 km²</span>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold text-xs transition-colors"
          >
            Close Spec Panel
          </button>
        </div>
      </div>
    </div>
  );
}
