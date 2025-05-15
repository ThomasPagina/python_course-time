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
  
    pipeline1 = SeveralRunsPipeline(steps, runs=5)
    pipeline2 = SeveralRunsPipeline(steps, runs=7)

    # any string for testing
    input_str1 = "BDR"
    input_str2 = "DDR"
    print(f"Start Pipelines with input: {input_str1} and {input_str2}")

    run_and_compare_pipelines(pipeline1, pipeline2, input_str1, input_str2, comparer=compare_pipeline_results_tail_length)
def compare_pipeline_results_length(result:str, result2:str)->int:
    # which one is longer?
    return len(result) - len(result2)
def tail_length(result:str, tail_letter='e')->int:
    # how long is the tail? count the number of letters of 'tail_letter' at the end of the string
    return len(result) - len(result.rstrip(tail_letter))

def compare_pipeline_results_tail_length(result:str, result2:str,tail_letter='e')->int:
    # which one has the longer tail?
    return tail_length(result, tail_letter) - tail_length(result2, tail_letter)


def run_and_compare_pipelines(pipeline:str, pipeline2:str, input_str1:str, input_str2:str, comparer=compare_pipeline_results_tail_length):
    # run the pipelines
    pipelineresult1 = pipeline.run_chained(input_str1)
    pipelineresult2 = pipeline2.run_chained(input_str2)

    result = comparer(pipelineresult1, pipelineresult2)

    if result > 0:
        print(f"Pipeline 1 ({len(pipelineresult1)} chars) is longer than Pipeline 2 ({len(pipelineresult2)} chars).")
    elif result < 0:
        print(f"Pipeline 2 ({len(pipelineresult2)} chars) is longer than Pipeline 1 ({len(pipelineresult1)} chars).")
    else:
        print(f"Both pipelines produced results of equal length: {len(pipelineresult1)} chars.")



if __name__ == "__main__":
    main()
