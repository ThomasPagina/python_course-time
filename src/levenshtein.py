import pipeline9
from pipeline9 import PipelineStep, Pipeline

# Neue Pipeline-Schritte definieren
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
            op_choice = ('match', None)
            if cost != 0:
                op_choice = ('substitute', target[j-1])
            if del_cost < dp[i][j]:
                dp[i][j] = del_cost
                op_choice = ('delete', None)
            if ins_cost < dp[i][j]:
                dp[i][j] = ins_cost
                op_choice = ('insert', target[j-1])
            op[i][j] = op_choice

    i, j = m, n
    ops = []
    while i > 0 or j > 0:
        action, arg = op[i][j]
        if action == 'match':
            i -= 1; j -= 1; continue
        if action == 'substitute':
            ops.append(('substitute', arg, i-1))
            i -= 1; j -= 1
        elif action == 'delete':
            ops.append(('delete', None, i-1))
            i -= 1
        elif action == 'insert':
            ops.append(('insert', arg, j-1))
            j -= 1
    ops.reverse()
    return dp[m][n], ops

# Demonstration
if __name__ == "__main__":
    source = "Haustier"
    target = "Mausstier"

    # Grundpfad ermitteln
    distance, ops = levenshtein_path(source, target)
    print(f"Levenshtein-Distanz: {distance}")
    print("Operationen (ohne Rotation):", ops)

    # Konvertiere Grund-ops in Pipeline-Schritte mit Rotation
    current = source
    steps = []
    for action, arg, idx in ops:
        if action == 'substitute':
            # Substitute: bring char at idx to end, swap, then zurückrotieren
            t = (idx + 1) % len(current)
            for _ in range(t):
                steps.append(Move()); current = Move().process(current)
            steps.append(Swap(arg)); current = Swap(arg).process(current)
            back = (len(current) - t) % len(current)
            for _ in range(back):
                steps.append(Move()); current = Move().process(current)

        elif action == 'delete':
            # Delete: bring char at idx to end, delete, zurückrotieren
            t = (idx + 1) % len(current)
            for _ in range(t):
                steps.append(Move()); current = Move().process(current)
            steps.append(Delete()); current = Delete().process(current)
            L = len(current)
            back = (L + 1 - t) % L if L > 0 else 0
            for _ in range(back):
                steps.append(Move()); current = Move().process(current)

        elif action == 'insert':
            # Insert: bring Einfügeposition idx an Anfang, add, zurückrotieren
            t = idx % (len(current) + 1)
            for _ in range(t):
                steps.append(Move()); current = Move().process(current)
            steps.append(Add(arg)); current = Add(arg).process(current)
            for _ in range(t):
                steps.append(Move()); current = Move().process(current)

    print("Pipeline-Schritte mit Rotation:", steps)

    # Pipeline ausführen und prüfen
    pipeline = Pipeline(steps)
    result = pipeline.run_chained(source)
    assert result == target, f"Erwartet '{target}', erhalten '{result}'"
    print("Transformation erfolgreich: ", result)

    # Graph der Pipeline ausgeben
    graph = pipeline.visualize("levenshtein_pipeline", format='png')
    graph.view()

    # Rotation demonstrieren
    print("\nRotation von 'Katze':")
    rot = Move()
    s = "Katze"
    for _ in range(3):
        s = rot.process(s)
        print(s)
