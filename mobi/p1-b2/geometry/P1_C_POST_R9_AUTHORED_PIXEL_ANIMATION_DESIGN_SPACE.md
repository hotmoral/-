# Mobi — Authored Pixel Animation Design Space after R9

Status: **PUBLIC ANALYSIS / NON-CANONICAL / NO IMPLEMENTATION DECISION**  
Date: **2026-10-16**

## 1. Purpose

This analysis explores a materially different presentation strategy after R9:

> pre-authored, high-quality pixel animation clips selected by growth stage, action, direction, transition and interaction state.

The purpose is not to lock counts such as 36 directions or 32 frames. The purpose is to enumerate the design space first, then prune by visible quality, authoring cost, storage/runtime cost and behavioral coverage.

Private `hotmoral/Mobi` remains canonical. This public branch is analysis only.

## 2. Four growth-stage hypothesis

Four visual/behavioral growth stages are retained as the working hypothesis because they provide enough room for meaningful user–cat and cat–cat progression without creating a large number of near-duplicate life stages.

Exact ages and pixel sizes are not frozen.

| Stage | Working label | Candidate native size | Structural/behavioral role |
|---|---|---:|---|
| G1 | young kitten | ~64 px | high head/body ratio, short limbs, unstable/compact movement, strong play/reactivity |
| G2 | juvenile kitten | ~72 px | longer limbs, rapid exploration, energetic play, improving coordination |
| G3 | adolescent / young cat | ~84 px | near-adult locomotion, high activity/social exploration, transitional proportions |
| G4 | adult | ~96 px | mature proportions, stable locomotion, broad rest/groom/social repertoire |

Growth stage should constrain **what motions are physically/behaviorally available**, but should not directly encode the whole behavioral state.

Recommended separation:

`growth capability × current internal state × user relationship × cat-cat relationship × environment affordance → action choice → animation clip`.

Potential state dimensions, subject to later behavioral design:

- energy / arousal;
- sleep pressure;
- curiosity;
- stress / vigilance;
- user affinity / trust;
- cat-cat affinity / rivalry;
- territory familiarity;
- recent event context;
- current support/environment affordance.

## 3. Animation asset ontology

Each animation should be classified before authoring.

### 3.1 Clip temporal type

- `LOOP`: repeatable cycle such as walk, breathing, idle.
- `ONE_SHOT`: finite event such as jump, yawn, shake.
- `TRANSITION`: explicit state bridge such as stand→sit or walk→stop.
- `PAIRED_ROLE`: synchronized interaction role, e.g. greeting initiator / receiver.
- `OVERLAY_MICRO`: localized motion that may be composited if pixel quality allows, e.g. blink/ear flick/tail tip.

### 3.2 Direction sensitivity tiers

Direction count must be action-specific rather than globally fixed.

Candidate tiers to test:

- D1: 1 orientation-independent or local overlay.
- D4: 4 principal orientations.
- D8: 45° spacing.
- D12: 30° spacing.
- D16: 22.5° spacing.
- D24: 15° spacing.
- D36: 10° spacing.
- D48: 7.5° spacing — exploratory upper bound only.
- D72: 5° spacing — stress/ceiling case only; likely excessive unless native-scale testing proves visible benefit.

The important comparison for locomotion is likely D16 vs D24 vs D36, but that remains an empirical question.

### 3.3 Frame-density tiers

Frame count also must be action-specific.

Candidate authored frame counts:

- F3–F6: blink, ear twitch, tiny reaction.
- F6–F12: impact, recoil, quick turn, short transition.
- F12–F16: run cycles, simple sit/stand transitions.
- F16–F24: ordinary walk, jump, exploratory actions.
- F24–F32: slow walk, detailed posture transitions, stretch.
- F32–F64+: grooming / long expressive sequences when needed.

Frame count and playback rate are separate. A 24-frame cycle can be time-scaled at runtime without authoring another clip if the motion remains convincing.

## 4. Broad action candidate space

The following list is intentionally wider than V1 needs. It is a pruning pool, not an authorization to author all clips.

### A. Baseline idle / locomotion

1. stand idle
2. alert stand idle
3. slow walk
4. normal walk
5. brisk walk / trot
6. run / gallop
7. kitten scamper
8. stalk / creep
9. cautious step
10. backward step
11. lateral step
12. approach target
13. retreat from target
14. walk along edge
15. balance on narrow edge

