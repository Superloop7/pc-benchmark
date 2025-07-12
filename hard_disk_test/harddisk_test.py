import os, time
from dataclasses import dataclass


# @dataclass can replace __init__
@dataclass
class HardDiskResult:
    mode: str
    # the speed unit is MB/s
    write_speed: float
    read_speed: float
    # size_unit is MB
    size_tested: int
    write_time_used: float
    read_time_used: float

    # it will more easy to see all data
    def __repr__(self):
        if self.mode == "write_test":
            return (
                f"SsdTestResult("
                f"write_speed={self.write_speed:.2f}, "
                f"size_tested={self.size_tested}, "
                f"write_time={self.write_time_used:.2f}"
            )
        elif self.mode == "read_test":
            return (
                f"SsdTestResult("
                f"read_speed={self.read_speed:.2f}, "
                f"size_tested={self.size_tested}, "
                f"read_time={self.read_time_used:.2f})"
            )

    def __str__(self):
        if self.mode == "write_test":
            return f"[HARDDISK RESULT] Write Speed : {self.write_speed:.2f} MB/s"
        elif self.mode == "read_test":
            return f"[HARDDISK RESULT] Read  Speed : {self.read_speed:.2f} MB/s"


class HardDiskTest:
    def __init__(self, file_path="write_test.bin", duration=1, block_size=256 * 1024):
        self.file_path = file_path
        self.duration = duration
        self.block_size = block_size
        # one binary 0 is 1 byte each round 256KB
        self.data_block = b"0" * block_size

    def harddisk_write_test(self) -> HardDiskResult:
        # write test
        total_written_round = 0
        write_start = time.perf_counter()

        print(f"[INFO] Starting HardDisk Write test ...")
        # write the binary file
        with open(self.file_path, "wb") as file:
            while True:
                file.write(self.data_block)
                total_written_round += 1
                # protect my disk
                if time.perf_counter() - write_start >= self.duration:
                    break

        write_end = time.perf_counter()
        write_time = write_end - write_start
        # one block is 256 kb
        self.written_size = (self.block_size * total_written_round) / (1024 * 1024)
        write_speed = self.written_size / write_time
        print(f"[INFO] Write Test finished")
        return HardDiskResult(
            write_speed=write_speed,
            write_time_used=write_time,
            size_tested=self.written_size,
            mode="write_test",
            read_speed=0,
            read_time_used=0,
        )

    def harddisk_read_test(self) -> HardDiskResult:
        # Read test
        print(f"[INFO] Starting HardDisk Read test ...")

        read_start = time.perf_counter()
        with open(self.file_path, "rb") as file:
            # Read the file in blocks to minimize memory usage
            while file.read(self.block_size):
                pass
        read_end = time.perf_counter()
        read_time = read_end - read_start
        read_speed = self.written_size / read_time

        # clean the binary file
        try:
            os.remove(self.file_path)
        except Exception as e:
            print(f"[WARN] Failed to remove the temp file: {e}")

        print(f"[INFO] Read Test finished")
        return HardDiskResult(
            read_speed=read_speed,
            read_time_used=read_time,
            size_tested=self.written_size,
            mode="read_test",
            write_speed=0,
            write_time_used=0,
        )


if __name__ == "__main__":
    tester = HardDiskTest()
    write_result = tester.harddisk_write_test()
    print(write_result)
    read_result = tester.harddisk_read_test()
    print(read_result)
