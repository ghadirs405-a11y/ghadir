import { NextRequest, NextResponse } from "next/server";
import ZAI from "z-ai-web-dev-sdk";

export const runtime = "nodejs";
export const maxDuration = 60;

const VALID_CATEGORIES = ["spiritual", "productivity", "self-care", "family"];
const VALID_DURATIONS = [7, 21, 40, 70, 100];
const VALID_PLATFORMS = ["instagram", "linkedin"];

const SYSTEM_PROMPT = `تو «دستیار هوشمند Habits Tracker» هستی؛ یک کوچ مهربان، پرانرژی و متخصص عادت‌سازی و برنامه‌ریزی زندگی برای کاربر فارسی‌زبان.

وظایف تو:
1. وقتی کاربر هدف، مشکل یا شرایطش را توضیح می‌دهد (مثلاً «برای کنکور برنامه بده»، «می‌خوام صبح‌ها زود بیدار بشم»، «برنامه ورزشی بساز»، «می‌خوام کمتر گوشی چک کنم»)، یک «برنامه تخصصی عادت‌سازی» مخصوص او طراحی می‌کنی.
2. وقتی کاربر سؤال می‌پرسد، احساسش را می‌گوید یا صرفاً گپ می‌زند، مثل یک کوچ واقعی و دوست‌داشتنی پاسخ می‌دهی و در صورت لزوم برنامه پیشنهاد می‌دهی.

قوانین ساخت برنامه (plan):
- بین ۳ تا ۶ عادت کاربردی، واقع‌بینانه و قابل اجرا بگذار (عادت‌های خیلی سخت انگیزه را می‌کشد).
- هر عادت شامل: name (کوتاه و واضح به فارسی، حداکثر ۵ کلمه)، icon (فقط یک ایموجی مناسب)، category (یکی از این ۴ مورد دقیقاً: spiritual برای معنویت، productivity برای بهره‌وری و درس و کار، self-care برای سلامتی و ورزش و خواب، family برای خانواده و روابط)، alarmTime (ساعت منطقی متناسب با عادت به فرمت HH:MM با ارقام انگلیسی مثل 06:30)، tip (یک نکته کوتاه برای اجرای بهتر آن عادت).
- duration برنامه باید یکی از این اعداد باشد: 7، 21، 40، 70، 100 (روز).
- name برنامه کوتاه و انگیزشی و summary یک جمله باشد.
- برنامه را با داده‌های کاربر شخصی‌سازی کن: اگر عادت مشابهی از قبل دارد، تکراری نساز؛ به استریک و درصد موفقیتش توجه کن و برنامه را متناسب با سطحش بساز (اگر مبتدی است ساده شروع کن).
- ساعت‌ها منطقی باشند: مثلاً قرآن و نماز صبح زود، مطالعه صبح یا عصر، ورزش عصر یا صبح، مرور شب قبل از خواب.

فرمت پاسخ (بسیار مهم): فقط و فقط یک JSON معتبر برگردان، بدون هیچ متن اضافه، بدون markdown و بدون بک‌تیک:
حالت گپ: {"reply":"...","plan":null}
حالت برنامه: {"reply":"...","plan":{"name":"...","summary":"...","duration":21,"habits":[{"name":"...","icon":"📚","category":"productivity","alarmTime":"06:30","tip":"..."}]}}

قوانین reply:
- همیشه فارسی، صمیمی، کوتاه (۱ تا ۴ جمله) و پرانرژی با ایموجی مناسب.
- اگر برنامه ساختی، در reply خلاصه بگو این برنامه چه کمکی می‌کند و دعوت کن دکمه «اعمال خودکار برنامه» را بزند.
- هرگز خارج از JSON چیزی ننویس.`;

