# Afia's Mech Royale bot

Python entry for the OSU Builders Buildathon, November 20–22, 2026.

Current version: the unmodified official example bot. We are establishing a working baseline before changing its decisions. No match score has been measured yet.

## Setup results, November 20

- Direct Python conformance check: PASS, all 300 observations answered on time, no bad lines or wrong ticks.
- Docker builds: succeeded for linux/amd64 (competition architecture) and linux/arm64 (local architecture).
- Docker conformance checks: not passed locally. Both container startups exceeded the 20-second ready limit. Even a minimal Intel Python command stalled before producing output; the diagnostic containers remained in Created state. This suggests a Docker startup issue, but its cause is not yet established. This is not evidence that the competition image will pass on the scorer.
- The base image is pinned by digest for reproducible builds. Only the two runtime Python files are copied into the image.

Next: resolve container startup, then measure the unchanged starter's practice score before claiming any strategy improvement.

## How the bot works

The server sends observations, and `example_bot.py` returns an action. `mechfight.py` handles reading and writing messages so the strategy can focus on decisions.

- `self` describes our robot, including its position, health, energy and weapons.
- `zone.next_center` is the center of the next playable circle. The example walks toward it so the shrinking zone does not leave it behind.
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

The supplied `protocol.md` is the full game specification. Read live configuration values instead of assuming the default numbers never change.
