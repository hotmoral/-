"""Public synthetic-only conceptual-lesson boundary checker."""
from dataclasses import dataclass

PHASES=("LOOK","HANDLE","IDENTIFY","FADE_HELP","FRESH_TRIAL","DEBRIEF")
@dataclass(frozen=True)
class Step:
    phase:str
    stimulus:str
    role:str
    answer_revealed:bool=False

def verify(steps, released=True, assisted=False):
    if tuple(s.phase for s in steps)!=PHASES: raise ValueError("phase order")
    if steps[0].stimulus!=steps[1].stimulus or steps[1].stimulus!=steps[2].stimulus: raise ValueError("different introduction")
    if steps[3].stimulus==steps[0].stimulus: raise ValueError("faded practice not new")
    if steps[4].stimulus in {s.stimulus for s in steps[:4]}: raise ValueError("assessment reused")
    if steps[5].stimulus!=steps[4].stimulus: raise ValueError("debrief unrelated")
    if any(s.role!="TEACH" for s in steps[:4]): raise ValueError("teaching scored")
    if steps[4].role!="SCORE" or steps[5].role!="EXPLAIN": raise ValueError("invalid scoring")
    if any(s.answer_revealed for s in steps[:5]): raise ValueError("answer leaked")
    if not released or assisted: raise ValueError("not independent release")
    return "PASS_SYNTHETIC_ONLY"

def example():
    return [Step("LOOK","a","TEACH"),Step("HANDLE","a","TEACH"),Step("IDENTIFY","a","TEACH"),Step("FADE_HELP","b","TEACH"),Step("FRESH_TRIAL","c","SCORE"),Step("DEBRIEF","c","EXPLAIN",True)]