const WEEKLY_REPORT_PROMPT = `تو «تحلیل‌گر هفتگی Habits Tracker» هستی؛ یک کوچ مهربان و دقیق که هر هفته یک گزارش عملکرد صمیمی و انگیزشی برای کاربر فارسی‌زبان می‌نویسد.

آمار ۷ روز گذشته کاربر را می‌گیری (درصد تکمیل عادت‌ها، تعداد تکمیل‌ها، بهترین استریک، میانگین حال و هوا، بهترین و ضعیف‌ترین روز، عادت‌های برتر و عادت‌های بدون تکمیل).

یک گزارش هفتگی واقع‌بینانه، تشویق‌کننده و عملی بنویس:
- اگر عملکرد خوب بوده جشن بگیر و اگر ضعیف بوده بدون سرزنش، امیدوارکننده برخورد کن.
- به الگوها اشاره کن (مثلاً روز خاصی ضعیف بوده یا عادتی اصلاً انجام نشده).
- پیشنهادها باید کوچک، مشخص و همین امروز قابل شروع باشند.

فرمت پاسخ (بسیار مهم): فقط و فقط یک JSON معتبر، بدون markdown و بدون بک‌تیک:
{"reply":"یک جمله کوتاه و صمیمی درباره آماده شدن گزارش","report":{"headline":"عنوان کوتاه و جذاب گزارش","summary":"۲ تا ۳ جمله تحلیل کلی هفته","highlights":["نکته مثبت ۱","نکته مثبت ۲"],"issues":["چالش یا نکته ضعف ۱"],"suggestions":["پیشنهاد عملی ۱","پیشنهاد عملی ۲","پیشنهاد عملی ۳"],"focus":"تمرکز اصلی هفته آینده در یک جمله","motivation":"یک جمله انگیزشی پایانی با ایموجی"}}

قوانین:
- همه متن‌ها فارسی و صمیمی.
- highlights، issues و suggestions هر کدام ۱ تا ۴ آیتم کوتاه (هر آیتم حداکثر یک جمله).
- اگر داده کم بود (مثلاً هیچ عادتی تکمیل نشده یا حال ثبت نشده)، محتاط باش و روی شروع کوچک و انگیزه تأکید کن.
- هرگز خارج از JSON چیزی ننویس.`;

const SOCIAL_PLAN_PROMPT = `تو «استراتژیست محتوای فضای مجازی» در اپ Habits Tracker هستی؛ متخصص تولید برنامه محتوای اینستاگرام و لینکدین برای کاربر فارسی‌زبان.

کاربر شغل یا حوزه کاری‌اش را گفته و پلتفرم‌های موردنظرش را انتخاب کرده. برای او یک برنامه محتوای دقیقاً ۴ هفته‌ای بساز؛ هر هفته برای هر پلتفرم انتخاب‌شده دقیقاً یک پست با «پرامت آماده اجرا» طراحی کن.

فرمت پاسخ (بسیار مهم): فقط و فقط یک JSON معتبر، بدون markdown و بدون بک‌تیک:
{"reply":"یک جمله کوتاه صمیمی که برنامه را معرفی می‌کند","socialPlan":{"title":"عنوان کوتاه برنامه","audience":"مخاطب هدف در یک جمله","weeks":[{"week":1,"theme":"تم همان هفته در چند کلمه","instagram":{"topic":"موضوع مشخص پست","prompt":"پرامت کامل و آماده کپی برای ابزار هوش مصنوعی","caption":"کپشن آماده انتشار با ایموجی","hashtags":["#هشتگ","#هشتگ","#هشتگ","#هشتگ"],"bestTime":"روز و ساعت پیشنهادی انتشار"},"linkedin":{"topic":"...","prompt":"...","caption":"...","hashtags":["#...","#...","#..."],"bestTime":"..."}}]}}

قوانین ساخت پرامت (مهم‌ترین بخش):
- هر پرامت بین ۳۵ تا ۶۰ کلمه و با این ساختار باشد: (۱) نوع پست و سبک تصویر/قالب، (۲) هوک ابتدایی جذاب، (۳) بدنه یا نکات اصلی، (۴) دعوت به اقدام (CTA).
- پرامت طوری نوشته شود که کاربر بتواند مستقیم آن را به ابزار هوش مصنوعی بدهد و خروجی آماده انتشار بگیرد.
- اینستاگرام: لحن صمیمی، ویژوال و کوتاه؛ مناسب ریلز/پست تصویری.
- لینکدین: لحن حرفه‌ای، آموزشی و تجربه‌محور.
- کپشن حداکثر ۳۰ کلمه با ایموجی.
- hashtags بین ۴ تا ۶ مورد، هر کدام با # شروع شود (فارسی یا انگلیسی).
- weeks دقیقاً ۴ هفته است و week از ۱ تا ۴ شماره می‌خورد.
- فقط پلتفرم‌های درخواستی کاربر را در JSON بگذار (کلید instagram/linkedin فقط اگر انتخاب شده).
- محتوای هر هفته متفاوت و پیشرونده باشد (معرفی، آموزش، اعتمادسازی/نمونه‌کار، تعامل و دعوت به همکاری).
- همه متن‌ها فارسی و متناسب با حوزه کاربر شخصی‌سازی شوند.
- هرگز خارج از JSON چیزی ننویس. یک JSON واحد؛ بدون توضیح اضافه.`;

