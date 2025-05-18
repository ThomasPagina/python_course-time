import pipeline9
from pipeline9 import PipelineStep, Pipeline

# Helfer-Funktion, um Move-Schritte mehrfach anzuwenden

def apply_moves(count: int, Move, steps: list, current: str) -> str:
    """Fügt count Mal einen Move-Schritt hinzu und rotiert current entsprechend."""
    for _ in range(count):
        step = Move()
        steps.append(step)
        current = step.process(current)
    return current

# Neue Pipeline-Schritte definieren
def define_pipeline_steps():
    class Add(PipelineStep):
        """Fügt am Ende einen Buchstaben hinzu"""
        def __init__(self, letter: str):
            self.letter = letter
        def process(self, s: str) -> str:
            return s + self.letter
        def __repr__(self) -> str:
            return f"Add({self.letter})"

    class Delete(PipelineStep):
        """Löscht den letzten Buchstaben"""
        def process(self, s: str) -> str:
            return s[:-1] if s else s
        def __repr__(self) -> str:
            return "Delete()"

    class Swap(PipelineStep):
        """Ersetzt den letzten Buchstaben durch einen neuen"""
        def __init__(self, letter: str):
            self.letter = letter
        def process(self, s: str) -> str:
            return (s[:-1] + self.letter) if s else s
        def __repr__(self) -> str:
            return f"Swap({self.letter})"

    class Move(PipelineStep):
        """Rotiert den String um eine Position nach links"""
        def process(self, s: str) -> str:
            return (s[1:] + s[0]) if s else s
        def __repr__(self) -> str:
            return "Move()"

    return Add, Delete, Swap, Move

# Funktion zur Berechnung der Levenshtein-Distanz und Pfad (ohne Move)
def levenshtein_path(source: str, target: str):
    m, n = len(source), len(target)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    op = [[None] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = i
        op[i][0] = ('delete', None)
    for j in range(1, n + 1):
        dp[0][j] = j
        op[0][j] = ('insert', target[j-1])

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if source[i-1] == target[j-1] else 1
            sub_cost = dp[i-1][j-1] + cost
            del_cost = dp[i-1][j] + 1
            ins_cost = dp[i][j-1] + 1
            dp[i][j] = sub_cost
            op_choice = ('match', None) if cost == 0 else ('substitute', target[j-1])
            if del_cost < dp[i][j]:
                dp[i][j] = del_cost
                op_choice = ('delete', None)
            if ins_cost < dp[i][j]:
                dp[i][j] = ins_cost
                op_choice = ('insert', target[j-1])
            op[i][j] = op_choice

    i, j, ops = m, n, []
    while i > 0 or j > 0:
        action, arg = op[i][j]
        if action == 'match':
            i, j = i-1, j-1
            continue
        if action == 'substitute':
            ops.append(('substitute', arg, i-1))
            i, j = i-1, j-1
        elif action == 'delete':
            ops.append(('delete', None, i-1))
            i -= 1
        elif action == 'insert':
            ops.append(('insert', arg, j-1))
            j -= 1
    ops.reverse()
    return dp[m][n], ops

# Demo: Baue Pipeline mit Rotation und teste
def build_and_run(source: str, target: str):
    Add, Delete, Swap, Move = define_pipeline_steps()
    distance, ops = levenshtein_path(source, target)
    print(f"Levenshtein-Distanz: {distance}")
    print("Levenshtein-Operationen:", ops)

    current = source
    steps = []
    for action, arg, idx in ops:
        if action in ('substitute', 'delete'):
            # Vorrotation zum Ende der Zielposition
            t = (idx + 1) % len(current)
            current = apply_moves(t, Move, steps, current)

            # Operation ausführen
            if action == 'substitute':
                step = Swap(arg)
                steps.append(step)
                current = step.process(current)
            else:
                step = Delete()
                steps.append(step)
                current = step.process(current)

            # Rückrotation
            back = (len(current) - t) % len(current) if current else 0
            current = apply_moves(back, Move, steps, current)

        elif action == 'insert':
            t = idx % (len(current) + 1)
            current = apply_moves(t, Move, steps, current)
            step = Add(arg)
            steps.append(step)
            current = step.process(current)
            back = (len(current) - t) % len(current)
            current = apply_moves(back, Move, steps, current)

    # Fallback finale Rotation
    if current != target:
        for _ in range(len(current)):
            current = apply_moves(1, Move, steps, current)
            if current == target:
                break

    print("Pipeline-Schritte mit Rotation:", steps)
    pipeline = Pipeline(steps)
    result = pipeline.run_chained(source)
    assert result == target, f"Erwartet '{target}', erhalten '{result}'"
    print("Transformation erfolgreich:", result)
    graph = pipeline.visualize("levenshtein_pipeline", format='png')
    graph.view()

if __name__ == "__main__":
    # Test-Fälle
    for src, tgt in [("Haus", "Maus"),
                     ("Haustier", "Mausstier"),
                     ("Haustierl", "Mausstier"),
                     ("Katzenfutter", "Hundemutter"),]:
        print(f"\n=== {src} -> {tgt} ===")
        build_and_run(src, tgt)


