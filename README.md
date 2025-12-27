# تطبيق AI محلي (Offline) — دليل بدء سريع

هذا المشروع مثال لبنية تطبيق يعمل محليًا (بدون إنترنت بعد تنزيل الأوزان) يوفّر:
- دردشة محلية (LLM) للرد على الأسئلة
- توليد صور (Stable Diffusion)
- خطّ أساسي لتوليد فيديو (إطار-بإطار مع أدوات تثبيت)

ملاحظة: يجب تنزيل أوزان النماذج (LLM وStable Diffusion وupscalers) مُسبقًا ووضعها في مجلّد `models/` قبل التشغيل.

متطلبات مبدئية
- نظام تشغيل: Linux أو Windows أو macOS
- Python 3.10+
- GPU مع CUDA (مُستحسن) أو CPU (أداء أقل)
- مساحة تخزين كافية لأوزان النماذج (عشرات إلى مئات جيجابايت حسب النماذج)

خطوات سريعة للتشغيل (مبدئي)
1. تنزيل الأوزان ووضعها:
   - models/llm/<model-files>
   - models/sd-xl/<sd-weights>
   - models/upscalers/<real-esrgan-checkpoints>

2. تهيئة البيئة:
   - أنصح باستخدام conda:
     conda create -n ai-offline python=3.10 -y
     conda activate ai-offline
     pip install -r requirements.txt

3. تشغيل الخدمات عبر Docker Compose:
   docker compose up --build
   (سوف يرفع خادم FastAPI على http://localhost:8000)

4. واجهة المستخدم:
   - افتح http://localhost:8000/docs للحصول على توثيق OpenAPI واختبار نقاط النهاية.

ملاحظات مهمة
- تنزيل الأوزان يحتاج إنترنت لمرة واحدة. بعد وضع الأوزان محليًا، لا يلزم اتصال.
- لتوليد فيديو متقدّم قد تحتاج نماذج/مكونات إضافية؛ البنية هنا قابلة للتوسيع.
- اقرأ تراخيص النماذج قبل الاستخدام التجاري.
