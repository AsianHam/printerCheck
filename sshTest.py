import paramiko
import time

COMP = '128.59.251.93'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(COMP, 22, username = 'sps', password = 'mjikirk7', allow_agent = False)

stdin = ssh.exec_command("")

conn = ssh.invoke_shell()
print("Interactive ssh session established")

"""
ftp = ssh.open_sftp()
ftp.put("yardPrinters.py", "/home/sps/yardPrinters.py")
ftp.close()

"""
output = conn.recv(1000)
conn.send("\n")
conn.send("python3 yardPrinters.py\n")

time.sleep(15)
rawData = conn.recv(1000000)
rawData = rawData.decode("ascii").strip("\n")

dataTemp = rawData.splitlines()
data = dataTemp[4:-1]

print(data)