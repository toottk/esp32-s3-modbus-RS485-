<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">


</head>
<body>
    <div class="container">
        <h1>Modbus AP模式 Web控制八路继电器</h1>
        <div class="instructions">
            <strong>使用说明：</strong>
            <ol>
                <li>手机连接WiFi热点<br>
                    名称：<code>ESP32S3_Relay</code><br>
                    密码：<code>12345678</code>
                </li>
                <li>浏览器访问：<code>http://192.168.4.1</code></li>
            </ol>
        </div>
        <div>
            <strong>ModbusRTU配置：</strong>
            <ul>
                <li>波特率：<code>9600</code></li>
                <li>通信接口：<code>tx=43</code>，<code>rx=44</code></li>
                <li>继电器地址：<code>0x0000</code> ~ <code>0x0007</code></li>
                <li>支持开（on）与关（off）操作</li>
                <li>Web服务器监听：<code>0.0.0.0:80</code></li>
                <li>已配置UTF-8编码</li>
            </ul>
        </div>
        <div class="relay-group">
            <!-- 8个继电器控制按钮 -->
            <div class="relay">
                继电器0<br>
                <button class="on" onclick="controlRelay(0, 'on')">开</button>
                <button class="off" onclick="controlRelay(0, 'off')">关</button>
            </div>
            <div class="relay">
                继电器1<br>
                <button class="on" onclick="controlRelay(1, 'on')">开</button>
                <button class="off" onclick="controlRelay(1, 'off')">关</button>
            </div>
            <div class="relay">
                继电器2<br>
                <button class="on" onclick="controlRelay(2, 'on')">开</button>
                <button class="off" onclick="controlRelay(2, 'off')">关</button>
            </div>
            <div class="relay">
                继电器3<br>
                <button class="on" onclick="controlRelay(3, 'on')">开</button>
                <button class="off" onclick="controlRelay(3, 'off')">关</button>
            </div>
            <div class="relay">
                继电器4<br>
                <button class="on" onclick="controlRelay(4, 'on')">开</button>
                <button class="off" onclick="controlRelay(4, 'off')">关</button>
            </div>
            <div class="relay">
                继电器5<br>
                <button class="on" onclick="controlRelay(5, 'on')">开</button>
                <button class="off" onclick="controlRelay(5, 'off')">关</button>
            </div>
            <div class="relay">
                继电器6<br>
                <button class="on" onclick="controlRelay(6, 'on')">开</button>
                <button class="off" onclick="controlRelay(6, 'off')">关</button>
            </div>
            <div class="relay">
                继电器7<br>
                <button class="on" onclick="controlRelay(7, 'on')">开</button>
                <button class="off" onclick="controlRelay(7, 'off')">关</button>
            </div>
        </div>
    </div>
</body>
</html>
