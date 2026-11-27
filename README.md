# The World in One Day — 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b176-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b176-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up world news on **Thursday 26 November 2026**: 50 stories
across 10 regions — the Macy's 100th Thanksgiving Parade postponed by storm,
the IRGC claim of two tankers hit by mines in the Strait of Hormuz, and the
global market rebound after the Trump tariff salvo.

## Contents

- `entry.png` — the finished image (1024×1024, under 1 MiB).
- `gen.py` — the build-time renderer (Pillow). Run `python3 gen.py` to
  regenerate `entry.png` from scratch.
- `main.py` — the grader entry point (standard library only). It copies
  `entry.png` into `MAKEFUN_OUTPUT_DIR`.

## Verification

- `entry.png` SHA-256: `6dcd2ce38698bc00f4162d7da091a369f44db3955869a7af28b33eff4556e348`
- Size: 193,530 bytes, 1024×1024 px.
- Stories: 3 heroes + 10 cards + 37 ALSO items = 50; regions: 10
  (North America, South America, Western Europe, Eastern Europe, Middle East,
  North Africa, Sub-Saharan Africa, East Asia, Southeast Asia, Oceania).
- Date check: the image carries a DATE CHECK strip listing the seven stories
  deliberately excluded because they happened on 22/24/25 November, not
  26 November (COP31, Shenzhou-24, Cairo tanker, Cartagena hostages,
  Australia–Solomon pact, UK energy +26%, Huawei verdict).
- Stdlib simulation: run in a venv without Pillow, from a different working
  directory, with an empty output directory and a read-only copy of the repo;
  `main.py` exits 0 and the copied file's SHA-256 matches the one above.

## License

MIT — see `LICENSE`.
