"""Public toy event ledger: no private problem geometry, student data or IDs."""
from dataclasses import dataclass,field

@dataclass(frozen=True)
class Event:
    event_id:str
    ordinal:int
    kind:str
    episode:str
    payload:dict=field(default_factory=dict)

class ToyLedger:
    def __init__(self, *, history_complete=True):
        self.events=[]
        self.by_id={}
        self.exposed=set()
        self.episodes={}
        self.history_complete=history_complete

    def push(self,event):
        if event.event_id in self.by_id:
            if self.by_id[event.event_id]!=event:
                raise ValueError("Conflicting duplicate event identity")
            return self.episodes.get(event.episode)
        if event.ordinal!=len(self.events):
            raise ValueError("Out-of-order/duplicate event ordinal")
        if not event.event_id or not event.episode:
            raise ValueError("Missing event identity")
        ep=self.episodes.get(event.episode)
        if event.kind=="SHOW":
            if ep is not None:
                raise ValueError("Episode displayed twice")
            role=event.payload.get("role")
            key=event.payload.get("equivalence_key")
            if role not in ("TRAIN_A","TRAIN_B","TEST") or not key:
                raise ValueError("Invalid toy stimulus metadata")
            verified=event.payload.get("verified_identity") is True
            fresh=("UNKNOWN" if not self.history_complete or not verified
                   else "EXPOSED" if key in self.exposed else "FRESH")
            ep={"role":role,"key":key,"freshness":fresh,
                "assigned":event.payload.get("assigned") is True,
                "approved":event.payload.get("approved") is True,
                "first":None,"selection":None,"committed":False,
                "supported":False,"scored":False,"aborted":False,
                "correct":None,"scoreEvents":0}
            self.episodes[event.episode]=ep
            self.exposed.add(key)
        else:
            if ep is None:
                raise ValueError("No presented episode")
            if ep["aborted"]:
                raise ValueError("Aborted episode is closed")
            if event.kind=="CHOOSE":
                if ep["committed"] or ep["scored"] or ep["role"]!="TEST":
                    raise ValueError("Selection not allowed")
                choice=event.payload.get("choice")
                if not isinstance(choice,str) or not choice:
                    raise ValueError("Missing choice")
                if ep["first"] is None:
                    ep["first"]=choice
                ep["selection"]=choice
            elif event.kind=="HELP_REQUESTED":
                pass
            elif event.kind=="HELP_SHOWN":
                if not ep["committed"] and ep["role"]=="TEST":
                    ep["supported"]=True
            elif event.kind=="REVEAL":
                if ep["role"]=="TEST" and not ep["committed"]:
                    raise ValueError("Cannot disclose test answer before commit")
            elif event.kind=="COMMIT":
                if ep["role"]!="TEST" or ep["committed"] or ep["selection"] is None:
                    raise ValueError("Invalid commit")
                ep["committed"]=True
            elif event.kind=="REPLAY":
                if not ep["committed"]:
                    raise ValueError("Replay before commitment")
            elif event.kind=="UNDO":
                if ep["role"]=="TEST" and ep["committed"]:
                    raise ValueError("Undo cannot alter committed choice")
            elif event.kind=="RESULT":
                if ep["role"]!="TEST" or ep["scored"] or not ep["committed"]:
                    raise ValueError("Unassigned, duplicate or uncommitted score")
                if not ep["approved"] or not ep["assigned"]:
                    raise ValueError("Unapproved or unassigned scored candidate")
                if type(event.payload.get("correct")) is not bool:
                    raise ValueError("Only authoritative boolean correctness sample")
                ep["correct"]=event.payload["correct"]
                ep["scored"]=True
                ep["scoreEvents"]+=1
            elif event.kind=="TECH_ABORT":
                if ep["scored"]:
                    raise ValueError("Cannot abort a scored result")
                ep["aborted"]=True
            elif event.kind in ("SUSPEND","RESUME"):
                pass
            else:
                raise ValueError("Unknown toy event")
        self.events.append(event)
        self.by_id[event.event_id]=event
        return ep

    def fresh_independent(self,episode):
        ep=self.episodes[episode]
        return bool(ep["role"]=="TEST" and ep["freshness"]=="FRESH" and
                    ep["scored"] and ep["correct"] is True and
                    not ep["supported"] and ep["first"]==ep["selection"])

    def summary(self,episode):
        ep=self.episodes[episode]
        return {"freshness":ep["freshness"],"first":ep["first"],
                "committed":ep["selection"] if ep["committed"] else None,
                "supportDelivered":ep["supported"],"submitted":ep["scoreEvents"],
                "independentFreshCandidate":self.fresh_independent(episode),
                "technicallyAbortedNotScored":ep["aborted"] and not ep["scored"]}
