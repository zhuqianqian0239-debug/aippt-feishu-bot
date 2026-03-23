# Vercel Serverless Function for AiPPT Webhook
import json
import urllib.request
import ssl

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/bcdf02ae-32fd-49fd-9e71-62b2678315b5"

def send_webhook_card(uid):
    embed_url = f"https://aippt-feishu-bot.vercel.app?uid={uid}"
    
    message = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "purple",
                "title": {"tag": "plain_text", "content": "AiPPT"}
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"用户: {uid}"}},
                {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "打开AiPPT"}, "type": "primary", "url": embed_url}]}
            ]
        }
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    data = json.dumps(message, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"}, method='POST')
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('code') == 0
    except Exception as e:
        return False

def handler(request):
    path = request.get('url', '/')
    
    if '/webhook' in path:
        body = request.get('body', '{}')
        try:
            event_data = json.loads(body) if isinstance(body, str) else body
        except:
            event_data = {}
        
        event_type = event_data.get('header', {}).get('event_type', '')
        
        if event_type == 'im.message.receive_v1':
            event = event_data.get('event', {})
            message = event.get('message', {})
            content = message.get('content', '{}')
            
            try:
                content_obj = json.loads(content)
                text = content_obj.get('text', '').lower()
            except:
                text = content.lower() if isinstance(content, str) else ''
            
            sender = event.get('sender', {})
            sender_id = sender.get('sender_id', {}).get('open_id', 'anonymous')
            
            if 'ppt' in text:
                success = send_webhook_card(sender_id)
                return {"statusCode": 200, "body": json.dumps({"status": "sent" if success else "failed"})}
        
        return {"statusCode": 200, "body": json.dumps({"status": "ignored"})}
    
    # 默认返回 embed 页面
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": f"<html><body><h1>AiPPT</h1><p>UID: {request.get('query', {}).get('uid', ['anon'])[0]}</p></body></html>"
    }
