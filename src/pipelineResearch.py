#!/usr/bin/env python3

from pipeline9 import MakeAppender, Pipeline, PipelineStep
import random
from typing import List 
import math

class SeveralRunsPipeline(Pipeline):
    def __init__(self, steps: List[PipelineStep], runs: int = 1):
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
    
class DefectivePipelineStepCopyText(PipelineStep):
    def process(self, text: str) -> str:
        # change any random letter to '_'
        if not text:
            return text
        index = random.randint(0, len(text) - 1)
        return text[:index] + '_' + text[index + 1:]

class DefectivePipelineStepRadiactiveCopyText(PipelineStep):
    def process(self, text: str) -> str:
        # change half the letters randomly to '_'
        if not text:
            return text
        text_list = list(text)
        for i in range(len(text_list) // 2):
            index = random.randint(0, len(text_list) - 1)
            text_list[index] = '_'
        return ''.join(text_list)
        
def remaining_fraction_of_letter(text: str, letter: str = 'e') -> float:
    """
    returns the fraction of the text that is not the letter 'e'.
    """
    if not text:
        return 0.0
    p = text.count(letter) / len(text)
    return 1.0 - p

def estimate_runs_from_fraction(text: str, letter: str = 'e') -> float:
    """
    Schätzt, wie viele 'Runs' nötig gewesen wären, um 
    auf den aktuellen Anteil des Buchstabens zu kommen,
    unter der Annahme, dass jeden Run der Restanteil halbiert wird.
    
    Liefert eine reelle Zahl; für volle Läufe auf- oder abrunden.
    """
    if not text:
        return 0.0
    p = text.count(letter) / len(text)
    if p >= 1.0:
        return float('inf')  # unendlich viele Läufe
    return -math.log2(1.0 - p)

def compare_pipeline_results_length(result:str, result2:str)->int:
    # which one is longer?
    return len(result) - len(result2)
def compare_pipeline_results_count_of_letter(result:str, result2:str, letter='e')->int:
    # which one has more of the letter 'e'?
    return result.count(letter) - result2.count(letter)
def compare_pipeline_results_percentage_of_letter(result:str, result2:str, letter='e')->int:
    # which one has a higher percentage of the letter 'e'?
    return result.count(letter) / len(result) - result2.count(letter) / len(result2)
def compare_pipeline_results_remaining_fraction_of_letter(result:str, result2:str, letter='e')->int:
    # which one has a higher remaining fraction of the letter 'e'?
    return remaining_fraction_of_letter(result, letter) - remaining_fraction_of_letter(result2, letter)

def make_compare_pipeline_results_count_of_letter(letter='e'):
    def compare(result:str, result2:str)->int:
        return compare_pipeline_results_count_of_letter(result, result2, letter)
    return compare
def make_compare_pipeline_results_percentage_of_letter(letter='e'):
    def compare(result:str, result2:str)->int:
        return compare_pipeline_results_percentage_of_letter(result, result2, letter)
    return compare
def make_compare_pipeline_results_remaining_fraction_of_letter(letter='e'):
    def compare(result:str, result2:str)->int:
        return compare_pipeline_results_remaining_fraction_of_letter(result, result2, letter)
    return compare
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
        print(f"Pipeline 1  took ({result} more runs than Pipeline 2).")
    elif result < 0:
        print(f"Pipeline 2 took ({-result} more runs than Pipeline 1).")
    else:
        print(f"Both pipelines run the same time.")

def checkAppender():
    # make two pipelines with different numbers of MakeAppender steps
    steps = [MakeAppender('e')]

    pipeline1 = SeveralRunsPipeline(steps, runs=5)
    pipeline2 = SeveralRunsPipeline(steps, runs=7)

    # any string for testing
    input_str1 = "South Africa is a country on the southernmost tip of the African continent."
    input_str2 = "Angola is a country in Southern Africa. It is bordered by Namibia to the south, Zambia to the east, and the Democratic Republic of the Congo to the north."
    print(f"Start Pipelines with input: {input_str1} and {input_str2}")

    run_and_compare_pipelines(pipeline1, pipeline2, input_str1, input_str2, comparer=compare_pipeline_results_count_of_letter('_'))
    
def check_defective_pipeline_step():
    # make two pipelines with different numbers of DefectivePipelineStepCopyText steps
    steps = [DefectivePipelineStepCopyText()]

    pipeline1 = SeveralRunsPipeline(steps, runs=5)
    pipeline2 = SeveralRunsPipeline(steps, runs=7)

    # any string for testing
    input_str1 = "South Africa is a country on the southernmost tip of the African continent."
    input_str2 = "Angola is a country in Southern Africa. It is bordered by Namibia to the south, Zambia to the east, and the Democratic Republic of the Congo to the north."
    print(f"Start Pipelines with input: {input_str1} and {input_str2}")

    run_and_compare_pipelines(pipeline1, pipeline2, input_str1, input_str2, comparer=make_compare_pipeline_results_remaining_fraction_of_letter('_'))

def check_defective_pipeline_step_radiative():
    # make two pipelines with different numbers of DefectivePipelineStepRadiactiveCopyText steps
    steps = [DefectivePipelineStepRadiactiveCopyText()]

    pipeline1 = SeveralRunsPipeline(steps, runs=5)
    pipeline2 = SeveralRunsPipeline(steps, runs=7)

    # any string for testing
    input_str1 = "South Africa is a country on the southernmost tip of the African continent."
    input_str2 = "Angola is a country in Southern Africa. It is bordered by Namibia to the south, Zambia to the east, and the Democratic Republic of the Congo to the north."
    print(f"Start Pipelines with input: {input_str1} and {input_str2}")

    run_and_compare_pipelines(pipeline1, pipeline2, input_str1, input_str2, comparer=make_compare_pipeline_results_percentage_of_letter('_'))

if __name__ == "__main__":
    check_defective_pipeline_step_radiative()
