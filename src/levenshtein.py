import pipeline9
from pipeline9 import PipelineStep, Pipeline

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

    # Rückverfolgung
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

# Demo: Baue Pipeline-Schritte mit Rotation und teste
def build_and_run(source: str, target: str):
    Add, Delete, Swap, Move = define_pipeline_steps()
    distance, ops = levenshtein_path(source, target)
    print(f"Levenshtein-Distanz: {distance}")
    print("Levenshtein-Operationen:", ops)

    current = source
    steps = []
    for action, arg, idx in ops:
        L = len(current)
        if action in ('substitute', 'delete'):
            # Operation am idx: Rotate nach links, sodass idx am Ende liegt
            t = (idx + 1) % L
            for _ in range(t):
                steps.append(Move()); current = Move().process(current)

            # Führe Operation aus
            if action == 'substitute':
                steps.append(Swap(arg)); current = Swap(arg).process(current)
            else:  # 'delete'
                steps.append(Delete()); current = Delete().process(current)

            # Nach Delete ist Länge L-1
        elif action == 'insert':
            # Einfügeposition idx => idx = Position in target
            # Rotieren idx Mal, so dass Position ans Ende kommt
            L = len(current)
            t = (idx) % (L + 1)
            for _ in range(t):
                steps.append(Move()); current = Move().process(current)
            steps.append(Add(arg)); current = Add(arg).process(current)

    # Abschließende Korrektur: Finde k, sodass rotate_left(current, k) == target
    if current != target:
        L = len(current)
        for k in range(1, L+1):
            rot = current[k % L:] + current[:k % L]
            if rot == target:
                for _ in range(k):
                    steps.append(Move())
                current = target
                break

    print("Pipeline-Schritte mit Rotation:", steps)
    pipeline = Pipeline(steps)
    result = pipeline.run_chained(source)
    assert result == target, f"Erwartet '{target}', erhalten '{result}'"
    print("Transformation erfolgreich:", result)
    # Graph ausgeben
    graph = pipeline.visualize("levenshtein_pipeline", format='png')
    graph.view()

if __name__ == "__main__":
    # Test-Fälle
    for src, tgt in [("Haus", "Maus"), ("Haustier", "Mausstier"), ("Haustierl", "Mausstier")]:
        print(f"\n=== {src} -> {tgt} ===")
        build_and_run(src, tgt)

    # Rotation demonstrieren
    Add, Delete, Swap, Move = define_pipeline_steps()
    print("\nRotation von 'Katze':")
    s = "Katze"
    for _ in range(3):
        s = Move().process(s)
        print(s)
