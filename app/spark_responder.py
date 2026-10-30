
import os
from openai import OpenAI

class SparkResponder:
    def __init__(self):
        self.key = (os.getenv("META_API_KEY") or os.getenv("MODEL_API_KEY") or "").strip()
        self.base = "https://api.meta.ai/v1"
        print(f"[MUSE SPARK] key={self.key[:12]} base={self.base}")

    async def test_models(self):
        # Test per Quickstart: list models
        try:
            client = OpenAI(base_url=self.base, api_key=self.key)
            models = client.models.list()
            data = [m.id for m in models.data]
            print(f"[MODELS] {data}")
            return {"status": 200, "models": data, "base": self.base, "key_prefix": self.key[:12]}
        except Exception as e:
            return {"status": 401, "error": str(e), "base": self.base, "key_prefix": self.key[:12]}

    async def chat(self, facts, user_msg):
        client = OpenAI(base_url=self.base, api_key=self.key)
        # Quickstart says use Responses API, but Chat Completions also works. Use responses per doc.
        try:
            # Try Responses API first (per Quickstart)
            resp = client.responses.create(
                model="muse-spark-1.3",
                input=f"Facts: {facts}\nUser: {user_msg}\nRespond short, mention facts remembered."
            )
            text = resp.output_text if hasattr(resp, 'output_text') else str(resp)
            print(f"[SPARK REAL OK] muse-spark-1.3 {len(text)} chars")
            return {"ok": True, "model": "muse-spark-1.3 REAL via Responses API", "text": text}
        except Exception as e1:
            print(f"[RESPONSES FAIL] {e1}, trying chat completions")
            try:
                # Fallback Chat Completions
                cc = client.chat.completions.create(
                    model="muse-spark-1.3",
                    messages=[{"role": "system", "content": f"You are MIND, Built with Meta AI. Facts: {facts}"}, {"role": "user", "content": user_msg}],
                    max_tokens=800
                )
                text = cc.choices[0].message.content
                return {"ok": True, "model": "muse-spark-1.3 REAL via Chat", "text": text}
            except Exception as e2:
                return {"ok": False, "error": f"Responses: {e1} | Chat: {e2}"}
