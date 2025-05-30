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
        for run_idx in range(self.runs):
            for step in self.steps:
                current = step.process(current)
        return current

    def run_independent(self, s: str) -> List[str]:
        results = []
        for step in self.original_steps:
            current = s
            for run_idx in range(self.runs):
                current = step.process(current)
                print(f"{step.__class__.__name__} run {run_idx+1}: {current}")
            results.append(current)
        return results

class DefectivePipelineStepCopyText(PipelineStep):
    def process(self, text: str) -> str:
        if not text:
            return text
        index = random.randrange(len(text))
        return text[:index] + '_' + text[index+1:]

class DefectivePipelineStepRadiactiveCopyText(PipelineStep):
    def process(self, text: str) -> str:
        if not text:
            return text
        text_list = list(text)
        letter_indices = [
            i for i, ch in enumerate(text_list)
            if ch.isalpha() and ch != '_'
        ]
        num_to_replace = len(letter_indices) // 2
        for idx in random.sample(letter_indices, num_to_replace):
            text_list[idx] = '_'
        return ''.join(text_list)

class DecayPipelineStep(PipelineStep):
    def __init__(self, decay_char: str = '_', decay_rate: float = 0.1):
        self.decay_char = decay_char
        self.decay_rate = decay_rate

    def process(self, text: str) -> str:
        indices = [i for i, c in enumerate(text) if c != self.decay_char]
        if not indices:
            return text
        num_to_decay = max(1, int(len(indices) * self.decay_rate))
        to_decay = set(random.sample(indices, num_to_decay))
        return ''.join(
            self.decay_char if i in to_decay else c
            for i, c in enumerate(text)
        )

def remaining_fraction_of_letter(text: str, letter: str = 'e') -> float:
    if not text:
        return 0.0
    p = text.count(letter) / len(text)
    return 1.0 - p

def estimate_runs_from_fraction(text: str, letter: str = 'e') -> float:
    L = len(text)
    if L == 0:
        raise ValueError("Output must be non-empty.")
    u = text.count(letter)
    remaining = L - u
    if remaining <= 0:
        raise ValueError(f"No letters remain (all {letter}); infinite or undefined runs.")
    frac = remaining / L
    return -math.log2(frac)

def compare_pipeline_results_length(result1: str, result2: str) -> int:
    return len(result1) - len(result2)

def compare_pipeline_results_count_of_letter(result1: str, result2: str, letter: str = 'e') -> int:
    return result1.count(letter) - result2.count(letter)

def compare_pipeline_results_percentage_of_letter(result1: str, result2: str, letter: str = 'e') -> int:
    return result1.count(letter)/len(result1) - result2.count(letter)/len(result2)

def compare_pipeline_results_remaining_fraction_of_letter(result1: str, result2: str, letter: str = 'e') -> int:
    return remaining_fraction_of_letter(result1, letter) - remaining_fraction_of_letter(result2, letter)

def make_compare_pipeline_results_count_of_letter(letter: str = 'e'):
    def compare(result1: str, result2: str) -> int:
        return compare_pipeline_results_count_of_letter(result1, result2, letter)
    return compare

def make_compare_pipeline_results_percentage_of_letter(letter: str = 'e'):
    def compare(result1: str, result2: str) -> int:
        return compare_pipeline_results_percentage_of_letter(result1, result2, letter)
    return compare

def make_compare_pipeline_results_remaining_fraction_of_letter(letter: str = 'e'):
    def compare(result1: str, result2: str) -> int:
        return compare_pipeline_results_remaining_fraction_of_letter(result1, result2, letter)
    return compare

def make_compare_pipeline_results_estimate_runs_from_fraction(letter: str = 'e'):
    def compare(result1: str, result2: str) -> int:
        return round(estimate_runs_from_fraction(result1, letter)) - round(estimate_runs_from_fraction(result2, letter))
    return compare

def tail_length(text: str, tail_letter: str = 'e') -> int:
    return len(text) - len(text.rstrip(tail_letter))

