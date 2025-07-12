import os, time
from dataclasses import dataclass

# @dataclass can replace __init__
class HardDiskResult:
    mode: str
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
        if self.mode == "write_test":
            return f"[HARDDISK RESULT] Write Speed : {self.write_speed:.2f} MB/s"
        elif self.mode == "read_test":
            return f"[HARDDISK RESULT] Read  Speed : {self.read_speed:.2f} MB/s"
    
class HardDiskTest:
    def __init__(self, file_path="harddisk_test_temp.bin", duration=1, block_size=256 * 1024):
        self.file_path = file_path
        self.duration = duration
        self.block_size = block_size
        # one binary 0 is 1 byte each round 256KB
        self.data_block = b"0" * block_size

    def harddisk_wirte_test(self) -> HardDiskResult:
        # write test
        total_written_size = 0
        write_start = time.perf_counter()

        print(f"[INFO] Starting HardDisk write test ...")
        # write the binary file
        with open(self.file_path, "wb") as file:
            while True:
                file.write(self.data_block)
                total_written_size += 1
                # write data to memory
                file.flush()
                # synchronize to harddisk
                os.fsync(file.fileno())
                # protect my disk
                if time.perf_counter() - write_start >= self.duration:
                    break

        write_end = time.perf_counter()
        write_time = write_end - write_start
        # one block is 256 kb
        self.written_size = 4 * total_written_size
        write_speed = self.written_size / write_time
        print(f"[INFO] Write Test finished")
        return HardDiskResult(
            write_speed=write_speed,
            size_tested= self.written_size,
            write_time=write_time,
            mode = "write_test"
        )
    
    def harddisk_read_test(self) -> HardDiskResult:
        # Read test
        print(f"[INFO] Starting HardDisk write test ...")
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
        return HardDiskTest(
            read_speed=read_speed,
            read_time=read_time,
            mode = "read_test"
        )
    
if __name__ == "__main__":
    tester = HardDiskTest()
    write_result = tester.harddisk_wirte_test()
    print(write_result)
    read_result = tester.harddisk_read_test()
    print(write_result)