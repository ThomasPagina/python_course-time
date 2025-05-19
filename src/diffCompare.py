#!/usr/bin/env python3
"""
infer_version_order.py

Ermittelt eine wahrscheinliche Reihenfolge mehrerer
Dateisnapshots desselben Quell­codes nur anhand des Text­inhalts.

Nutzung:
    python infer_version_order.py [pfad_zum_ordner]

Idee
-----
1. Jede Datei als String einlesen
2. Für jedes Paar die Ähnlichkeit   sim = SequenceMatcher(...).ratio()
   -> Distanz  d = 1 - sim
3. Den Snapshot mit der *geringsten* durchschnittlichen Ähnlichkeit
   zu allen anderen als wahrscheinlich ältesten wählen.
4. Greedy-Pfad: Immer die noch nicht besuchte Datei mit
   der *größten* Ähnlichkeit (kleinster d) an die aktuelle anhängen.
Das entspricht grob einer Approximation des „kürzesten Pfads“
durch alle Versionen (TSP-Heuristik).
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

    print("⮕ Vermutete Reihenfolge (alt → neu):")
    for i, f in enumerate(order, 1):
        print(f"  {i:02} {f.name}   ⌀-Ähnlichkeit {avg[f]:.3f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "./data")
