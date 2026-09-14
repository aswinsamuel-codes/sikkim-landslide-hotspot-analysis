import React from 'react';
import { AlertTriangle } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <div className="w-full bg-amber-950/90 border-y border-amber-500/40 px-4 py-2 flex items-center justify-between text-xs text-amber-200 z-20 relative shadow-inner">
      <div className="flex items-center space-x-2.5 max-w-7xl mx-auto">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 stroke-[2.5]" />
        <span className="font-semibold tracking-wide text-amber-300 uppercase text-[11px] shrink-0">
          Mandatory Semantic Notice:
        </span>
        <span className="text-amber-100/90 leading-tight">
          Mapped landslide inventory represents available observations. Areas without mapped features must not be interpreted as landslide-free or hazard-free. Missing data represents <strong>DATA_NOT_HELD</strong> state, not zero landslides.
        </span>
      </div>
    </div>
  );
}
