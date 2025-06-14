import machine
import time

class ModbusRTU:
    def __init__(self, uart_id=1, baudrate=9600, tx=43, rx=44):
        self.uart = machine.UART(uart_id, baudrate=baudrate, tx=machine.Pin(tx), rx=machine.Pin(rx))

    def calc_crc(self, data):
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if (crc & 0x0001):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, 'little')

    def write_single_coil(self, slave_addr, coil_addr, on):
        value = 0xFF00 if on else 0x0000
        req = bytearray([
            slave_addr,
            0x05,
            (coil_addr >> 8) & 0xFF,
            coil_addr & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        req += self.calc_crc(req)
        print('发送:', ' '.join('{:02X}'.format(b) for b in req))
        self.uart.write(req)

    def read_response(self, length=8, timeout=1000):
        start = time.ticks_ms()
        while self.uart.any() < length:
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                print('响应超时')
                return None
            time.sleep(0.01)
        resp = self.uart.read(length)
        print('接收:', resp)
        return resp

modbus = ModbusRTU(uart_id=1, baudrate=9600, tx=43, rx=44)

# 八个继电器的线圈地址分别为0x0000~0x0007
relay_addrs = [0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007]

while True:
    # 依次打开8个继电器
    for addr in relay_addrs:
        modbus.write_single_coil(slave_addr=0xFF, coil_addr=addr, on=True)
        resp = modbus.read_response(length=8)
        print(f'打开继电器{hex(addr)}响应:', resp)
        time.sleep(0.5)

    time.sleep(2)

    # 依次关闭8个继电器
    for addr in relay_addrs:
        modbus.write_single_coil(slave_addr=0xFF, coil_addr=addr, on=False)
        resp = modbus.read_response(length=8)
        print(f'关闭继电器{hex(addr)}响应:', resp)
        time.sleep(0.5)

    time.sleep(2)