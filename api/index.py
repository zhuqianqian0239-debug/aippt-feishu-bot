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
