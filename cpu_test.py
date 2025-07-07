import time


def cpu_test(calculate_time=20):
    start = time.time()
    # pi calculate
    factor = 1
    pi = 0
    round = 0
    # for loop to calculate the pi
    while time.time() - start < calculate_time:

        if round % 2 == 0:
            pi += 4 / factor

        else:
            pi -= 4 / factor

        factor += 2
        round += 1

    return f"Your cpu scores is : {round / 1e7:.4f}"


if __name__ == "__main__":
    print(cpu_test())
