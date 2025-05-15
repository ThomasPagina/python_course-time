#!/usr/bin/env python3

from pipeline9 import MakeAppender, Pipeline

def main():
    # Erstelle eine Pipeline mit 5 Appendern, die jeweils ein 'e' anfügen
    steps = [MakeAppender('e') for _ in range(5)]
    pipeline = Pipeline(steps)

    # Beispiel-Eingabestring
    input_str = "BDR"
    print(f"Starte Pipeline mit Eingabe: {input_str}")

    # Ausführung der Pipeline (verkettet: jeder Schritt nimmt das Ergebnis des vorherigen)
    result = pipeline.run_chained(input_str)

    print(f"Endergebnis: {result}")

if __name__ == "__main__":
    main()
