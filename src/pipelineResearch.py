#!/usr/bin/env python3

from pipeline9 import MakeAppender, Pipeline

def main():
    # make two pipelines with different numbers of MakeAppender steps
    steps = [MakeAppender('e') for _ in range(5)]
    steps2 = [MakeAppender('e') for _ in range(7)]
    pipeline = Pipeline(steps)
    pipeline2 = Pipeline(steps2)

    # any string for testing
    input_str = "BDR"
    print(f"Starte Pipelines mit Eingabe: {input_str}")

    # run the pipelines
    result = pipeline.run_chained(input_str)
    result2 = pipeline2.run_chained(input_str)

    #which one is longer?
    if len(result) > len(result2):
        print(f"Pipeline 1 (5 Appender) Ergebnis: {result} ist länger als Pipeline 2 (7 Appender) Ergebnis: {result2}")
    elif len(result) < len(result2):
        print(f"Pipeline 2 (7 Appender) Ergebnis: {result2} ist länger als Pipeline 1 (5 Appender) Ergebnis: {result}")
    else:
        print(f"Beide Ergebnisse sind gleich lang: {len(result)} Zeichen.")

    

if __name__ == "__main__":
    main()
