import cpu_test
import ssd_test
import webbrowser


cpu_result = cpu_test.cpu_test()
ssd_result = ssd_test.ssd_test()

with open("myfile.html", "r", encoding="utf-8") as f:
    html = f.read()

result_script = f"<p>{cpu_result}</p>\n<p>{ssd_result}</p>\n"

final_report = html.replace("<result>", result_script)

with open("result.html", "w", encoding="utf-8") as f:
    f.write(final_report)

webbrowser.open("result.html")
