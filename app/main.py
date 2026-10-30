
from fastapi import FastAPI, responses
from pydantic import BaseModel
from app.spark_responder import SparkResponder
from app.wonder_memory import WonderMemory

app = FastAPI()
resp = SparkResponder()
mem = WonderMemory()

class Req(BaseModel):
    message: str

@app.get("/")
async def root():
    return await resp.test_models()

@app.get("/test-muse")
async def test():
    return await resp.test_models()

@app.post("/api/chat/demo")
async def chat(req: Req):
    facts = mem.remember(req.message)
    ctx = mem.get()
    result = await resp.chat(ctx["facts"], req.message)
    if result.get("ok"):
        return {"text": result["text"], "model": result["model"], "facts": ctx["facts"], "facts_count": len(ctx["facts"])}
    else:
        return {"text": f"⚠️ {result['error']}\n\nPara usar tus $149.80 free credits:\n1. Ve a https://dev.meta.ai → API keys → Create key → Type Muse\n2. Copia la muse_... key\n3. En Render pon MODEL_API_KEY=muse_...\n4. Deploy", "model": "fallback - check error", "facts": ctx["facts"]}

@app.get("/mind.html", response_class=responses.HTMLResponse)
async def mind():
    return """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MIND by Cognitiva - Built with Meta AI - Muse Spark 1.3</title>
<style>:root{--b:#0064E0;--p:#7C3AED;--c:#00D1FF;--bg:#F8FAFF}*{box-sizing:border-box;margin:0;padding:0}body{font-family:Inter,system-ui;background:var(--bg);min-height:100vh}.bg{position:fixed;inset:0;background:radial-gradient(1200px 600px at 10% -10%, rgba(0,100,224,.12), transparent), radial-gradient(1000px 500px at 90% 10%, rgba(124,58,237,.12), transparent)}.header{position:sticky;top:0;z-index:10;backdrop-filter:blur(24px);background:rgba(255,255,255,.8);border-bottom:1px solid rgba(0,0,0,.06);padding:14px 20px;display:flex;gap:12px;align-items:center}.logo{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,var(--b),var(--p),var(--c))}.header h1{font-size:18px;font-weight:700}.header span{font-size:12px;color:#6B7280}.fluor{height:3px;background:linear-gradient(90deg,var(--b),var(--p),var(--c),var(--b));background-size:200% 100%;animation:s 6s linear infinite}@keyframes s{0%{background-position:0%}100%{background-position:200%}}.container{position:relative;max-width:1100px;margin:0 auto;padding:20px;display:grid;grid-template-columns:320px 1fr;gap:20px}@media(max-width:900px){.container{grid-template-columns:1fr}}.card{background:rgba(255,255,255,.9);backdrop-filter:blur(12px);border:1px solid rgba(0,0,0,.06);border-radius:20px;padding:20px;box-shadow:0 8px 32px rgba(0,0,0,.04)}.card h3{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:12px}.facts{font-size:13px;line-height:1.6}.chat{height:72vh;display:flex;flex-direction:column}.messages{flex:1;overflow:auto;display:flex;flex-direction:column;gap:12px;padding:10px 0}.msg{max-width:82%;padding:12px 16px;border-radius:18px;font-size:14px;line-height:1.5}.msg.user{align-self:flex-end;background:linear-gradient(135deg,var(--b),var(--p));color:white;border-bottom-right-radius:6px}.msg.assistant{align-self:flex-start;background:white;border:1px solid rgba(0,0,0,.06);border-bottom-left-radius:6px}.input-row{display:flex;gap:10px;margin-top:12px}.input-row input{flex:1;padding:14px 18px;border-radius:14px;border:1px solid rgba(0,0,0,.08);font-size:14px;outline:none}.input-row button{padding:14px 20px;border-radius:14px;border:0;background:linear-gradient(135deg,var(--b),var(--p));color:white;font-weight:600;cursor:pointer}.status{font-size:11px;color:#6B7280;margin-top:8px}pre{font-size:11px;background:#0F172A;color:#E2E8F0;padding:10px;border-radius:10px;white-space:pre-wrap;word-break:break-all}</style></head>
<body><div class="bg"></div><div class="header"><div class="logo"></div><div><h1>MIND by Cognitiva</h1><span>Built with Meta AI • Muse Spark 1.3 • 1M context • Quickstart Official</span></div></div><div class="fluor"></div>
<div class="container"><div class="card"><h3>FACTS REMEMBERED (FROM AI)</h3><div id="facts" class="facts"><span style="color:#9CA3AF">No facts yet - AI will remember</span></div><div style="margin-top:20px"><h3>TEST MUSE CONNECTION</h3><button onclick="testMuse()" style="width:100%;padding:10px;border-radius:10px;border:1px solid #E5E7EB;background:white;cursor:pointer">Test GET /models - Quickstart</button><pre id="testOut" style="margin-top:10px"></pre></div><div style="margin-top:20px;font-size:11px;color:#6B7280">Quickstart: base https://api.meta.ai/v1 model muse-spark-1.3 • Free credits $149.80</div></div>
<div class="card chat"><div id="msgs" class="messages"><div class="msg assistant">Hola! Soy MIND con Muse Spark 1.3 (Quickstart oficial). Dime: "Me llamo Remis, vivo en Labranza, mi perro es Luna" y lo recordaré.</div></div><div class="input-row"><input id="inp" placeholder="Escribe..." onkeydown="if(event.key==='Enter')send()"><button type="button" onclick="send()">Enviar</button></div><div id="status" class="status">Muse Spark 1.3 • https://api.meta.ai/v1 • Esperando MODEL_API_KEY...</div></div></div>
<script>
async function testMuse(){document.getElementById('testOut').textContent='Cargando...';const r=await fetch('/test-muse');const j=await r.json();document.getElementById('testOut').textContent=JSON.stringify(j,null,2);}
async function send(){const inp=document.getElementById('inp');const txt=inp.value.trim();if(!txt)return;const msgs=document.getElementById('msgs');msgs.innerHTML+=`<div class="msg user">${txt}</div>`;inp.value='';msgs.scrollTop=msgs.scrollHeight;document.getElementById('status').textContent='Pensando con muse-spark-1.3...';try{const r=await fetch('/api/chat/demo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});const j=await r.json();msgs.innerHTML+=`<div class="msg assistant">${j.text}<br><small style="color:#9CA3AF">${j.model||''}</small></div>`;if(j.facts&&Object.keys(j.facts).length){document.getElementById('facts').innerHTML=Object.entries(j.facts).map(([k,v])=>`<div><b>${k}</b>=${v}</div>`).join('');}document.getElementById('status').textContent=j.model||'OK';}catch(e){document.getElementById('status').textContent='Error: '+e.message}msgs.scrollTop=msgs.scrollHeight;}
</script></body></html>
"""
