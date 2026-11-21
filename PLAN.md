# Mech Royale build plan

## 1. Establish a measured baseline

Publish the official starter as a public repository, submit its commit and record the score. Preserve that commit so improvements can be compared with a known starting point. Local conformance checks pass, including the Intel Docker image under the match restrictions. No real-match score has been measured yet.

## 2. Make survival decisions better

Use zone timing to stay in the playable circle without needlessly running to its center. Detect getting stuck from movement over multiple observations. Read the static map to choose routes around buildings. Balance threat avoidance against keeping enough energy to escape. Each change must have a clear reason and be evaluated separately.

## 3. Improve aiming and firing

Gun bullets take time to reach an enemy. Predict the target's movement rather than aiming only at its current position. Respect actual torso aim, weapon range and cooldown. Handle laser charging/release, mortar arcs and lightning range separately instead of holding every trigger indiscriminately.

## 4. Make loot and upgrades deliberate

Collect nearby useful resources only when their value outweighs exposure and travel time. Check both horizontal and vertical pickup distance. Choose upgrades from the live offer to match our current needs instead of always selecting the first option.

## 5. Compare results and lock the final

Record commit, strategy change, conformance result, submission time and practice score. Four submissions per hour are allowed under the released rules. Keep a buffer before Sunday November 22, 2026 at 10 AM Central to choose the final entry and address build problems. The final faces different opponents, so avoid treating a practice-only trick as a general strategy.

## Working habits

- Explain the reason behind each decision in plain language.
- Keep stdout for game messages and stderr for diagnostic logs.
- Use the published live configuration instead of hard-coding defaults.
- Check actual strategy behavior on focused scenarios, then run the supplied conformance check.
- A valid check proves protocol compliance, not survival performance.
- Do not claim that a code change improves the score until a match result supports it.
