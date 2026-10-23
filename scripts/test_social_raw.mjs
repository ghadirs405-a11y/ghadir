import ZAI from 'z-ai-web-dev-sdk';

const SYS = `تو «استراتژیست محتوای فضای مجازی» در اپ Habits Tracker هستی؛ متخصص تولید برنامه محتوای اینستاگرام و لینکدین برای کاربر فارسی‌زبان.
کاربر شغل یا حوزه کاری‌اش را گفته و پلتفرم‌های موردنظرش را انتخاب کرده. برای او یک برنامه محتوای دقیقاً ۴ هفته‌ای بساز؛ هر هفته برای هر پلتفرم انتخاب‌شده دقیقاً یک پست با «پرامت آماده اجرا» طراحی کن.

فرمت پاسخ (بسیار مهم): فقط و فقط یک JSON معتبر، بدون markdown و بدون بک‌تیک:
{"reply":"یک جمله کوتاه صمیمی","socialPlan":{"title":"عنوان کوتاه برنامه","audience":"مخاطب هدف در یک جمله","weeks":[{"week":1,"theme":"تم همان هفته در چند کلمه","instagram":{"topic":"موضوع مشخص پست","prompt":"پرامت کامل و آماده کپی برای ابزار هوش مصنوعی","caption":"کپشن آماده انتشار با ایموجی","hashtags":["#هشتگ","#هشتگ"],"bestTime":"روز و ساعت پیشنهادی"},"linkedin":{"topic":"...","prompt":"...","caption":"...","hashtags":["#..."],"bestTime":"..."}}]}}

قوانین:
- پرامت کامل و اجرایی باشد (موضوع، ساختار، لحن، CTA) اما فشرده؛ حداکثر ۵۰ کلمه.
- weeks دقیقاً ۴ هفته. فقط پلتفرم‌های درخواستی.
- هرگز خارج از JSON چیزی ننویس.`;

const zai = await ZAI.create();
const completion = await zai.chat.completions.create({
  messages: [
    { role: 'system', content: SYS },
    { role: 'user', content: 'حوزه کاری/شغل کاربر: در حوزه هوش مصنوعی کار می‌کنم\nپلتفرم‌های انتخابی: اینستاگرام و لینکدین\n\nحالا برنامه محتوای ۴ هفته‌ای را طبق فرمت بساز.' },
  ],
  thinking: { type: 'disabled' },
  temperature: 0.75,
  max_tokens: 3000,
});
const c = completion?.choices?.[0]?.message?.content || '';
console.log('RAW LEN:', c.length);
console.log('HEAD:', c.slice(0, 120));
console.log('TAIL:', c.slice(-200));
const cleaned = c.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '');
try {
  const j = JSON.parse(cleaned);
  console.log('PARSE OK, weeks:', j?.socialPlan?.weeks?.length);
} catch (e) {
  console.log('PARSE FAIL:', e.message);
}
console.log('finish_reason:', completion?.choices?.[0]?.finish_reason);
