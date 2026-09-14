import React from 'react';
import { ShieldCheck, Database, Layers, Info } from 'lucide-react';

export default function Header({ health, onOpenInfo }) {
  return (
    <header className="h-16 px-6 glass-panel border-b border-slate-800 flex items-center justify-between z-30 relative shadow-lg">
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-md shadow-cyan-500/20">
          <Database className="w-5 h-5 text-slate-950 stroke-[2.5]" />
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-100 tracking-tight flex items-center gap-2">
            SIKKIM HISTORICAL LANDSLIDE GIS PORTAL
            <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
              Phase 5 Baseline Locked
            </span>
          </h1>
          <p className="text-xs text-slate-400 font-medium">
            507 Primary Source Features &bull; Local-First Provenance Architecture (EPSG:4326)
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {/* Health status badge */}
        <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 text-xs">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-slate-300 font-mono text-[11px]">FastAPI Local: OK</span>
        </div>

        {/* Informational Panel Toggle */}
        <button
          onClick={onOpenInfo}
          className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors shadow-sm"
        >
          <Info className="w-4 h-4 text-cyan-400" />
          <span className="hidden sm:inline">Baseline Metrics</span>
        </button>
      </div>
    </header>
  );
}
