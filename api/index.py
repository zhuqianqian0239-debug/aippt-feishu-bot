# Vercel Serverless Function for AiPPT SDK Embed + Webhook
# File: api/index.py

import json
import urllib.request
import ssl
import hmac
import hashlib
import base64
import time
import re

# AiPPT 配置
APP_KEY = "658415eecba7a"
SECRET_KEY = "9rSv6RYyt1rD8BPhaN2DVIGiGCdzReaw"
API_BASE = "https://co.aippt.cn"
CHANNEL = "feishu_bot"

# 牛马助手2号 Webhook 配置
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/bcdf02ae-32fd-49fd-9e71-62b2678315b5"

# 关键词配置
PPT_KEYWORDS = [r'ppt', r'p\.p\.t', r'powerpoint', r'幻灯片', r'演示文稿']

def generate_signature(method, uri, timestamp):
    if not uri.startswith("/"):
        uri = "/" + uri
    if not uri.endswith("/"):
        uri = uri + "/"
    
    string_to_sign = f"{method}@{uri}@{timestamp}"
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha1
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def get_auth_code(uid):
    uri = "/api/grant/code"
    timestamp = str(int(time.time()))
    signature = generate_signature("GET", uri, timestamp)
    
    url = f"{API_BASE}{uri}?uid={uid}&channel={CHANNEL}"
    headers = {
        "x-api-key": APP_KEY,
        "x-timestamp": timestamp,
        "x-signature": signature
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get("code") == 0:
                return result.get("data", {}).get("code")
    except Exception as e:
        print(f"Error: {e}")
    return None

def should_trigger_aippt(message_text):
    """检测消息是否包含PPT相关关键词"""
    if not message_text:
        return False
    text_lower = message_text.lower()
    for pattern in PPT_KEYWORDS:
        if re.search(pattern, text_lower):
            return True
    return False

def send_webhook_card(uid):
    """通过 Webhook 发送 AiPPT 卡片"""
    embed_url = f"https://aippt-feishu-bot.vercel.app?uid={uid}"
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "purple",
            "title": {"tag": "plain_text", "content": "💔 电子牛马"}
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": "电子牛马很不高兴为您服务❤️\n\n需要智能PPT工具帮助吗？\n我为您准备了便捷好用的AI工具，点击按钮即可体验⬇️"}
            },
            {
                "tag": "action",
                "actions": [{
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "🚀 打开 AiPPT 工具"},
                    "type": "primary",
                    "url": embed_url
                }]
            }
        ]
    }
    
    message = {
        "msg_type": "interactive",
        "card": card
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    data = json.dumps(message, ensure_ascii=False).encode('utf-8')
    
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('code') == 0
    except Exception as e:
        print(f"Webhook Error: {e}")
        return False

def handle_webhook(event_data):
    """处理飞书 webhook 事件"""
    try:
        # 提取事件类型
        event_type = event_data.get('header', {}).get('event_type', '')
        
        if event_type != 'im.message.receive_v1':
            return {'status': 'ignored', 'reason': 'not_message_event'}
        
        # 提取消息内容from http.server import BaseHTTPRequestHandler
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
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;height:100vh}}
#container{{width:100%;height:100%;position:relative}}
.loading{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}}
.spinner{{width:40px;height:40px;border:3px solid #f0f0f0;border-top:3px solid #542FEB;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 15px}}
@keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
.loading p{{color:#999;font-size:14px}}
</style></head><body>
<div id="container"><div class="loading" id="loading"><div class="spinner"></div><p>正在加载 AiPPT...</p></div></div>
<script>(async()=>{{try{{await AipptIframe.show({{appkey:'{APP_KEY}',channel:'{CHANNEL}',code:'{code}',container:document.getElementById("container"),editorModel:true}});document.getElementById("loading").style.display="none"}}catch(e){{console.error(e)}}}})()</script>
</body></html>'''
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
