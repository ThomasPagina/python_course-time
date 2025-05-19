#!/usr/bin/env python3
"""
infer_version_order.py

Determines a probable order of multiple
file snapshots of the same source code based only on the text content.

Usage:
    python infer_version_order.py [path_to_folder]

Idea
-----
1. Read each file as a string
2. For each pair, compute similarity   sim = SequenceMatcher(...).ratio()
   -> Distance  d = 1 - sim
3. Select the snapshot with the *lowest* average similarity
   to all others as the likely oldest.
4. Greedy path: Always append the not-yet-visited file with
   the *highest* similarity (smallest d) to the current one.
This roughly corresponds to an approximation of the "shortest path"
through all versions (TSP heuristic).
"""
import sys, glob, difflib, itertools, statistics, pathlib

def load_files(folder: str):
    files = sorted(pathlib.Path(folder).glob("*.py"))
    if not files:
        raise SystemExit(f"Keine *.py-Dateien in {folder} gefunden.")
    return files, {f: f.read_text(encoding="utf-8", errors="ignore") for f in files}

def pairwise_similarity(files, texts):
    sim = {(a, b): difflib.SequenceMatcher(None, texts[a], texts[b]).ratio()
           for a, b in itertools.permutations(files, 2) if a != b}
    return sim

def greedy_order(files, sim):
    # 1) ältesten Kandidaten wählen – geringster mittlerer sim-Wert
    avg = {f: statistics.mean(sim[(f, g)] for g in files if g != f) for f in files}
    current = min(avg, key=avg.get)
    order = [current]
    remaining = set(files) - {current}

    # 2) Greedy durch die ähnlichste nächste Version
    while remaining:
        nxt = max(remaining, key=lambda g: sim[(current, g)])
        order.append(nxt)
        remaining.remove(nxt)
        current = nxt
    return order, avg

def main(folder="./data"):
    files, texts = load_files(folder)
    sim = pairwise_similarity(files, texts)
    order, avg = greedy_order(files, sim)

    print("⮕ probable order (old → new):")
    for i, f in enumerate(order, 1):
        print(f"  {i:02} {f.name}   ⌀-similarity {avg[f]:.3f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "./data")
