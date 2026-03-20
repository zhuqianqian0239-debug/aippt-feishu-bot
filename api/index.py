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
