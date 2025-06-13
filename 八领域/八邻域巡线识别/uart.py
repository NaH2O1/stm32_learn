from maix import app, uart, pinmap, time
from struct import pack, unpack

def print_hex(data: bytes):
    for i in data:
        print(f"0x{i:02X}", end=" ")
    print("")

# 配置串口参数
device = "/dev/ttyS0"
serial0 = uart.UART(device, 115200)  # 明确指定引脚

# 构造发送数据
arg = 10
cent = 1000
data_body = pack("<HH", arg, cent)  # 小端打包两个uint16
header = b"\xAA"                    # 帧头
checksum = sum(header + data_body) % 256  # 校验和计算（假设协议包含帧头）
data = header + data_body + pack("B", checksum)

# 发送数据并打印
serial0.write(data)
print("Sent:")
print_hex(data)

# 接收处理逻辑
print("Waiting for response...")
recv_buffer = b''  # 缓冲区用于存储接收到的数据

# 定义特殊字节序列
special_sequence = b'\x34\x32\x0D\x0A'

while not app.need_exit():
    # 尝试读取数据（非阻塞）
    chunk = serial0.read(64)  # 一次最多读取64字节
    if chunk:
        recv_buffer += chunk
        print("Received chunk:", end=' ')
        print_hex(chunk)
    
    # 尝试检查特殊字节序列
    if len(recv_buffer) >= len(special_sequence):
        # 检查是否收到特殊字节序列
        if recv_buffer.startswith(special_sequence):
            print("Special sequence received! Triggering special operation...")
            # 在这里填写你想要执行的特定操作
            # 例如：打开某个设备、发送特定指令等
            
            # 回显处理
            serial0.write(special_sequence)
            # 清除缓冲区中的已处理字节序列
            recv_buffer = recv_buffer[len(special_sequence):]
        else:
            # 跳过非特殊序列的数据
            recv_buffer = recv_buffer[1:]
    
    time.sleep_ms(1)