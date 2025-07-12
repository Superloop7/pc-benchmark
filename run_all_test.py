import cpu_test.cpu_test as cpu_test
import hard_disk_test.harddisk_test as harddisk_test
import webbrowser

if __name__ == "__main__":
    cpu_tester = cpu_test.CpuTest(calculate_time=20)
    single_core_result =cpu_tester.run_single()
    multi_cores_result =cpu_tester.run_multi()
    cpu_result = (
        f"Single-core score: {single_core_result.scores:.2f} Points<br>"
        f"Multi-core score ({multi_cores_result.cpu_count} cores): {multi_cores_result.scores:.2f} Points"
    )
    harddisk_tester = harddisk_test.HardDiskTest()
    write_result = harddisk_tester.harddisk_write_test()
    read_result = harddisk_tester.harddisk_read_test()
    harddisk_result = (
        f"Write Speed: {write_result.write_speed:.2f} MB/s<br>"
        f"Read Speed: {read_result.read_speed:.2f} MB/s"
    )
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    result_script = f"<p>{cpu_result}</p>\n<p>{harddisk_result}</p>\n"

    final_report = html.replace("<result>", result_script)

    with open("pc_bench_result.html", "w", encoding="utf-8") as f:
        f.write(final_report)

    webbrowser.open("pc_bench_result.html")