interface ChatHabit {
  name?: string;
  icon?: string;
  category?: string;
  alarmTime?: string;
  tip?: string;
}

interface AgentPlan {
  name: string;
  summary: string;
  duration: number;
  habits: ChatHabit[];
}

interface WeeklyReport {
  headline: string;
  summary: string;
  highlights: string[];
  issues: string[];
  suggestions: string[];
  focus: string;
  motivation: string;
}

interface SocialPost {
  topic: string;
  prompt: string;
  caption: string;
  hashtags: string[];
  bestTime: string;
}

interface SocialWeek {
  week: number;
  theme: string;
  instagram?: SocialPost | null;
  linkedin?: SocialPost | null;
}

interface SocialPlan {
  title: string;
  audience: string;
  weeks: SocialWeek[];
}

function toEnglishDigits(s: string): string {
  return s
    .replace(/[۰-۹]/g, (d) => String("۰۱۲۳۴۵۶۷۸۹".indexOf(d)))
    .replace(/[٠-٩]/g, (d) => String("٠١٢٣٤٥٦٧٨٩".indexOf(d)));
}

function extractJson(raw: string): any | null {
  if (!raw) return null;
  let text = raw.trim();
  // strip markdown fences if present
  text = text.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/i, "");
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start === -1 || end === -1 || end <= start) return null;
  const candidate = text.slice(start, end + 1);
  try {
    return JSON.parse(candidate);
  } catch {
    // try to fix trailing commas
    try {
      return JSON.parse(candidate.replace(/,\s*([}\]])/g, "$1"));
    } catch {
      return null;
    }
  }
}

function sanitizePlan(plan: any): AgentPlan | null {
  if (!plan || typeof plan !== "object") return null;
  const habitsRaw = Array.isArray(plan.habits) ? plan.habits : [];
  const icons: Record<string, string> = {
    spiritual: "🕊️",
    productivity: "⚡",
    "self-care": "💖",
    family: "👨‍👩‍👧",
  };
  const habits: ChatHabit[] = habitsRaw
    .filter((h: any) => h && typeof h === "object" && typeof h.name === "string" && h.name.trim())
    .slice(0, 8)
    .map((h: any) => {
      let category = String(h.category || "productivity").trim();
      if (!VALID_CATEGORIES.includes(category)) category = "productivity";
      let alarmTime = toEnglishDigits(String(h.alarmTime || "08:00")).trim();
      if (!/^([01]?\d|2[0-3]):[0-5]\d$/.test(alarmTime)) alarmTime = "08:00";
      if (alarmTime.length === 4) alarmTime = "0" + alarmTime;
      let duration = 21;
      const d = Number(h.duration);
      if (VALID_DURATIONS.includes(d)) duration = d;
      return {
        name: String(h.name).trim().slice(0, 80),
        icon: typeof h.icon === "string" && h.icon.trim() ? [...h.icon.trim()][0] : icons[category],
        category,
        alarmTime,
        tip: typeof h.tip === "string" ? h.tip.slice(0, 140) : "",
        duration,
      };
    });
  if (habits.length === 0) return null;
  let duration = Number(plan.duration);
  if (!VALID_DURATIONS.includes(duration)) duration = 21;
  return {
    name: String(plan.name || "برنامه تخصصی من").slice(0, 60),
    summary: String(plan.summary || "").slice(0, 200),
    duration,
    habits,
  };
}

function sanitizeReport(r: any): WeeklyReport | null {
  if (!r || typeof r !== "object") return null;
  const str = (v: any, max: number) => (typeof v === "string" ? v.trim().slice(0, max) : "");
  const arr = (v: any, maxItems: number, maxLen: number) =>
    Array.isArray(v)
      ? v
          .filter((x: any) => typeof x === "string" && x.trim())
          .slice(0, maxItems)
          .map((x: string) => String(x).trim().slice(0, maxLen))
      : [];
  const headline = str(r.headline, 120);
  const summary = str(r.summary, 700);
  if (!headline && !summary) return null;
  return {
    headline: headline || "گزارش هفتگی تو",
    summary,
    highlights: arr(r.highlights, 4, 200),
    issues: arr(r.issues, 4, 200),
    suggestions: arr(r.suggestions, 4, 200),
    focus: str(r.focus, 200),
    motivation: str(r.motivation, 300),
  };
}

