import network
import machine
import socket
import time
import ure

# --------- AP模式配置 ---------
AP_SSID = 'ESP32S3_Relay'
AP_PASSWORD = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)
print('AP模式已启动，SSID:', AP_SSID)
print('AP模式网络配置:', ap.ifconfig())

# --------- Modbus RTU 驱动 ---------
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
        self.uart.write(req)

# --------- 继电器配置 ---------
relay_addrs = [0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007]
relay_states = [0] * 8  # 记录每路状态，0=关，1=开
modbus = ModbusRTU(uart_id=1, baudrate=9600, tx=43, rx=44)
slave_addr = 0xFF  # 按实际模块地址设置

# --------- Web服务器 ---------
def html_page(states):
    btns = ""
    for i in range(8):
        btns += (
            f"<tr><td>继电器{i+1}</td>"
            f"<td>{'开' if states[i] else '关'}</td>"
            f"<td>"
            f"<form style='display:inline;' method='get'>"
            f"<button name='relay' value='{i}' type='submit'>打开</button>"
            f"<input type='hidden' name='action' value='on'>"
            f"</form>"
            f"<form style='display:inline;' method='get'>"
            f"<button name='relay' value='{i}' type='submit'>关闭</button>"
            f"<input type='hidden' name='action' value='off'>"
            f"</form>"
            f"</td></tr>"
        )
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ESP32S3 继电器控制</title>
</head>
<body>
<h2>ESP32S3 八路继电器控制</h2>
<table border="1" cellpadding="8">
<tr><th>通道</th><th>状态</th><th>操作</th></tr>
{btns}
</table>
<p>请连接WiFi热点 <b>{AP_SSID}</b>，然后访问 <b>{ap.ifconfig()[0]}</b></p>
</body>
</html>
"""
    return html

def parse_query(query):
    params = {}
    for pair in query.split('&'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            params[k] = v
    return params

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print('Web服务器已启动，访问 http://%s/ 控制继电器' % ap.ifconfig()[0])

try:
    while True:
        cl, addr = s.accept()
        try:
            req = cl.recv(1024).decode()
            # 解析GET参数
            match = ure.search(r'GET /\??(.*?) ', req)
            if match:
                query = match.group(1)
                params = parse_query(query)
                if 'relay' in params and 'action' in params:
                    idx = int(params['relay'])
                    if 0 <= idx < 8:
                        if params['action'] == 'on':
                            modbus.write_single_coil(slave_addr, relay_addrs[idx], True)
                            relay_states[idx] = 1
                        elif params['action'] == 'off':
                            modbus.write_single_coil(slave_addr, relay_addrs[idx], False)
                            relay_states[idx] = 0
            html = html_page(relay_states)
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(html)
            cl.close()
        except Exception as e:
            print('处理请求时出错:', e)
            try:
                cl.close()
            except Exception:
                pass
finally:
    s.close()