import time
import os
import concurrent.futures
from dataclasses import dataclass


# @dataclass can replace __init__
@dataclass
class CPUTestResult:
    mode: str         # 'single' or 'multi'
    # rounds: int
    scores: float
    cpu_count: int = 1

    def __str__(self):
        if self.mode == 'single':
            return f"[RESULT] Single-core score is {self.scores:.4f}."
        else:
            return f"[RESULT] Multiple-cores score is ({self.cpu_count} cores: {self.scores:.4f})."


class CpuTest:
    def __init__(self, calculate_time=20):
        self.calculate_time = calculate_time
    def single_core_work(self, seconds):
        start = time.time()
        # print(f"single core test start")
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
        # print(f"the single core test is finished")
        return round_count

    def run_single(self) -> CPUTestResult:
        print("[INFO] Starting single-core test for 20 seconds...")
        total_rounds = self.single_core_work(self.calculate_time)
        single_scores = total_rounds / 1e5
        print("[INFO] Single-core test complete.")
        return CPUTestResult(mode="single",
                            scores = single_scores
                            )

    def run_multi(self, cpu_count=None) -> CPUTestResult:
        cpu_count = os.cpu_count()
        if cpu_count is None:
            cpu_count = 1
            print("[INFO] Detected failed, the cpu will be set as 1")
        elif cpu_count == 1:
            print(f"[INFO] Detected {cpu_count} logical CPU core")
        else:
            print(f"[INFO] Detected {cpu_count} logical CPU cores")
        print("[INFO] Starting multi-core test for 20 seconds...")
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
            single_run = [executor.submit(self.single_core_work, self.calculate_time) for _ in range(cpu_count)]
            round_list = [f.result() for f in concurrent.futures.as_completed(single_run)]

        total_rounds = sum(round_list)
        multi_scores = total_rounds / 1e5
        print("[INFO] Multi-core test complete.")
        return CPUTestResult(
            mode="multi",
            scores = multi_scores,
            cpu_count= cpu_count
            )

    def run_all(self):
        single = self.run_single()
        print(single)
        multi = self.run_multi()
        print(multi)
        return single, multi

if __name__ == "__main__":
    tester = CpuTest(calculate_time=20)
    tester.run_all()