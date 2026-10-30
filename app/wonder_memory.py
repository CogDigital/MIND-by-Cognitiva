
import json, re
from pathlib import Path
MEM_FILE = Path("/tmp/mind_memories.json")
class WonderMemory:
    def __init__(self):
        self.data = {"facts": {}, "history": []}
        if MEM_FILE.exists():
            try: self.data = json.loads(MEM_FILE.read_text())
            except: pass
    def remember(self, text: str):
        t=text.lower()
        m=re.search(r"(?:me llamo|my name is|soy)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", text, re.I)
        if m: self.data["facts"]["name"]=m.group(1).strip()
        m=re.search(r"(?:vivo en|live in|de)\s+([A-Za-z\s,]+)", text, re.I)
        if m and len(m.group(1))<40: self.data["facts"]["city"]=m.group(1).strip()
        m=re.search(r"(?:mi perro|my dog|perro)\s+(?:es\s+|se llama\s+)?([A-Z][a-z]+)", text, re.I)
        if m: self.data["facts"]["pet"]=m.group(1).strip()
        self.data["history"].append(text)
        self.data["history"]=self.data["history"][-20:]
        MEM_FILE.write_text(json.dumps(self.data, ensure_ascii=False))
        return self.data["facts"]
    def get(self): return self.data
