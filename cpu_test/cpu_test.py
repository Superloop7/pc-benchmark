import time
import os
import concurrent.futures
from dataclasses import dataclass


@dataclass
class TestResult:
    mode: str         # 'single' or 'multi'
    # rounds: int
    scores: float
    cpu_count: int = 1

    def __str__(self):
        if self.mode == 'single':
            return f"The single core test is finished your single thred score is {self.scores:.4f})"
        else:
            return f"The multiple cores test is finished: your multiple thread score is ({self.scores:.4f})"


class CpuTest:
    def __init__(self, calculate_time=20):
        self.calculate_time = calculate_time
    def single_core_work(self, seconds):
        start = time.time()
        factor = 1
        pi = 0
        round_count = 0

        while time.time() - start < seconds:
            if round_count % 2 == 0:
                pi += 4 / factor
            else:
                pi -= 4 / factor
            factor += 2
            round_count += 1
        return round_count

    def run_single(self) -> TestResult:
        print("The single core test is start, and will run about 20 seconds ...")
        total_rounds = self.single_core_work(self.calculate_time)
        single_scores = total_rounds / 1e5
        print("The single core test is finished")
        return TestResult(mode="single", scores = single_scores)

    def run_multi(self) -> TestResult:
        cpu_count = os.cpu_count()
        if cpu_count is None:
            cpu_count = 1
            print("Detected failed the default cpu will be seted as 1")
        elif cpu_count == 1:
            print(f"Your pc have {cpu_count} core")
        else:
            print(f"Your pc has {cpu_count} cores")
        print("The multiple cores test is start, and will run about 20 seconds ...")
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
            single_run = [executor.submit(self.single_core_work, self.calculate_time) for _ in range(cpu_count)]
            round_list = [f.result() for f in concurrent.futures.as_completed(single_run)]

        total_rounds = sum(round_list)
        multi_scores = total_rounds / 1e5
        print("The multiple cores test is finished")
        return TestResult(mode="multi", scores = multi_scores)

    def run_all(self):
        single = self.run_single()
        multi = self.run_multi()
        print(single)
        print(multi)


if __name__ == "__main__":
    tester = CpuTest(calculate_time=20)
    tester.run_all()