function sanitizePost(b: any): SocialPost | null {
  if (!b || typeof b !== "object") return null;
  const str = (v: any, max: number) => (typeof v === "string" ? v.trim().slice(0, max) : "");
  const topic = str(b.topic, 200);
  const prompt = str(b.prompt, 1400);
  if (!prompt && !topic) return null;
  const hashtags = Array.isArray(b.hashtags)
    ? b.hashtags
        .filter((h: any) => typeof h === "string" && h.trim())
        .slice(0, 8)
        .map((h: string) => {
          const t = h.trim().replace(/^#+/, "");
          return t ? "#" + t.slice(0, 40) : "";
        })
        .filter(Boolean)
    : [];
  return {
    topic,
    prompt: prompt || topic,
    caption: str(b.caption, 900),
    hashtags,
    bestTime: str(b.bestTime, 60),
  };
}

function sanitizeSocialPlan(p: any, platforms: string[]): SocialPlan | null {
  if (!p || typeof p !== "object") return null;
  const weeksRaw = Array.isArray(p.weeks) ? p.weeks.slice(0, 4) : [];
  const weeks: SocialWeek[] = [];
  weeksRaw.forEach((w: any, i: number) => {
    if (!w || typeof w !== "object") return;
    const sw: SocialWeek = {
      week: i + 1,
      theme: typeof w.theme === "string" ? w.theme.trim().slice(0, 140) : "",
    };
    if (platforms.includes("instagram")) sw.instagram = sanitizePost(w.instagram);
    if (platforms.includes("linkedin")) sw.linkedin = sanitizePost(w.linkedin);
    if (sw.instagram || sw.linkedin) weeks.push(sw);
  });
  if (weeks.length === 0) return null;
  return {
    title:
      typeof p.title === "string" && p.title.trim()
        ? p.title.trim().slice(0, 120)
        : "برنامه محتوای هفتگی",
    audience: typeof p.audience === "string" ? p.audience.trim().slice(0, 200) : "",
    weeks,
  };
}

function buildContextBlock(context: any): string {
  if (!context || typeof context !== "object") return "";
  const lines: string[] = [];
  const dateStr =
    context.dateFa && typeof context.dateFa === "string" ? context.dateFa : "";
  if (dateStr) lines.push(`تاریخ امروز: ${dateStr}`);
  if (typeof context.wakeTime === "string") lines.push(`ساعت بیدارباش تنظیمی: ${context.wakeTime}`);
  if (typeof context.streak === "number") lines.push(`استریک فعلی کاربر: ${context.streak} روز`);
  if (typeof context.completionRate7 === "number")
    lines.push(`درصد تکمیل عادت‌ها در ۷ روز گذشته: ${context.completionRate7}٪`);
  if (Array.isArray(context.habits) && context.habits.length > 0) {
    lines.push("عادت‌های فعلی کاربر:");
    context.habits.slice(0, 20).forEach((h: any, i: number) => {
      const name = typeof h?.name === "string" ? h.name : "بدون نام";
      const cat = typeof h?.category === "string" ? h.category : "";
      const streak = typeof h?.streak === "number" ? h.streak : 0;
      const done = h?.completedToday ? "انجام‌شده امروز" : "انجام‌نشده امروز";
      lines.push(`  ${i + 1}. ${name} (دسته: ${cat}، استریک: ${streak}، ${done})`);
    });
  } else {
    lines.push("کاربر هنوز هیچ عادتی ندارد.");
  }
  if (typeof context.moodToday === "number")
    lines.push(`حال و هوای امروز کاربر (از ۱ تا ۵): ${context.moodToday}`);
  return lines.join("\n");
}

function buildStatsBlock(stats: any): string {
  if (!stats || typeof stats !== "object") return "داده‌ای از کاربر موجود نیست.";
  const lines: string[] = [];
  const num = (v: any, fallback = 0) => (typeof v === "number" && isFinite(v) ? v : fallback);
  lines.push(`تعداد عادت‌های فعال: ${num(stats.totalHabits)}`);
  lines.push(
    `درصد تکمیل ۷ روز گذشته: ${num(stats.rate7)}٪ (${num(stats.totalDone)} تکمیل از ${num(stats.totalSlots)} جای ممکن)`
  );
  lines.push(`بهترین استریک فعلی: ${num(stats.bestStreak)} روز`);
  if (typeof stats.moodAvg === "number")
    lines.push(`میانگین حال و هوای هفته (از ۵): ${stats.moodAvg} (${num(stats.moodCount)} روز ثبت‌شده)`);
  else lines.push("کاربر این هفته حال و هوایی ثبت نکرده است.");
  if (stats.bestDay) lines.push(`بهترین روز هفته: ${stats.bestDay}`);
  if (stats.weakDay) lines.push(`ضعیف‌ترین روز هفته: ${stats.weakDay}`);
  if (Array.isArray(stats.topHabits) && stats.topHabits.length > 0) {
    lines.push(
      `عادت‌های برتر هفته: ${stats.topHabits
        .map((h: any) => `${h?.name || "?"} (${num(h?.done7)} از ۷ روز)`)
        .join("، ")}`
    );
  }
  if (Array.isArray(stats.zeroHabits) && stats.zeroHabits.length > 0) {
    lines.push(`عادت‌های بدون هیچ تکمیلی در ۷ روز: ${stats.zeroHabits.join("، ")}`);
  }
  if (Array.isArray(stats.perDay) && stats.perDay.length > 0) {
    lines.push(
      `روند روزانه: ${stats.perDay
        .map((d: any) => `${d?.dayFa || "?"}: ${num(d?.done)}/${num(d?.total)}`)
        .join("، ")}`
    );
  }
  return lines.join("\n");
}

async function callLLM(system: string, userContent: string, maxTokens: number): Promise<string> {
  const zai = await ZAI.create();
  const completion = await zai.chat.completions.create({
    messages: [
      { role: "system", content: system },
      { role: "user", content: userContent },
    ],
    thinking: { type: "disabled" },
    temperature: 0.75,
    max_tokens: maxTokens,
  } as any);
  return completion?.choices?.[0]?.message?.content || "";
}

async function handleChat(body: any) {
  const message: string = body?.message ? String(body.message).slice(0, 2000) : "";
  if (!message.trim()) {
    return NextResponse.json({ reply: "لطفاً یک پیام بنویس تا کمکت کنم 🙂", plan: null }, { status: 200 });
  }

  const history: Array<{ role: string; content: string }> = Array.isArray(body?.history)
    ? body.history
        .filter(
          (m: any) =>
            m &&
            (m.role === "user" || m.role === "assistant") &&
            typeof m.content === "string" &&
            m.content.trim()
        )
        .slice(-8)
        .map((m: any) => ({
          role: m.role,
          content: String(m.content).slice(0, 1200),
        }))
    : [];

  const contextBlock = buildContextBlock(body?.context);

  const messages: Array<{ role: "system" | "user" | "assistant"; content: string }> = [
    { role: "system", content: SYSTEM_PROMPT },
    ...history.map((m) => ({
      role: (m.role === "user" ? "user" : "assistant") as "user" | "assistant",
      content: m.content,
    })),
    {
      role: "user",
      content: `${contextBlock ? `داده‌های کاربر در اپلیکیشن:\n${contextBlock}\n\n` : ""}پیام کاربر: ${message}`,
    },
  ];

  let content = "";
  try {
    const zai = await ZAI.create();
    const completion = await zai.chat.completions.create({
      messages,
      thinking: { type: "disabled" },
      temperature: 0.75,
      max_tokens: 1600,
    } as any);
    content = completion?.choices?.[0]?.message?.content || "";
  } catch (e) {
    console.error("Agent LLM error:", e);
    return NextResponse.json({
      reply: "هوم! الان نمی‌توانم به سرور هوش مصنوعی وصل شوم. چند لحظه دیگر دوباره امتحان کن 🙏",
      plan: null,
    });
  }

  const parsed = extractJson(content);
  if (!parsed || typeof parsed.reply !== "string") {
    // model did not return valid JSON — treat whole text as conversational reply
    const fallback = content.trim().slice(0, 800);
    return NextResponse.json({
      reply: fallback || "پاسخی دریافت نشد، دوباره تلاش کن 🙂",
      plan: null,
    });
  }

  const plan = sanitizePlan(parsed.plan);
  return NextResponse.json({
    reply: String(parsed.reply).slice(0, 1500),
    plan,
  });
}

async function handleWeeklyReport(body: any) {
  const statsBlock = buildStatsBlock(body?.stats);
  const contextBlock = buildContextBlock(body?.context);

  try {
    const content = await callLLM(
      WEEKLY_REPORT_PROMPT,
      `آمار ۷ روز گذشته کاربر در اپلیکیشن:\n${statsBlock}${
        contextBlock ? `\n\nاطلاعات تکمیلی:\n${contextBlock}` : ""
      }\n\nحالا گزارش هفتگی او را طبق فرمت بنویس.`,
      1500
    );
    const parsed = extractJson(content);
    const report = parsed ? sanitizeReport(parsed.report) : null;
    if (!report) {
      return NextResponse.json({
        reply: "گزارش این هفته آماده نشد؛ یک بار دیگر تلاش کن 🙏",
        plan: null,
        report: null,
      });
    }
    return NextResponse.json({
      reply:
        typeof parsed?.reply === "string" && parsed.reply.trim()
          ? parsed.reply.trim().slice(0, 400)
          : "گزارش هفتگی‌ات آماده است! 📊",
      plan: null,
      report,
    });
  } catch (e) {
    console.error("Weekly report error:", e);
    return NextResponse.json({
      reply: "الان نمی‌توانم گزارش بسازم؛ چند لحظه دیگر دوباره امتحان کن 🙏",
      plan: null,
      report: null,
    });
  }
}

async function handleSocialPlan(body: any) {
  const field: string =
    body?.field ? String(body.field).slice(0, 500) : body?.message ? String(body.message).slice(0, 500) : "";
  if (!field.trim()) {
    return NextResponse.json({
      reply: "اول بنویس چه کار می‌کنی یا در چه حوزه‌ای فعالی تا برنامه محتوا برایت بسازم 🙂",
      plan: null,
      socialPlan: null,
    });
  }
  const platforms = VALID_PLATFORMS.filter((p) =>
    Array.isArray(body?.platforms) ? body.platforms.includes(p) : true
  );
  const platformFa = platforms.includes("instagram") && platforms.includes("linkedin")
    ? "اینستاگرام و لینکدین"
    : platforms.includes("instagram")
      ? "اینستاگرام"
      : "لینکدین";
  const contextBlock = buildContextBlock(body?.context);

  try {
    let content = await callLLM(
      SOCIAL_PLAN_PROMPT,
      `حوزه کاری/شغل کاربر: ${field}\nپلتفرم‌های انتخابی: ${platformFa}${
        contextBlock ? `\n\nاطلاعات تکمیلی کاربر:\n${contextBlock}` : ""
      }\n\nحالا برنامه محتوای ۴ هفته‌ای را طبق فرمت بساز.`,
      4000
    );
    let parsed = extractJson(content);
    let socialPlan = parsed ? sanitizeSocialPlan(parsed.socialPlan, platforms) : null;
    if (!socialPlan) {
      // Retry once with a stricter conciseness instruction (output was likely truncated)
      console.error(
        "Social plan first attempt failed, retrying. rawLen:",
        content.length,
        "tail:",
        content.slice(-120)
      );
      content = await callLLM(
        SOCIAL_PLAN_PROMPT,
        `حوزه کاری/شغل کاربر: ${field}\nپلتفرم‌های انتخابی: ${platformFa}\n\nپاسخ قبلی بیش از حد طولانی بود و قطع شد. این بار بسیار فشرده بنویس: پرامت هر پست حداکثر ۴۰ کلمه، کپشن حداکثر ۲۰ کلمه. فقط JSON کامل و کوتاه.`,
        3500
      );
      parsed = extractJson(content);
      socialPlan = parsed ? sanitizeSocialPlan(parsed.socialPlan, platforms) : null;
    }
    if (!socialPlan) {
      return NextResponse.json({
        reply: "برنامه محتوا ساخته نشد؛ یک بار دیگر تلاش کن 🙏",
        plan: null,
        socialPlan: null,
      });
    }
    return NextResponse.json({
      reply:
        typeof parsed?.reply === "string" && parsed.reply.trim()
          ? parsed.reply.trim().slice(0, 400)
          : `برنامه محتوای ${platformFa} آماده شد! 🎉`,
      plan: null,
      socialPlan,
    });
  } catch (e) {
    console.error("Social plan error:", e);
    return NextResponse.json({
      reply: "الان نمی‌توانم برنامه محتوا بسازم؛ چند لحظه دیگر دوباره امتحان کن 🙏",
      plan: null,
      socialPlan: null,
    });
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => null);
    const mode = body?.mode ? String(body.mode) : "chat";

    if (mode === "weekly-report") return await handleWeeklyReport(body);
    if (mode === "social-plan") return await handleSocialPlan(body);
    return await handleChat(body);
  } catch (e) {
    console.error("Agent API error:", e);
    return NextResponse.json(
      {
        reply: "خطایی پیش آمد. لطفاً دوباره تلاش کن 🙏",
        plan: null,
      },
      { status: 500 }
    );
  }
}
