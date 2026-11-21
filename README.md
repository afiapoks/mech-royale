# Afia's Mech Royale bot

Python entry for the OSU Builders Buildathon, November 20–22, 2026.

Current version: `bloom-survival-v1`, our first movement experiment. The unchanged official example at commit `5009066` scored 1.15. The new version is not yet measured in matches.

## First experiment: survival steering

`navigation.py` considers a small set of possible movement directions and gives each a cost. Directions outside the playable circle get a large penalty. Directions nearer predicted enemy positions get a smaller penalty. The bot also estimates whether it needs to start moving into the next circle before it closes.

This is rule-based decision making: we define what matters, compare choices, and return the least costly one. It needs no online model and is fast enough to check on every observation. It does not yet plan routes using buildings or terrain. Suspected obstruction is inferred from movement history, which can also be affected by collisions or enemy effects.

The bot can pause in a safe area without visible enemies to conserve energy and allow healing. A repeated lack of movement while trying to move triggers a direction change and, when grounded with enough energy, a jump. Shooting, loot collection and upgrade choices still use the original starter logic so this experiment focuses on movement.

Focused tests cover returning from outside the zone, relocating before a deadline, retreating from an approaching enemy, resting without threats, and trying to escape when stuck. These tests validate intended decisions, not whether they win games.

## Setup results, November 20

- Direct Python conformance check: PASS, all 300 observations answered on time, no bad lines or wrong ticks.
- Docker builds: succeeded for linux/amd64 (competition architecture) and linux/arm64 (local architecture).
- Docker conformance check: PASS on the required linux/amd64 image, with no network, one CPU, 512 MB, read-only disk and the unprivileged user. All 300 observations answered on time; ready in 1,006 ms, maximum answer time 5.2 ms. Initial startup attempts stalled, but a later unchanged-image retry passed after Docker began starting containers normally. The original startup cause is not established.
- The base image is pinned by digest for reproducible builds. Only runtime Python files are copied into the image.
- Survival-v1 checks: five focused tests pass; direct Python and competition-style Intel Docker conformance pass for all 300 observations. Docker maximum response was 8.8 ms on this Mac, below the 50 ms budget. Local timings do not predict scorer timings.

Measured starter result: 1.15, receipt BB-5FF74C07. Next: check and submit the movement experiment, then compare its score.

## How the bot works

The server sends observations, and `example_bot.py` returns an action. `mechfight.py` handles reading and writing messages so the strategy can focus on decisions.

- `self` describes our robot, including its position, health, energy and weapons.
- `zone.next_center` is the center of the next playable circle. The baseline walks directly toward it; our navigator balances relocation with nearby threats.
- `math.atan2` converts the difference between two positions into a direction angle. Cosine and sine turn that angle into east/north movement.
- `near` finds weapon pickups within horizontal collection distance. The starter tries to collect one when its second slot is empty. This logic still needs improvement: collection also has a height limit.
- `enemies` sorts visible enemy mechs by distance. The starter aims at the nearest one and holds both triggers. Different weapons need different firing logic, so this is another future improvement.
- `tick` echoes the observation number. Without it, the server cannot match our decision to the observation.
- `mf.draw` adds debugging information. These drawings do not improve performance or appear in the public replay.

Passing the conformance check means the program follows the communication rules and responds in time. It does not prove the strategy wins matches. The supplied observations do not change in response to our actions.

## Run the supplied checks

From the parent workspace, with the official kit in `mechfight-kit/`:

```sh
python3 mechfight-kit/check/check.py -- python3 -u mech-royale/example_bot.py
docker build --platform linux/amd64 -t afia-mech:starter mech-royale
python3 mechfight-kit/check/check.py --map-dir /arena -- docker run --rm -i --platform linux/amd64 --network none --cpus 1 --memory 512m --read-only --tmpfs /tmp:rw,size=64m --user 65534:65534 -v "$PWD/mechfight-kit/arena:/arena:ro" afia-mech:starter
```

Apple Silicon runs the Intel image through emulation locally. Local timings do not predict timings on the scorer's Intel machine.

## Submission

The repository must be public with `Dockerfile` at its root. Submit its URL and a commit on the track page. Keep submitted commits available through results. Maximum repository size: 20 MB at the submitted commit. The map is provided by the scorer, so it is not bundled here.

Cutoff: Sunday November 22, 2026 at 10 AM Central. Four submissions per hour under the released track rules.

Official rules: https://www.joinbuilders.org/buildathon/tracks/builders

The supplied `protocol.md` is the full game specification. Read live configuration values instead of assuming the default numbers never change. Run focused navigation checks with `python3 -m unittest -v test_navigation`.
