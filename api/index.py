from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request
import ssl
import hmac
import hashlib
import base64
import time

APP_KEY = "658415eecba7a"
SECRET_KEY = "9rSv6RYyt1rD8BPhaN2DVIGiGCdzReaw"
API_BASE = "https://co.aippt.cn"
CHANNEL = "feishu_bot"

def generate_signature(method, uri, timestamp):
    if not uri.startswith("/"):
        uri = "/" + uri
    if not uri.endswith("/"):
        uri = uri + "/"
    string_to_sign = method + "@" + uri + "@" + timestamp
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1
    ).digest()
    return base64.b64encode(signature).decode("utf-8")

def get_auth_code(uid):
    try:
        uri = "/api/grant/code"
        timestamp = str(int(time.time()))
        signature = generate_signature("GET", uri, timestamp)
        url = API_BASE + uri + "?uid=" + uid + "&channel=" + CHANNEL
        headers = {
            "x-api-key": APP_KEY,
            "x-timestamp": timestamp,
            "x-signature": signature
        }
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("code") == 0:
                return result.get("data", {}).get("code")
    except Exception as e:
        print("Error:", e)
    return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        uid = query.get("uid", ["anonymous"])[0]
        code = get_auth_code(uid)
        
        if not code:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Error")
            return
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>AiPPT</title>
<script src="https://api-static.aippt.cn/aippt-iframe-sdk.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;height:100vh;display:flex;flex-direction:column;background:#f5f5f5}}
.header{{background:transparent;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;position:absolute;top:0;left:0;right:0;z-index:10}}
.header h1{{font-size:15px;font-weight:500;color:#542FEB}}
.header span{{font-size:13px;color:#542FEB}}
#container{{flex:1;width:100%;position:relative;background:#fff}}
.loading{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}}
.spinner{{width:40px;height:40px;border:3px solid #f0f0f0;border-top:3px solid #542FEB;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 15px}}
@keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
.loading p{{color:#999;font-size:14px}}
</style></head><body>
<div class="header"><h1>💔电子PPT码字仔</h1><span>很不高兴为您服务</span></div>
<div id="container"><div class="loading" id="loading"><div class="spinner"></div><p>正在加载 AiPPT...</p></div></div>
<script>(async()=>{{try{{await AipptIframe.show({{appkey:'{APP_KEY}',channel:'{CHANNEL}',code:'{code}',container:document.getElementById("container"),editorModel:true}});document.getElementById("loading").style.display="none"}}catch(e){{console.error(e)}}}})()</script>
</body></html>'''
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
