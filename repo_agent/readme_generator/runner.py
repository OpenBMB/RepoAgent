import subprocess

# 定义要运行的两个 Python 文件的文件名
file1 = "summary.py"
file2 = "readmegen.py"

# 运行第一个 Python 文件
result1 = subprocess.run(["python", file1], capture_output=True, text=True, check=True)

# 打印第一个文件的输出
print("Output of summary.py:")
print(result1.stdout)

# 运行第二个 Python 文件
result2 = subprocess.run(["python", file2], capture_output=True, text=True, check=True)

# 打印第二个文件的输出
print("\nOutput of readmegen.py:")
print(result2.stdout)
