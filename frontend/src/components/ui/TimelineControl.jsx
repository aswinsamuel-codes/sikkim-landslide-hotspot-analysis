import React from 'react';
import { Calendar, Info, AlertCircle, CheckCircle2, Clock } from 'lucide-react';

export default function TimelineControl({
  timeline,
  selectedYear,
  onSelectYear,
  onClearYear
}) {
  return (
    <div className="w-full glass-panel-accent rounded-xl p-4 text-xs space-y-3 shadow-2xl border border-slate-800">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Calendar className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold text-slate-100">Extensible 15-Year Timeline Architecture</span>
        </div>
        <div className="flex items-center space-x-3 text-[11px]">
          {selectedYear ? (
            <button
              onClick={onClearYear}
              className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium border border-slate-700 transition-colors"
            >
              Show All Years
            </button>
          ) : (
            <span className="text-cyan-400 font-mono">Viewing All Imagery Years</span>
          )}
        </div>
      </div>

      {/* 3-Category Legend Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2 py-1 text-[11px]">
        <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-300">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
          <span><strong>Validated Held:</strong> Zenodo 8169506 Imagery Years</span>
        </div>
        <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded bg-amber-950/60 border border-amber-500/40 text-amber-300">
          <Clock className="w-3.5 h-3.5 text-amber-400 shrink-0" />
          <span><strong>Authoritative Metadata:</strong> NRSC 2014/2023 Vector Pending</span>
        </div>
        <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded bg-slate-900/80 border border-slate-700 text-slate-400">
          <AlertCircle className="w-3.5 h-3.5 text-slate-500 shrink-0" />
          <span><strong>Data Not Held:</strong> Unmapped / Unavailable Years</span>
        </div>
      </div>

      {/* Year Grid */}
      <div className="grid grid-cols-6 sm:grid-cols-8 md:grid-cols-12 gap-1.5 pt-1">
        {timeline.map((item) => {
          const isSelected = selectedYear === item.year;
          const isHeld = item.status_class === 'VALIDATED_OBSERVATIONS_HELD';
          const isAuthoritative = item.status_class === 'AUTHORITATIVE_METADATA_ONLY';
          const isDataNotHeld = item.status_class === 'DATA_NOT_HELD';

          let btnBg = 'bg-slate-900/60 text-slate-500 border-slate-800 hover:border-slate-700';
          if (isHeld) {
            btnBg = 'bg-emerald-950/40 text-emerald-200 border-emerald-700/60 hover:bg-emerald-900/50 hover:border-emerald-500';
          } else if (isAuthoritative) {
            btnBg = 'bg-amber-950/40 text-amber-200 border-amber-700/60 hover:bg-amber-900/50 hover:border-amber-500';
          }

          if (isSelected) {
            btnBg = 'bg-cyan-600 text-white font-bold border-cyan-300 ring-2 ring-cyan-400/50 shadow-lg';
          }

          return (
            <button
              key={item.year}
              onClick={() => onSelectYear(item.year)}
              disabled={isDataNotHeld}
              className={`p-2 rounded-lg border text-center transition-all flex flex-col items-center justify-between h-14 ${btnBg} ${
                isDataNotHeld ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
              }`}
              title={`${item.year}: ${item.notes}`}
            >
              <span className="text-xs font-mono font-semibold">{item.year}</span>
              {isHeld && (
                <span className="text-[10px] px-1 py-0.5 rounded bg-emerald-900/80 text-emerald-300 font-mono">
                  {item.feature_count}
                </span>
              )}
              {isAuthoritative && (
                <span className="text-[9px] px-1 py-0.5 rounded bg-amber-900/80 text-amber-300 font-mono uppercase">
                  Meta
                </span>
              )}
              {isDataNotHeld && (
                <span className="text-[9px] text-slate-500 font-mono uppercase truncate max-w-[40px]">
                  N/A
                </span>
              )}
            </button>
          );
        })}
      </div>

      <div className="text-[11px] text-slate-400 leading-snug flex items-center gap-2 border-t border-slate-800/80 pt-2 font-mono">
        <Info className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
        <span>
          Observation years represent satellite imagery acquisition dates, NOT failure/event dates. Missing years render as <strong>DATA_NOT_HELD</strong> (no zero counts created).
        </span>
      </div>
    </div>
  );
}
