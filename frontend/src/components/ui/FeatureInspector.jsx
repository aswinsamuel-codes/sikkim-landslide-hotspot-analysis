import React from 'react';
import { X, Search, Shield, Calendar, Database, Hash, FileCode } from 'lucide-react';

export default function FeatureInspector({ feature, onClose }) {
  if (!feature) return null;

  const props = feature.properties || {};
  const geomType = feature.geometry ? feature.geometry.type : 'Unknown';

  return (
    <div className="w-96 glass-panel-accent rounded-xl p-5 text-xs space-y-4 shadow-2xl border border-cyan-500/30 z-30 animate-in slide-in-from-right duration-200">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2 text-cyan-400 font-semibold text-sm">
          <Search className="w-4 h-4" />
          <span>Feature Provenance Inspector</span>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="space-y-3 font-mono">
        {/* Layer & Feature Type */}
        <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1.5">
          <div className="text-[10px] uppercase tracking-wider text-slate-400 font-sans font-semibold">
            Feature Classification
          </div>
          <div className="text-sm font-semibold text-slate-100 font-sans flex items-center justify-between">
            <span>{props.layer_name || 'Landslide Inventory Feature'}</span>
            <span className="px-2 py-0.5 text-[10px] rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
              {geomType}
            </span>
          </div>
        </div>

        {/* Identifiers */}
        <div className="grid grid-cols-2 gap-2">
          <div className="p-2.5 rounded-lg bg-slate-900/70 border border-slate-800">
            <div className="text-[10px] text-slate-400 font-sans mb-1 flex items-center gap-1">
              <Database className="w-3 h-3 text-cyan-400" /> Source ID
            </div>
            <div className="text-slate-200 font-semibold truncate" title={props.source_id}>
              {props.source_id || 'ZENODO_8169506'}
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-slate-900/70 border border-slate-800">
            <div className="text-[10px] text-slate-400 font-sans mb-1 flex items-center gap-1">
              <Hash className="w-3 h-3 text-cyan-400" /> Original Feature ID
            </div>
            <div className="text-slate-200 font-semibold truncate">
              {props.original_feature_id || props.FID || props.id || 'SK_FEAT_001'}
            </div>
          </div>
        </div>

        {/* Provenance Tier & License */}
        <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 space-y-2 font-sans">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 flex items-center gap-1">
              <Shield className="w-3 h-3 text-emerald-400" /> Provenance Tier:
            </span>
            <span className="text-xs font-semibold text-emerald-300 font-mono">
              {props.provenance_tier || 'AUTHORITATIVE_COMMUNITY_PUBLIC'}
            </span>
          </div>

          <div className="flex items-center justify-between border-t border-slate-800/60 pt-1.5">
            <span className="text-[10px] text-slate-400">License Status:</span>
            <span className="text-xs text-slate-300 font-mono">
              {props.license_status || 'NOT_DECLARED_ON_RECORD'}
            </span>
          </div>
        </div>

        {/* Temporal Semantics */}
        <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 space-y-1.5 font-sans">
          <div className="text-[10px] text-slate-400 flex items-center gap-1">
            <Calendar className="w-3 h-3 text-amber-400" /> Temporal Semantics
          </div>
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-300">Observation Year:</span>
            <span className="font-mono text-amber-300 font-bold">
              {props.observation_year || props.Year || 'Active / Baseline'}
            </span>
          </div>
          <div className="flex items-center justify-between text-xs border-t border-slate-800/60 pt-1.5">
            <span className="text-slate-300">Event Failure Date:</span>
            <span className="font-mono text-slate-400 italic">
              {props.event_date || 'NULL (Not Failure Date)'}
            </span>
          </div>
        </div>

        {/* Source Attributes JSON dump */}
        <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1 font-sans">
          <div className="text-[10px] text-slate-400 flex items-center gap-1 mb-1">
            <FileCode className="w-3 h-3 text-cyan-400" /> Source Attributes
          </div>
          <pre className="text-[10px] text-slate-300 font-mono bg-slate-950 p-2 rounded overflow-x-auto max-h-32 border border-slate-800 leading-normal">
            {JSON.stringify(props, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
