import os, time
from dataclasses import dataclass

# @dataclass can replace __init__
class HardDiskResult:
    # the speed unit is MB/s
    write_speed: float
    read_speed: float
    # size_unit is MB
    size_tested: int
    wirte_time_used: float
    read_time: float

    # it will more easy to see all data
    def __repr__(self):
        return (
            f"SsdTestResult("
            f"write_speed={self.write_speed:.2f}, "
            f"read_speed={self.read_speed:.2f}, "
            f"size_tested={self.size_tested}, "
            f"write_time={self.write_time:.2f}, "
            f"read_time={self.read_time:.2f})"
        )

    def __str__(self):
        return (
            f"[HARDDISK RESULT] Write Speed : {self.write_speed:.2f} MB/s\n"
            f"[HARDDISK RESULT] Read  Speed : {self.read_speed:.2f} MB/s\n"
        )
    
class HardDiskTest:
    def __init__(self, file_path="harddisk_test_temp.bin", duration=1, block_size=256 * 1024):
        self.file_path = file_path
        self.duration = duration
        self.block_size = block_size
        # one binary 0 is 1 byte each round 256KB
        self.data_block = b"0" * block_size

    def harddisk_test(self) -> HardDiskResult:
        # write test
        total_written_size = 0
        write_start = time.perf_counter()

        # write the binary file
        with open(self.file_path, "wb") as f:
            while True:
                f.write(self.data_block)
                total_written_size += 1
                # write data to memory
                f.flush()
                # synchronize to harddisk
                os.fsync(f.fileno())
                # protect my disk
                total_used_time = time.perf_counter()
                if total_used_time - write_start >= self.duration:
                    break