def compare_pipeline_results_tail_length(result1: str, result2: str, tail_letter: str = 'e') -> int:
    return tail_length(result1, tail_letter) - tail_length(result2, tail_letter)

def run_and_compare_pipelines(
    pipeline1: Pipeline,
    pipeline2: Pipeline,
    input_str1: str,
    input_str2: str,
    comparer
) -> None:
    print("Running first pipeline...")
    result1 = pipeline1.run_chained(input_str1)
    print("Running second pipeline...")
    result2 = pipeline2.run_chained(input_str2)
    comp = comparer(result1, result2)

    if comp > 0:
        print("First pipeline is longer based on comparer.")
    elif comp < 0:
        print("Second pipeline is longer based on comparer.")
    else:
        print("Both pipelines perform equally based on the comparer.")

def check_appender():
    steps = [MakeAppender('e')]
    pipeline1 = SeveralRunsPipeline(steps, runs=5)
    pipeline2 = SeveralRunsPipeline(steps, runs=7)
    input_str1 = (
        "South Africa is a country on the southernmost tip of the African continent. "
        "It is known for its diverse culture and history."
    )
    input_str2 = (
        "Angola is a country in Southern Africa. It is bordered by Namibia to the south,"
        " Zambia to the east, and the Democratic Republic of the Congo to the north."
    )
    print(f"Start Pipelines with input: {input_str1} and {input_str2}")
    run_and_compare_pipelines(
        pipeline1,
        pipeline2,
        input_str1,
        input_str2,
        comparer=make_compare_pipeline_results_count_of_letter('e')
    )

def check_defective_pipeline_step():
    steps = [DefectivePipelineStepCopyText()]
    pipeline1 = SeveralRunsPipeline(steps, runs=2)
    pipeline2 = SeveralRunsPipeline(steps, runs=3)
    input_str1 = (
        "South Africa is a country on the southernmost tip of the African continent."
    )
    input_str2 = (
        "Angola is a country in Southern Africa. It is bordered by Namibia to the south,"
        " Zambia to the east, and the Democratic Republic of the Congo to the north."
    )
    print(f"Testing defective\nStart Pipelines with input: {input_str1} and {input_str2}")
    run_and_compare_pipelines(
        pipeline1,
        pipeline2,
        input_str1,
        input_str2,
        comparer=make_compare_pipeline_results_count_of_letter('_')
    )

def check_defective_pipeline_step_radiative():
    steps = [DefectivePipelineStepRadiactiveCopyText()]
    pipeline1 = SeveralRunsPipeline(steps, runs=2)
    pipeline2 = SeveralRunsPipeline(steps, runs=4)
    input_str1 = (
        "South Africa is a country on the southernmost tip of the African continent. "
        "It is known for its diverse culture and history. There are many languages spoken in South Africa, "
        "including Zulu, Xhosa, Afrikaans, and English."
    )
    input_str2 = (
        "Angola is a country in Southern Africa. It is bordered by Namibia to the south, Zambia to the east,"
        " and the Democratic Republic of the Congo to the north. Among the animals of this country are elephants,"
        " lions, and leopards. The capital city is Luanda."
    )
    print(f"Testing radiactive\nStart Pipelines with input: {input_str1} and {input_str2}")
    run_and_compare_pipelines(
        pipeline1,
        pipeline2,
        input_str1,
        input_str2,
        comparer=make_compare_pipeline_results_estimate_runs_from_fraction('_')
    )

def check_decay_pipeline_step():
    steps = [DecayPipelineStep(decay_char='_', decay_rate=0.1)]
    pipeline1 = SeveralRunsPipeline(steps, runs=7)
    pipeline2 = SeveralRunsPipeline(steps, runs=3)
    input_str = "This is an example sentence to test the DecayPipelineStep."
    print(f"Testing decay\nStart Pipelines with input: {input_str}")
    run_and_compare_pipelines(
        pipeline1,
        pipeline2,
        input_str,
        input_str,
        comparer=make_compare_pipeline_results_percentage_of_letter('_')
    )

if __name__ == "__main__":
    check_decay_pipeline_step()
