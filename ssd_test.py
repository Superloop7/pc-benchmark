import time, os


def disk_write_method(filepath, write_size):
    # create one block and keep write to test file
    block_size = 1048576
    one_block = "0" * block_size
    write_loops = int(write_size // block_size)
    with open(filepath, "w") as f:
        for _ in range(0, write_loops):
            f.write(one_block)


def disk_read_method(filepath):
    with open(filepath, "r") as f:
        f.read()


def ssd_test(total_size=1073741824 * 16):
    # create all parameter
    file_path = "testfile.txt"
    max_time = 0.5

    # start calculate time
    start = time.time()
    round_counter = 0
    # keep write block until up to input size
    while True:
        disk_write_method(file_path, total_size)
        round_counter += 1
        test_time = time.time() - start
        # stop the loop
        if test_time > max_time:
            break
    # 1Mb mult round_counter can calculate the written size
    size = round_counter * 1024

    r_start = time.time()
    disk_read_method(file_path)
    r_end = time.time()
    read_time = r_end - r_start
    read_speed = 1024 / read_time

    return f"Your Hard Disk write speed is : {size / test_time:.2f} Mbytes per second\nYour Hard Disk read speed is :{read_speed:.2f} Mbytes per seconds"


if __name__ == "__main__":
    print(ssd_test())
