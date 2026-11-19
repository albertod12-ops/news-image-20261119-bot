# news-image-20261119-bot

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/albertod12-ops/news-image-20261119-bot/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/albertod12-ops/news-image-20261119-bot/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Thursday 19 November 2026: 36 stories, 7 regions, one picture — an entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261119) "Sum up 19 November's world news in one image".

The program is `main.py` (Python 3.13). It copies the finished front page, `entry.png` (1024x1024, under 1 MiB), to the grader's output directory, byte for byte, with no network access and no randomness. Run it twice and both runs write the same bytes.

The front page is built by `draw.py` (Pillow, DejaVu fonts, a world map from `world.geo.json`): a navy masthead, three hero stories with flat-vector illustrations (the Shenzhen summit, GTA VI, the Anthropic IPO), ten small cards with pictures (the ICJ ruling, COP31, Cyclone Akvan, Ukraine, APEC, Florida, the Suneung exam, Colombia, Australia, Libya), a BY THE NUMBERS strip, a world map with numbered pins, and 23 more stories. Every story happened, or was first reported, on Thursday 19 November 2026. Sources: Reuters, AP, AFP, Yonhap, IMD, ICJ, SEC, ABS. Original illustrations.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=rbvcjbg9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