High directional sensitivity: locomotion 3–14. Candidate range D16–D36 for primary locomotion, D8–D16 for low-frequency variants.

### B. Locomotion transitions and orientation changes

16. idle→walk start
17. walk→idle stop
18. walk→run
19. run→walk
20. walk→turn while moving
21. turn in place
22. quick head-led body turn
23. reverse / about-face
24. recover balance after turn

Transitions should not automatically inherit full locomotion direction density. Candidate range D8–D24 depending visual need.

### C. Posture family

25. stand→sit
26. sit idle
27. sit→stand
28. sit→loaf
29. loaf idle
30. loaf→sit
31. sit→lie
32. lie / sphinx idle
33. lie→sit
34. lie→stand
35. side lie
36. curl into sleep
37. uncurl / wake posture
38. roll partially onto side/back

Candidate direction range D4–D12 for most posture clips.

### D. Rest / sleep / comfort

39. breathing idle
40. drowsy head drop
41. doze loop
42. sleep breathing
43. wake slowly
44. wake suddenly
45. yawn
46. forward stretch
47. hindquarter stretch
48. whole-body stretch
49. shake body
50. settle / reposition before sleep

Usually D4–D8; some transitions may need D8–D12.

### E. Grooming / maintenance

51. lick nose / lips
52. lick forepaw
53. wash face with paw
54. groom chest
55. groom flank
56. groom belly
57. groom hind leg
58. groom tail
59. scratch neck/ear with hind paw
60. brief body shake after grooming
61. inspect / nibble fur spot

Usually D4–D8. Long sequence clips may use F24–F64+.

### F. Exploration / attention

62. look left/right/up/down
63. head tilt
64. sniff air
65. sniff ground
66. sniff object / UI target
67. inspect screen edge
68. peer downward from edge
69. paw-test surface
70. freeze and listen
71. orient ears toward stimulus
72. track moving stimulus
73. investigate new object
74. cautious approach to unfamiliar stimulus

Candidate D8–D16 for head/body-oriented actions; micro-ear variants may be overlays.

### G. Play / predatory play

75. play crouch
76. wiggle / pre-pounce preparation
77. pounce
78. chase
79. short hop
80. bat with forepaw
81. double bat
82. grab / hold
83. bunny-kick play
84. rear up
85. roll / tumble
86. sudden sideways hop
87. toy/stimulus stalk
88. failed pounce / recovery

Strong growth differentiation. G1/G2 may require unique unstable/tumble variants; G3/G4 can be more controlled.

### H. User interaction

89. notice user touch
90. orient toward touch point
91. approach user stimulus
92. avoid / step away
93. solicit attention
94. rub / nuzzle interaction target
95. lean into petting
96. content sit/lie response
97. paw at user stimulus
98. follow moving finger/stimulus
99. startled touch response
100. trust-based close rest near user target
101. return after avoidance
102. attention interruption / glance back

Many can reuse locomotion/posture clips at the behavior layer; unique full-body clips should be created only when silhouette/timing materially differs.

### I. Cat–cat social interaction

103. notice other cat
104. approach other cat
105. cautious approach
106. nose greeting
107. mutual sniff
108. flank/body rub
109. follow another cat
110. sit near
111. lie near
112. sleep adjacent
113. mutual grooming initiator
114. mutual grooming receiver
115. play invitation
116. chase initiator
117. chase receiver
118. pounce on partner
119. play wrestle
120. playful swat
121. defensive swat
122. freeze / stare
123. arch / threat posture
124. retreat / disengage
125. reconcile / re-approach

Paired interactions should use synchronized role clips rather than one unique animation for every pair of cats. Growth-pair combinations should be handled through shared contact markers and compatible role timing when feasible.

### J. Environment / overlay-specific physical actions

126. step onto virtual ledge / UI boundary
127. step off ledge
128. jump up
129. jump down
130. horizontal gap jump
131. landing
132. heavy landing recovery
133. edge balance correction
134. slip and recover
135. sit at screen edge
136. peer around/behind UI region
137. route around obstacle
138. wait at blocked path

These actions may be particularly important to Mobi because the smartphone interface is part of the cat's environment.

### K. Micro-expression / secondary motion candidates

139. blink
140. slow blink
141. ear flick
142. ears rotate toward sound
143. tail-tip twitch
144. tail sway
145. tail lift / lower
146. whisker/face micro-change if later art supports it
147. tiny head bob / breathing
148. weight shift
149. paw flex
150. small shoulder/haunch settle

