
from maix import app, uart, pinmap, time
import struct
from enum import Enum

def print_hex(data : bytes):
    for i in data:
        print(f"0x{i:02X}", end=" ")
    print("")

device = "/dev/ttyS0"
serial0 = uart.UART(device, 115200)


class DataType(Enum):
    DEBUG = 0x01  # 调试指令
    ANGLE = 0x02  # 角度数据

class DataFrame:
    """统一数据结构，支持调试指令和角度数据"""
    def __init__(self, data_type, value):
        """
        :param data_type: 数据类型 - "debug"或"angle"
        :param value: 数据值 - debug(0-3), angle(-90到90)
        """
        if data_type == "debug":
            if not (0 <= value <= 3):
                raise ValueError("Debug value must be 0-3")
            self.data_type = DataType.DEBUG
        elif data_type == "angle":
            if not (-90 <= value <= 90):
                raise ValueError("Angle value must be -90 to 90")
            self.data_type = DataType.ANGLE
        else:
            raise ValueError("Invalid data type")
            
        self.value = value

    def __str__(self):
        type_str = "Debug" if self.data_type == DataType.DEBUG else "Angle"
        return f"{type_str} Frame: Value={self.value}"

class UARTProtocol:
    HEADER = 0xAA
    FOOTER = 0x6B
    
    def pack(self, frame):
        """打包DataFrame为字节流"""
        # 构建帧内容 (header|type|length|data)
        frame_content = struct.pack('BBBB', 
            self.HEADER,
            frame.data_type.value,
            0x01,  # 固定长度1字节
            frame.value)
            
        # 计算校验和 (不包括footer)
        checksum = sum(frame_content) % 256
        
        # 添加校验和和footer
        return frame_content + struct.pack('BB', checksum, self.FOOTER)
        
    def unpack(self, raw_data):
        """从字节流解包为DataFrame"""
        if len(raw_data) != 6:
            raise ValueError("Invalid frame length")
            
        try:
            header, data_type, length, data, checksum, footer = \
                struct.unpack('BBBBBB', raw_data)
        except struct.error as e:
            raise ValueError("Failed to unpack data") from e
            
        # 验证帧结构
        if header != self.HEADER or footer != self.FOOTER or length != 0x01:
            raise ValueError("Invalid frame structure")
            
        # 验证校验和
        if checksum != sum(raw_data[:4]) % 256:
            raise ValueError("Checksum mismatch")
            
        # 创建DataFrame对象
        try:
            if data_type == DataType.DEBUG.value:
                return DataFrame("debug", data)
            elif data_type == DataType.ANGLE.value:
                return DataFrame("angle", data)
            else:
                raise ValueError("Unknown data type")
        except ValueError as e:
            raise ValueError(f"Invalid data value: {e}")

protocol = UARTProtocol()
buffer = bytearray()

while not app.need_exit():
    # Read available data
    data = serial0.read()
    if not data:
        time.sleep_ms(10)
        continue
        
    # Add to buffer
    buffer.extend(data)
    
    # Process complete frames
    while len(buffer) >= 6:
        # Find frame header
        try:
            header_pos = buffer.index(UARTProtocol.HEADER)
        except ValueError:
            buffer.clear()
            break
            
        # Check if we have a complete frame
        if len(buffer) - header_pos < 6:
            break
            
        frame_data = buffer[header_pos:header_pos+6]
        del buffer[:header_pos+6]  # Remove processed bytes
        
        try:
            # Unpack and process the frame
            frame = protocol.unpack(frame_data)
            print(f"Received: {frame}")
            
            # Handle different frame types
            if frame.data_type == DataType.DEBUG:
                print(f"Debug command: {frame.value}")
            elif frame.data_type == DataType.ANGLE:
                print(f"Angle value: {frame.value}°")
                
        except ValueError as e:
            print(f"Error processing frame: {e}")
            continue
