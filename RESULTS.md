# Practice results

## Official starter baseline

- Team: Bloom
- Receipt: BB-5FF74C07
- Submitted: November 20, 2026, 8:33 PM as displayed by the team submission record (site labels can differ from local timezone).
- Commit: 5009066d70121504c43298a93b2a55d8165c9785
- Result: Scored, 1.15 placement points.
- Snapshot rank: 81 of 86 scored teams. This is temporary and changes as teams submit.
- Matches per practice submission: 48 under published rules.
- This uses the unchanged official example strategy and matches the displayed 1.15 baseline.
- The site selected it as the team's current final entry because it is our only scored submission. This does not mean the team has qualified for the final series.

Next experiment: improve movement/survival or aiming with a clearly described change, validate conformance, then compare its measured score with 1.15.

## Survival steering v1

- Receipt: BB-B7D40A85
- Commit: f74769ddd4efd3bb422cd8d29f247b4849d1cb44
- Result: Scored, 0.79 placement points.
- Compared with baseline: -0.36 points. This experiment did not improve the practice score.
- Local focused tests and sandbox conformance passed; that did not translate into better gameplay.
- The site's selected entry remains the 1.15 starter. Do not manually select this weaker experiment as the final.
- The observed result does not explain individual deaths. Possible issues such as retreating into obstacles, resting without sensing enemies or inadequate route planning are hypotheses, not confirmed causes.
- Next: preserve this experiment in Git, build the next experiment from the scored baseline, and evaluate aiming separately before adding broad steering changes again.

## Predictive gun aiming v1

- Restores the starter's movement and changes aiming to predict bullet interception and target body height.
- Five focused maths tests passed; direct Python and sandboxed linux/amd64 Docker conformance passed all 300 observations with no missed deadlines.
- Docker maximum response: 7.1 ms locally. Local timing does not guarantee scorer timing.
- Receipt: BB-97061475. Submitted commit: 082352b916cf75255617b3e6389c853e28c422fb.
- Practice score: Scored, 1.38. Improvement over the measured 1.15 starter: +0.23 points (20%).
- The site automatically selected this as our best entry. Snapshot rank: 86 of 93 teams, which changes as entries arrive.
- This measures the combined aiming changes on the fixed practice seeds, not a guarantee of improvement against competitors or proof of any individual change's effect.
