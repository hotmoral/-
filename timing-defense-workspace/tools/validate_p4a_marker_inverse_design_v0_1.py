#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import run_p4a_marker_inverse_design_v0_1 as run
DEFAULT_CORPUS=ROOT/'legacy-game-structure'/'data'/'p4a_marker_opportunity_corpus_v0_1.json'
DEFAULT_SUMMARY=ROOT/'legacy-game-structure'/'data'/'p4a_marker_inverse_design_summary_v0_1.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--corpus',type=Path,default=DEFAULT_CORPUS);ap.add_argument('--summary',type=Path,default=DEFAULT_SUMMARY);a=ap.parse_args()
 corpus=run.normalize_corpus(json.loads(a.corpus.read_text())); expected=json.loads(a.summary.read_text()); actual=run.compute(corpus,int(expected['simulationSeedsPerFixture']))
 errors=[]
 if actual!=expected: errors.append('RECOMPUTED_SUMMARY_MISMATCH')
 if not all(actual['validation'].values()): errors.append('STATIC_CORPUS_VALIDATION_FAIL')
 if not all(x['nonEmpty'] for x in actual['centralP50FeasibleThresholdIntervals'].values()): errors.append('CENTRAL_UNIVERSAL_THRESHOLD_INTERSECTION_EMPTY')
 for lv,(lo,hi) in run.WINDOWS.items():
  for t in run.TIERS:
   p50=actual['centralReachAtMidpointCandidates'][str(lv)][t]['P50']
   if not (lo<=p50<=hi): errors.append(f'CENTRAL_P50_OUTSIDE_WINDOW:{t}:Lv{lv}:{p50}')
 result={'recordType':'P4A_VALIDATION','result':'PASS' if not errors else 'FAIL','errors':errors,'fixtures':len(corpus['fixtures']),'seedsPerFixture':expected['simulationSeedsPerFixture'],'allCentralIntersectionsNonEmpty':all(x['nonEmpty'] for x in actual['centralP50FeasibleThresholdIntervals'].values()),'warning':'P4-A marker-only diagnostic; candidate anchors are not numerically frozen.'}
 print(json.dumps(result,separators=(',',':'))); return 0 if not errors else 2
if __name__=='__main__':raise SystemExit(main())
