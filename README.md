[# Search Algorithms in Python: Starter Repository

Starter code and tests for the search algorithms worksheet (Chapter 3, Sections 3.3–3.4). You will implement breadth-first, depth-first, and best-first search, then choose the right one for three problems.

## Setup

You need Python 3.8 or newer.

```
python -m pip install -r requirements.txt
```

## What's here

| File | What you do with it |
| --- | --- |
| `search.py` | The problem and node framework, plus a road map of western Pennsylvania. **Parts 1–3:** fill in `breadth_first_search`, `depth_first_search`, and `best_first_search` at the bottom. |
| `problems.py` | **Part 4:** finish the knight and queens formulations, and fill in `solve_ambulance`, `solve_knight`, and `solve_queens` with the search you choose. |





## The map

Instead of the textbook's Romania map, this repository uses 24 towns in western Pennsylvania and the 49 main roads between them, with Indiana as the starting point. Each road's length is the real driving distance in miles between town centers, from the OpenStreetMap routing engine ([OSRM](https://project-osrm.org/)), rounded to the nearest mile. Like Figure 3.1 it is simplified to main highways, so a few real trips are a little shorter than the map allows.
](https://github.com/DrGrieggs/405-Search-Starter.git)
