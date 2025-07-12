import cpu_test.cpu_test as cpu_test
import hard_disk_test.harddisk_test as harddisk_test
import webbrowser

if __name__ == "__main__":
    cpu_tester = cpu_test.CpuTest(calculate_time=20)
    single_core_result =cpu_tester.run_single()
    multi_cores_result =cpu_tester.run_multi()
    single_core_result = str(single_core_result).split(" ")[1:]
    multi_cores_result = str(multi_cores_result).split(" ")[1:]
    cpu_result = f"{single_core_result}\n {multi_cores_result}"

    harddisk_tester = harddisk_test.HardDiskTest()
    write_result = harddisk_tester.harddisk_write_test()
    read_result = harddisk_tester.harddisk_read_test()
    write_result = str(write_result).split(" ")[1:]
    read_result = str(read_result).split(" ")[1:]
    harddisk_result = f"{write_result}\n {read_result}"

    with open("myfile.html", "r", encoding="utf-8") as f:
        html = f.read()

    result_script = f"<p>{cpu_result}</p>\n<p>{harddisk_result}</p>\n"

    final_report = html.replace("<result>", result_script)

    with open("result.html", "w", encoding="utf-8") as f:
        f.write(final_report)

    webbrowser.open("result.html")