These should be tested as overlays/layers before multiplying full-body directional clips.

## 5. Growth differentiation matrix

Legend:

- `U`: unique motion character strongly justified.
- `V`: same action family but timing/proportion variant likely required.
- `S`: standard choreography may be shared as motion reference, while raster art remains stage-specific.
- `R`: rare / optional for the stage.
- `N`: normally unavailable.

| Action family | G1 | G2 | G3 | G4 |
|---|---|---|---|---|
| basic walk | U | U | V | S |
| brisk walk/trot | U | U | V | S |
| run | R/V | U | V | S |
| stalk | R | U | V | S |
| balance/edge walk | U | U | V | S |
| stand/sit/lie transitions | U | V | V | S |
| sleep/rest | U | V | S | S |
| grooming | U/short | V | V | S/full |
| exploration | U | U | V | S |
| pounce/play | U | U | V | V |
| complex jump | R | U | V | S |
| user approach/avoid | U | V | V | S |
| cat-cat greeting | U | V | V | S |
| cat-cat chase/play | U | U | V | V |
| threat/territorial behavior | R/N | R | V | S |
| mutual grooming | R/N | R/V | V | S |

This table is intentionally behavioral rather than biological. Final availability must follow Mobi's progression design.

## 6. Reuse opportunities that do not require visual compromise

Potential reuse layers:

1. **Behavioral reuse** — `approach user`, `approach cat`, `approach object` may call the same locomotion clip and differ only in target/state logic.
2. **Timing/choreography reuse** — growth stages may share event timing/contact markers while retaining separately drawn sprites.
3. **Mirror reuse** — left/right-facing base-body animation may be mirrored where markings/accessories/anatomical event semantics permit; metadata must swap L/R correctly.
4. **Transition reuse** — a common `walk→stop` may serve many causes of stopping.
5. **Micro-layer reuse** — blink, ear flick, tail-tip motion can potentially overlay a compatible full-body clip.
6. **Paired-role reuse** — cat-cat interactions use role A/B clips synchronized to shared contact events instead of unique assets for every pair identity.

Do not use reuse when it creates obvious repeated/robotic behavior or violates physical contact.

## 7. Major combinatorial traps

Avoid these multiplications unless perceptual tests prove they are necessary:

- every action × every direction;
- every action × the same frame count;
- every context × a unique full-body clip;
- every cat pair × a unique paired animation;
- every mood × a full duplicate animation bank;
- every coat/appearance × body animation frames;
- every speed × separately drawn walk cycles if timing changes alone suffice;
- every growth pair × unique social choreography.

The preferred architecture is a **sparse animation matrix**: only combinations with visible value receive unique frames.

## 8. Structural metadata retained per clip/frame

Even in an authored-sprite strategy, animation should carry physical metadata so Mobi can remain coherent with the existing semantic/contact foundation.

Candidate metadata:

- nominal body root;
- four paw/contact anchors;
- current planted/swing paw state;
- head anchor;
- tail root;
- body/visual bounds;
- intended facing direction index;
- transition entry/exit pose IDs;
- event markers: plant, release, apex, contact, interaction touch;
- optional paired-interaction contact anchor;
- loop seam identity.

This allows visual animation to be authored directly while gameplay/environment logic still knows where the cat is physically contacting the screen environment.

## 9. Open questions to prune experimentally

1. For 64–96 px cats, when does D16→D24→D36 stop producing visible improvement?
2. For walk cycles, when does F16→F24→F32 stop producing visible improvement?
3. Can left/right mirroring halve authoring cost without visible asymmetry problems?
4. Which micro-actions can be layers rather than full-body duplicates?
5. How much growth-specific redrawing is required versus reusable choreography?
6. Which social interactions truly need paired clips?
7. How many transition clips are required before the state machine feels continuous rather than clip-like?
8. Can 4 growth stages carry meaningful progression without visually abrupt stage transitions?
9. What package/download budget is acceptable for the final Android product?
10. Can animation banks be loaded on demand by growth/action family to avoid large runtime texture memory?

## 10. Current non-decision

No exact count is frozen here.

Retained proposition for next analysis:

> authored directional pixel animation is a viable high-quality candidate only if direction density, frame density, behavior breadth and growth variation are allocated non-uniformly according to perceptual value.

Next required artifact: quantitative asset-budget and pruning analysis.