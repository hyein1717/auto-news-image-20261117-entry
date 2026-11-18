# 17 November 2026 — The World in One Day

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/hyein1717/auto-news-image-20261117-entry/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/hyein1717/auto-news-image-20261117-entry/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Entry for the [make.fun](https://make.fun/bounty/news-image-20261117)
"Sum up 17 November's world news in one image" bounty (news-image-20261117).

A newspaper front page for Tuesday 17 November 2026 (1024×1024 PNG): the
date in huge type, one dramatic hero photo of the day's biggest story, and
five labelled stories across regions and fields — all typeset crisply with
PIL + shipped DejaVu fonts so nothing is garbled and the page stays legible
even at ~300px.

## Stories shown (all verified against 17 Nov 2026 reporting)

1. **Kerch Bridge hit** — Ukraine strikes the Crimea bridge a second day
   running; a road span collapses. Russia hits a river-crossing bridge in Kyiv.
2. **Gulf on edge** — A tanker hits a mine near the Strait of Hormuz;
   Iranian drones are fired at a US radar site in Bahrain (intercepted,
   no casualties, per Bahrain).
3. **ASEAN in Manila** — Trump arrives for the ASEAN summit and signs a
   joint trade statement with Thailand; a Xi–Trump–Putin three-way meeting
   is confirmed for Thursday 19 Nov in Shenzhen.
4. **Vulcan rocket lost** — ULA's Vulcan fails in flight; 40 Amazon Leo
   internet satellites destroyed.
5. **Nvidia reports** — First earnings since Jensen Huang stepped down.
6. Also: JPMorgan blames a software bug (not a cyberattack) for Monday's
   banking glitch; the UK sanctions 8 firms over West Bank settlements.

## Program

`main.py` (Python 3.13, stdlib + Pillow for the image work) composes the
front page from `assets/hero.jpg` and the shipped fonts, then applies the
playbook post-processing — resize 1024×1024 LANCZOS, Sharpness 1.18,
Contrast 1.08 — and writes `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output`). If Pillow is absent it copies the pre-rendered
`assets/page.png` instead. Deterministic: both runs write byte-identical
output.

## Run

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Writes `entry.png` (1024×1024, under 1 MiB) into the output directory.
