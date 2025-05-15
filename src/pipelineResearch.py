#!/usr/bin/env python3

from pipeline9 import MakeAppender, Pipeline

class SeveralRunsPipeline(Pipeline):
    def __init__(self, steps, runs=1):
        super().__init__(steps)
        self.original_steps = steps.copy()
        self.steps = steps.copy()
        self.runs = runs

    def run_chained(self, s: str) -> str:
        current = s
        for _ in range(self.runs):
            for step in self.steps:
                current = step.process(current)
                print(current)
        return current
    def run_independent(self, s):
        for _ in range(self.runs):
            for step in self.steps:
                s = step.process(s)
                print(s)
        return s


def main():
    # make two pipelines with different numbers of MakeAppender steps
    steps = [MakeAppender('e')]
    steps2 = [MakeAppender('e')]
    pipeline = SeveralRunsPipeline(steps, runs=5)
    pipeline2 = SeveralRunsPipeline(steps2, runs=7)

    # any string for testing
    input_str = "BDR"
    print(f"Starte Pipelines mit Eingabe: {input_str}")

    run_and_compare_pipelinelengths(pipeline, pipeline2, input_str)
def compare_pipeline_results(result:str, result2:str)->int:
    # which one is longer?
    return len(result) - len(result2)

def run_and_compare_pipelinelengths(pipeline:str, pipeline2:str, input_str:str, comparer=compare_pipeline_results):
    # run the pipelines
    pipelineresult1 = pipeline.run_chained(input_str)
    pipelineresult2 = pipeline2.run_chained(input_str)

    result = comparer(pipelineresult1, pipelineresult2)

    if result > 0:
        print(f"Pipeline 1 ({len(pipelineresult1)} chars) is longer than Pipeline 2 ({len(pipelineresult2)} chars).")
    elif result < 0:
        print(f"Pipeline 2 ({len(pipelineresult2)} chars) is longer than Pipeline 1 ({len(pipelineresult1)} chars).")
    else:
        print(f"Both pipelines produced results of equal length: {len(pipelineresult1)} chars.")



if __name__ == "__main__":
    main()
