"""Public synthetic classroom UI policy checks; independent toy implementation.

No canonical GeometryLearningProgram specs, problem IDs, or source code here.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ToyActivity:
    role: str
    actions: tuple
    prediction: bool = False
    replay_after_commit: bool = False
    released: bool = True


def check_play(activity, trace):
    if activity.role not in {"TRAINING", "DIRECT", "PREDICT", "EXTENSION"}:
        raise ValueError("Unknown toy activity")
    if not activity.released and activity.role != "EXTENSION":
        raise ValueError("Unapproved exercise cannot be scored")
    if activity.role == "EXTENSION" and not activity.released:
        if any(event == "SUBMIT" for event in trace):
            raise ValueError("Unreleased extension cannot be submitted")
    seen_commit = False
    saved_first = None
    submitted = False
    for event in trace:
        if submitted:
            raise ValueError("No events after score submission")
        if event == "SHOW_SOLUTION":
            if activity.role == "PREDICT" and not seen_commit:
                raise ValueError("No solution/replay before commitment")
        elif event == "REPLAY":
            if not activity.replay_after_commit or not seen_commit:
                raise ValueError("Replay not authorized before commit")
        elif event == "CHOOSE":
            if event not in activity.actions:
                raise ValueError("Selection not allowed")
            if saved_first is None:
                saved_first = "FIRST_SELECTION_RETAINED"
        elif event == "COMMIT":
            if "COMMIT" not in activity.actions or seen_commit:
                raise ValueError("Invalid commitment")
            seen_commit = True
        elif event == "UNDO":
            if "UNDO" not in activity.actions or seen_commit:
                raise ValueError("Invalid undo")
        elif event in {"TURN", "MIRROR", "PLACE"}:
            if event not in activity.actions or (activity.role == "PREDICT" and not seen_commit):
                raise ValueError("Unauthorized geometry action")
        elif event == "SUBMIT":
            if activity.role == "TRAINING":
                raise ValueError("Teaching action cannot create a scored result")
            if activity.role == "PREDICT" and not seen_commit:
                raise ValueError("Prediction must commit")
            submitted = True
        else:
            raise ValueError("Unknown toy event")
    return {"submitCount":int(submitted), "firstChoiceRetained":saved_first is not None,
            "committed":seen_commit}


def classify(*, solved, helped, corrected, technical_abort=False):
    if technical_abort:
        return "UNSCORED_TECHNICAL"
    if not solved:
        return "UNSOLVED"
    if helped:
        return "ASSISTED_SUCCESS"
    if corrected:
        return "SELF_CORRECTED_SUCCESS"
    return "INDEPENDENT_SUCCESS"


def positive_process(*, legal, future, actual_move):
    if future not in {"YES","NO","UNKNOWN"}:
        raise ValueError("Invalid synthetic future state")
    return bool(legal and actual_move and future=="YES")
