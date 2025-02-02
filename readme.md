# AADT Dance Matching Algorithm

AADT dance matching algorithm.

The algorithm runs in two (or 3) phases:
- Phase 1: Matching each dancer to one of their top 3 preferences. This should be guaranteed.
- Phase 2: For any dancers that signed up for multiple dances, assign their remaining dances to the heighest preferences
- Phase 3 (Optional): For any de-prioritized dancers, assign them their dances according to whichever dances still have space.


## Installation

We recommend setting up a Python virtual env first:

```bash
python3 -m venv venv
source venv/bin/activate
```

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

Make sure you have two files in this folder: `dancer_preferences.csv` and `dances.csv`. Then run:
```bash
python3 aadt.py dancer_preferences.csv dances.csv
```