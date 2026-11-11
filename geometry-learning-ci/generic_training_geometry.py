"""Public synthetic shape rules for teaching-vs-assessment examples.

Uses no private source, no frozen problems, no learner data and no A/B shapes.
"""
def normalize(cells):
    points={tuple(x) for x in cells}
    if not points or len(points)!=len(cells):
        raise ValueError("Empty or duplicated shape")
    if any(len(x)!=2 or any(type(v)!=int for v in x) for x in points):
        raise ValueError("Invalid integer-grid cell")
    dx=min(x for x,y in points);dy=min(y for x,y in points)
    return tuple(sorted((x-dx,y-dy) for x,y in points))

def rotate(cells):
    return normalize([(y,-x) for x,y in cells])

def mirror(cells):
    return normalize([(-x,y) for x,y in cells])

def orbit(cells):
    current=normalize(cells);result=set()
    for _ in range(4):
        result.add(current);result.add(mirror(current))
        current=rotate(current)
    return min(result)

def distinct_shapes(samples):
    keys=[orbit(s) for s in samples]
    if len(keys)!=len(set(keys)):
        raise ValueError("Training or evaluation shape repeats under rotation/reflection")
    return len(keys)

def placements(board,piece):
    B=set(normalize(board))
    P=set(normalize(piece))
    result=set()
    for bx,by in B:
        for px,py in P:
            pp=frozenset((x+bx-px,y+by-py) for x,y in P)
            if pp<=B:
                result.add(pp)
    return result

def first_moves(board,first,second):
    B=set(normalize(board))
    results=[]
    for firstPosition in placements(board,first):
        rest=frozenset(B-set(firstPosition))
        yes=rest in placements(board,second)
        results.append((firstPosition,"YES" if yes else "NO"))
    return results

def guard_unscored(*,role,event,assigned):
    if role.startswith("TRAIN") and event in ("SCORE","EVIDENCE","SUBMIT"):
        raise ValueError("Training does not score")
    if event=="SUBMIT" and not assigned:
        raise ValueError("Canonical assessment assignment required")
    return True
