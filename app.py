from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess, os, uuid, time, json

app = FastAPI(title="AI Offline API")

# تكامل بسيط مع خدمات محلية (افتراضية)
# - LLM: نفترض وجود واجهة محلية على شكل أمر عبر llama.cpp أو text-generation-webui
# - Image: نفترض وجود SD WebUI REST أو نستخدم diffusers مباشرًا

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 512

class ImageRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024
    steps: int = 28

@app.post("/chat")
def chat(req: ChatRequest):
    # مثال استدعاء بسيط لـ llama.cpp مترجم إلى واجهة سطر أوامر (تحتاج ضبط المسارات)
    model_path = "models/llm/ggml-model-q4_0.bin"  # مثال
    cmd = [
        "./llama.cpp/osscript/run_llama.sh",  # افتراض سكربت تشغيل محلي
        "--model", model_path,
        "--prompt", req.prompt,
        "--tokens", str(req.max_tokens)
    ]
    try:
        # هنا نستخدم subprocess كمثال؛ الأفضل التواصل مع خدمة محلية عبر HTTP
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=60)
        text = output.decode(errors="ignore")
        return {"answer": text}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e.output.decode()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_image")
def generate_image(req: ImageRequest):
    # مثال استدعاء REST إلى SD WebUI المحلي إن كان يعمل على 127.0.0.1:7860/api
    import requests
    sd_api = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": req.prompt,
        "width": req.width,
        "height": req.height,
        "steps": req.steps
    }
    try:
        r = requests.post(sd_api, json=payload, timeout=300)
        r.raise_for_status()
        data = r.json()
        # sd-webui عادةً يرجع صور base64 داخل response; هنا نحفّظ صورة كملف
        images = data.get("images", [])
        if not images:
            raise HTTPException(status_code=500, detail="No images returned")
        img_b64 = images[0]
        import base64
        img_data = base64.b64decode(img_b64.split(",",1)[-1]) if img_b64.startswith("data:") else base64.b64decode(img_b64)
        out_name = f"output/{int(time.time())}_{uuid.uuid4().hex[:6]}.png"
        os.makedirs("output", exist_ok=True)
        with open(out_name, "wb") as f:
            f.write(img_data)
        return {"path": out_name}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"SD API error: {str(e)}")