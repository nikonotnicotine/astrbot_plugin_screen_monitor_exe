from flask import Flask, send_file
import mss
import io
import logging
from PIL import Image

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/screenshot', methods=['GET'])
def take_screenshot():
    try:
        # 换回大写的 mss.MSS()，彻底消除警告
        with mss.MSS() as sct:
            monitor = sct.monitors[1] 
            sct_img = sct.grab(monitor)
            
            # 压缩为 JPEG 格式，极速传输
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG', quality=60)
            img_io.seek(0)
            
            print("📸 成功截取屏幕并压缩为 JPEG，正在传输给大模型...")
            return send_file(img_io, mimetype='image/jpeg')
            
    except Exception as e:
        print(f"❌ 截图失败: {e}")
        return str(e), 500

if __name__ == '__main__':
    print("🚀 截图查岗服务已启动，监听 0.0.0.0:6878")
    app.run(host='0.0.0.0', port=6878, threaded=True)