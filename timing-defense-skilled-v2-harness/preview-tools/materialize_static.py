from pathlib import Path

root = Path(__file__).parent
public = root.parent / 'public'
app_base = root / 'app.base.mjs'
protocol_base = root / 'protocol.base.mjs'

app_text = app_base.read_text(encoding='utf-8')
old = "a.download='linkline-nl5-matched-repair-1.json'"
new = "a.download='linkline-nl6-matched-repair-1.json'"
if app_text.count(old) != 1:
    raise SystemExit('app export filename replacement cardinality mismatch')
(public / 'app.mjs').write_text(app_text.replace(old, new, 1), encoding='utf-8')

text = protocol_base.read_text(encoding='utf-8')

def once(old_value: str, new_value: str) -> None:
    global text
    count = text.count(old_value)
    if count != 1:
        raise SystemExit(f'protocol replacement cardinality {count}: {old_value[:80]!r}')
    text = text.replace(old_value, new_value, 1)

once('LINKLINE_A3_NL5_RUNTIME_ANALYSIS_METADATA', 'LINKLINE_A3_NL6_RUNTIME_ANALYSIS_METADATA')
once(
    "\nexport async function validateSessionBundle(bundle,metadata){",
    "\nconst EXPECTED_PAIR_SHAPES=Object.freeze([\n"
    "  {axis:'SAME_L',controlN:4,controlL:8,largerN:6,largerL:8},\n"
    "  {axis:'OCCUPANCY_40_EXACT_DISTANCE',controlN:4,controlL:6,largerN:6,largerL:15},\n"
    "  {axis:'SAME_L',controlN:4,controlL:9,largerN:6,largerL:9},\n"
    "  {axis:'OCCUPANCY_40_EXACT_DISTANCE',controlN:4,controlL:6,largerN:6,largerL:15},\n"
    "  {axis:'SAME_L',controlN:4,controlL:9,largerN:6,largerL:9},\n"
    "  {axis:'OCCUPANCY_40_EXACT_DISTANCE',controlN:4,controlL:7,largerN:6,largerL:15}\n"
    "]);\n\nexport async function validateSessionBundle(bundle,metadata){"
)
once("if(bundle?.largerN!==5)errors.push('largerN');", "if(bundle?.largerN!==6)errors.push('largerN');")
once(
    "  const quarantine=new Set(QUARANTINED_RESEARCH_EQUIVALENCE_IDS),ids=new Set();\n  const lengthCounts=new Map([[6,0],[7,0],[9,0]]);",
    "  const quarantine=new Set(QUARANTINED_RESEARCH_EQUIVALENCE_IDS),ids=new Set();"
)
once(
    "    const pair=bundle.pairs?.[pairIndex],position=pairIndex+1;",
    "    const pair=bundle.pairs?.[pairIndex],position=pairIndex+1,shape=EXPECTED_PAIR_SHAPES[pairIndex];"
)
once("if(pair?.axis!=='SAME_L')errors.push(`pairAxis:${position}`);", "if(pair?.axis!==shape.axis)errors.push(`pairAxis:${position}`);")
once("p.axis!=='SAME_L'", "p.axis!==shape.axis")
once(
    "    if(members[0].length!==members[1].length||!lengthCounts.has(members[0].length))errors.push(`pairLength:${position}`);\n"
    "    else lengthCounts.set(members[0].length,lengthCounts.get(members[0].length)+1);\n"
    "    const control=members.find(p=>p.pairMember==='control'),larger=members.find(p=>p.pairMember==='larger');\n"
    "    if(!control||!larger||control.n!==4||larger.n!==5)errors.push(`pairMembers:${position}`);",
    "    const control=members.find(p=>p.pairMember==='control'),larger=members.find(p=>p.pairMember==='larger');\n"
    "    if(!control||!larger)errors.push(`pairMembers:${position}`);\n"
    "    else{\n"
    "      if(control.n!==shape.controlN||control.length!==shape.controlL||larger.n!==shape.largerN||larger.length!==shape.largerL)errors.push(`pairShape:${position}`);\n"
    "      if(shape.axis==='SAME_L'&&control.length!==larger.length)errors.push(`pairLength:${position}`);\n"
    "      if(shape.axis==='OCCUPANCY_40_EXACT_DISTANCE'&&metadata?.shortestDistanceByResearchEquivalenceIdV1?.[control.researchEquivalenceIdV1]!==metadata?.shortestDistanceByResearchEquivalenceIdV1?.[larger.researchEquivalenceIdV1])errors.push(`pairExactDistance:${position}`);\n"
    "    }"
)
once("  for(const [length,count] of lengthCounts)if(count!==2)errors.push(`lengthPairCount:${length}:${count}`);\n\n", "\n")
once("if(![4,5].includes(puzzle.n))", "if(![4,6].includes(puzzle.n))")
(public / 'protocol.mjs').write_text(text, encoding='utf-8')
