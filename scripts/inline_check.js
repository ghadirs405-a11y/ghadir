
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            surface: '#fcf8ff',
            'surface-container': '#efebff',
            'surface-container-low': '#f6f2ff',
            'surface-container-high': '#e9e5ff',
            'surface-container-highest': '#e3dfff',
            'on-surface': '#181445',
            'on-surface-variant': '#4a4455',
            primary: '#630ed4',
            'primary-container': '#7c3aed',
            'on-primary': '#ffffff',
            'on-primary-container': '#ede0ff',
            secondary: '#6b38d4',
            'secondary-container': '#8455ef',
            'on-secondary': '#ffffff',
            tertiary: '#843700',
            'tertiary-container': '#aa4900',
            'on-tertiary': '#ffffff',
            'tertiary-fixed': '#ffdbca',
            'on-tertiary-fixed': '#341100',
            error: '#ba1a1a',
            outline: '#7b7487',
            'outline-variant': '#ccc3d8',
            spiritual: '#a78bfa',
            productivity: '#34d399',
            'self-care': '#f472b6',
            gold: '#fbbf24',
            silver: '#94a3b8',
            bronze: '#d97706',
            'agent-primary': '#8b5cf6',
            'agent-secondary': '#06b6d4',
            'agent-accent': '#f59e0b'
          },
          fontFamily: { sans: ['Vazirmatn', 'sans-serif'] },
          borderRadius: { '4xl': '2rem' }
        }
      }
    }
  
;

    // ================= STATE =================
    const STORAGE_KEY = 'habits_tracker_agent_v1';
    const today = () => new Date().toISOString().split('T')[0];
    const currentMonth = () => new Date().toISOString().slice(0, 7);

    const defaultState = {
      habits: [],
      moodLog: [],
      journal: {},
      journalingResponses: {},
      notebookEntries: [],
      settings: { 
        sound: true, 
        notifications: true, 
        masterVolume: 50, 
        weather: 'sunny', 
        batterySaver: false, 
        breathType: '478',
        // NEW: Agent settings
        agent: {
          wakeTime: '06:30',
          wakeEnabled: false,
          voiceEnabled: false,
          lastCheckin: null,
          checkinHistory: [],
          moodHistory: []
        }
      },
      chellehStartDate: null,
      isFirstRun: true,
      notifications: [],
      musicTracks: [],
      musicCollections: []
    };

    let state;
    
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        state = JSON.parse(saved);
        // Merge agent settings if missing
        if (!state.settings.agent) state.settings.agent = defaultState.settings.agent;
        if (!state.moodLog) state.moodLog = [];
        if (!state.journal) state.journal = {};
        if (!state.journalingResponses) state.journalingResponses = {};
        if (!state.notebookEntries) state.notebookEntries = [];
        if (!state.settings) state.settings = defaultState.settings;
        if (!state.chellehStartDate) state.chellehStartDate = today();
        if (!state.notifications) state.notifications = [];
        if (!state.agentChat) state.agentChat = [];
        if (state.agentWeeklyReport === undefined) state.agentWeeklyReport = null;
        if (!Array.isArray(state.agentSocialPlans)) state.agentSocialPlans = [];
        if (!Array.isArray(state.musicTracks)) state.musicTracks = [];
        if (!Array.isArray(state.musicCollections)) state.musicCollections = [];
        state.musicTracks.forEach(t => {
          if (!t.schedule) t.schedule = { enabled: false, time: '07:00', lastPlayedOn: null };
          if (!t.category) t.category = 'calm';
          if (typeof t.playCount !== 'number') t.playCount = 0;
          if (typeof t.favorite !== 'boolean') t.favorite = false;
          if (!t.emoji) t.emoji = '🎵';
        });
        if (state.isFirstRun === undefined) state.isFirstRun = false;
        state.habits.forEach(h => { 
          if (!h.notes) h.notes = []; 
          if (!h.category) h.category = 'productivity';
          if (!h.duration) h.duration = 21;
          if (!h.completions) h.completions = {};
          if (!h.streak) h.streak = 0;
        });
      } else {
        state = JSON.parse(JSON.stringify(defaultState));
        state.chellehStartDate = today();
      }
    } catch (e) {
      state = JSON.parse(JSON.stringify(defaultState));
      state.chellehStartDate = today();
    }

    function saveState() { 
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); 
    }

    // ================= CATEGORIES =================
    const categories = {
      spiritual: { label: 'معنوی و پاکی', color: '#a78bfa', icon: 'self_improvement', emoji: '🕊️' },
      productivity: { label: 'بهره‌وری و کار', color: '#34d399', icon: 'bolt', emoji: '' },
      'self-care': { label: 'مراقبت از خود', color: '#f472b6', icon: 'favorite', emoji: '💖' },
      family: { label: 'خانواده و مهر', color: '#843700', icon: 'family_restroom', emoji: '👨‍‍👧' }
    };

    // ================= QUOTES =================
    const quotes = [
      "ریشه‌های اراده در سکوت رشد می‌کنند و شاخه‌های آرامش، سایه‌بان کانون گرم خانواده می‌شوند.",
      "نظم، پل میان اهداف و دستاوردهاست.",
      "آینده متعلق به کسانی است که به زیبایی رویاهایشان باور دارند.",
      "هر روز فرصتی جدید برای ساختن نسخه بهتری از خودت است.",
      "استمرار، کلید تبدیل غیرممکن به ممکن است.",
      "ذهن آرام، قوی‌ترین سلاح برای فتح دنیای بیرون است.",
      "عادت‌های کوچک، زندگی‌های بزرگ می‌سازند.",
      "تو همان چیزی هستی که مکرراً انجام می‌دهی.",
      "رشد، نتیجه‌ی تصمیم‌های کوچک روزمره است.",
      "هر قدم کوچک، تو را به نسخه‌ی ایده‌آلت نزدیک‌تر می‌کند.",
      "تمرکز، هنر نادیده گرفتن چیزهای بی‌اهمیت است.",
      "ریشه‌های اراده در سکوت رشد می‌کنند.",
      "امروز، بذر فردای توست.",
      "باغبان صبور، زیباترین گل‌ها را می‌پروراند.",
      "ذهنت باغ توست؛ آن را با افکار زیبا آبیار.",
      "از امروز شروع کن، نه از شنبه.",
      "نظم شخصی، آزادی واقعی می‌آفریند.",
      "استقامت، هنر ادامه دادن وقتی همه چیز سخت می‌شود.",
      "تغییر، با یک تصمیم کوچک آغاز می‌شود.",
      "آرامش، پاداش ذهنی است که تمرین کرده."
    ];
    let currentQuoteIndex = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24) % quotes.length;

    function setDailyQuote() {
      document.getElementById('dailyQuote').textContent = `«${quotes[currentQuoteIndex]}»`;
    }

    // ================= AUDIO ENGINE =================
    let audioCtx = null;
    let activeSounds = {};
    let masterGain = null;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        masterGain = audioCtx.createGain();
        masterGain.gain.value = (state.settings.masterVolume || 50) / 100;
        masterGain.connect(audioCtx.destination);
      }
      if (audioCtx.state === 'suspended') audioCtx.resume();
    }

    function createNoiseBuffer(type = 'white', duration = 2) {
      const sampleRate = audioCtx.sampleRate;
      const length = sampleRate * duration;
      const buffer = audioCtx.createBuffer(1, length, sampleRate);
      const data = buffer.getChannelData(0);
      let lastOut = 0;
      for (let i = 0; i < length; i++) {
        const white = Math.random() * 2 - 1;
        if (type === 'white') data[i] = white;
        else if (type === 'pink' || type === 'brown') {
          data[i] = (lastOut + (0.02 * white)) / 1.02;
          lastOut = data[i];
          data[i] *= 3.5;
        }
      }
      return buffer;
    }

    function playCrystalChime() {
      if (state.settings.batterySaver) return;
      initAudio();
      const frequencies = [1318.51, 1567.98, 2093.00, 2637.02];
      const now = audioCtx.currentTime;
      const gain = audioCtx.createGain();
      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(0.15, now + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
      gain.connect(masterGain);
      frequencies.forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const oscGain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        oscGain.gain.setValueAtTime(0, now);
        oscGain.gain.linearRampToValueAtTime(0.3 / (i + 1), now + 0.01 + i * 0.05);
        oscGain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
        osc.connect(oscGain);
        oscGain.connect(gain);
        osc.start(now + i * 0.05);
        osc.stop(now + 1.5);
      });
    }

    // NEW: Text-to-Speech for Agent
    function speakText(text) {
      if (!state.settings.agent.voiceEnabled) return;
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'fa-IR';
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        window.speechSynthesis.speak(utterance);
      }
    }
    // ================= NOTIFICATIONS =================
    function updateHeaderNotifBadge() {
      const badge = document.getElementById('headerNotifBadge');
      if (!badge) return;
      const unread = state.notifications.filter(n => !n.read).length;
      badge.textContent = toPersian(unread);
      badge.style.display = unread > 0 ? 'flex' : 'none';
    }
    function addNotification(type, title, message, icon) {
      const notification = {
        id: 'n' + Date.now(),
        type,
        title,
        message,
        icon,
        time: new Date().toISOString(),
        read: false
      };
      state.notifications.unshift(notification);
      if (state.notifications.length > 20) {
        state.notifications = state.notifications.slice(0, 20);
      }
      saveState();
      renderNotifications();
    }

    function renderNotifications() {
      const container = document.getElementById('notificationsList');
      if (!container) return;
      updateHeaderNotifBadge();
      
      if (state.notifications.length === 0) {
        container.innerHTML = `
          <div class="text-center text-on-surface-variant text-xs py-8">
            <span class="material-symbols-outlined text-4xl opacity-30 block mb-2">notifications_none</span>
            <p>هنوز اعلانی ندارید</p>
            <p class="text-[10px] mt-1">با تکمیل عادت‌ها، اعلان‌ها اینجا نمایش داده می‌شوند</p>
          </div>
        `;
        document.getElementById('notificationCount').textContent = '۰';
        return;
      }

      const unreadCount = state.notifications.filter(n => !n.read).length;
      document.getElementById('notificationCount').textContent = toPersian(unreadCount);

      container.innerHTML = state.notifications.map(notif => {
        const d = new Date(notif.time);
        const timeStr = d.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
        const dateStr = d.toLocaleDateString('fa-IR', { day: 'numeric', month: 'short' });
        const iconColors = {
          'habit': 'bg-primary/10 text-primary',
          'streak': 'bg-tertiary-fixed text-tertiary',
          'achievement': 'bg-secondary/10 text-secondary',
          'reminder': 'bg-surface-container-low text-on-surface-variant',
          'agent': 'bg-agent-primary/10 text-agent-primary'
        };
        const iconEmojis = {
          'habit': '️',
          'streak': '',
          'achievement': '🏆',
          'reminder': '⏰',
          'agent': '🤖'
        };
        
        return `
          <div class="notification-item ${notif.read ? '' : 'unread'}" onclick="markNotificationRead('${notif.id}')">
            <div class="flex items-start gap-3">
              <div class="notification-icon ${iconColors[notif.type] || iconColors.reminder}">
                ${iconEmojis[notif.type] || notif.icon || '📌'}
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-bold text-on-surface mb-0.5">${notif.title}</div>
                <div class="text-[11px] text-on-surface-variant leading-relaxed">${notif.message}</div>
                <div class="notification-time">${dateStr} • ${timeStr}</div>
              </div>
              ${!notif.read ? '<div class="w-2 h-2 rounded-full bg-primary flex-shrink-0 mt-2"></div>' : ''}
            </div>
          </div>
        `;
      }).join('');
    }

    function markNotificationRead(id) {
      const notif = state.notifications.find(n => n.id === id);
      if (notif && !notif.read) {
        notif.read = true;
        saveState();
        renderNotifications();
      }
    }

    function clearAllNotifications() {
      if (confirm('آیا مطمئن هستید که می‌خواهید همه اعلان‌ها را پاک کنید؟')) {
        state.notifications = [];
        saveState();
        renderNotifications();
      }
    }

    // ================= AI AGENT: CHAT & AUTOMATION ENGINE =================
    let agentChatBusy = false;

    function getAgentContext() {
      const t = today();
      const habitList = state.habits.map(h => ({
        name: h.name,
        category: h.category,
        streak: h.streak || 0,
        duration: h.duration,
        completedToday: !!h.completions[t]
      }));
      let totalSlots = 0, doneSlots = 0;
      for (let i = 0; i < 7; i++) {
        const d = new Date(); d.setDate(d.getDate() - i);
        const ds = d.toISOString().split('T')[0];
        state.habits.forEach(h => { totalSlots++; if (h.completions[ds]) doneSlots++; });
      }
      const rate = totalSlots > 0 ? Math.round((doneSlots / totalSlots) * 100) : 0;
      const moodToday = (state.moodLog || []).find(m => m.date === t);
      let dateFa = '';
      try { dateFa = new Date().toLocaleDateString('fa-IR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }); } catch (e) {}
      return {
        dateFa: dateFa,
        wakeTime: (state.settings.agent && state.settings.agent.wakeTime) || '06:30',
        streak: calculateCurrentStreak(),
        completionRate7: rate,
        habits: habitList,
        moodToday: moodToday ? moodToday.score : undefined
      };
    }

    function seedAgentWelcome() {
      if (!Array.isArray(state.agentChat)) state.agentChat = [];
      if (state.agentChat.length === 0) {
        state.agentChat.push({
          id: 'm' + Date.now(),
          role: 'agent',
          content: 'سلام! من ایجنت اتوماسیون هوشمند تو هستم 🤖✨\nکافیه بگی چه هدفی داری یا چه برنامه‌ای می‌خوای — مثلاً «برای کنکور برنامه بده» یا «می‌خوام صبح‌ها زود بیدار شم» — تا یک برنامه تخصصی عادت‌سازی برات طراحی کنم و با یک کلیک، خودکار روی برنامه‌هات نصبش کنم.\nاز وضعیت عادت‌ها و استریک‌هات هم خبر دارم؛ هر سوالی داری بپرس!\nهر هفته یک «گزارش هفتگی» خودکار از پیشرفتت می‌سازم (تب 📈) و در تب «📱 فضای مجازی» اگر شغلت را بگویی، برنامه محتوای اینستاگرام و لینکدین با پرامت آماده به‌ات می‌دهم. 💜',
          plan: null,
          ts: Date.now()
        });
        saveState();
      }
      renderAgentChat();
    }

    function showAgentTyping(show) {
      const row = document.getElementById('agentTypingRow');
      if (!row) return;
      if (show) {
        row.classList.add('visible');
        setTimeout(() => { try { row.scrollIntoView({ block: 'end', behavior: 'smooth' }); } catch (e) {} }, 50);
      } else {
        row.classList.remove('visible');
      }
    }

    function agentPlanCardHtml(plan, msgId) {
      const catLabels = { spiritual: '🕊️ معنوی', productivity: '⚡ بهره‌وری', 'self-care': '💖 خودمراقبتی', family: '👨‍👩‍👧 خانواده' };
      let habitsHtml = '';
      (plan.habits || []).forEach(h => {
        habitsHtml += `
          <div class="agent-plan-habit">
            <div class="agent-plan-habit-icon">${h.icon || '🏔️'}</div>
            <div class="flex-1 min-w-0">
              <div class="agent-plan-habit-name">${escapeHtml(h.name || '')}</div>
              <div class="agent-plan-habit-meta">⏰ ${toPersian(h.alarmTime || '--:--')} · ${catLabels[h.category] || '⚡ بهره‌وری'} · ${toPersian(h.duration || plan.duration || 21)} روزه</div>
              ${h.tip ? `<div class="agent-plan-habit-tip">💡 ${escapeHtml(h.tip)}</div>` : ''}
            </div>
          </div>
        `;
      });
      return `
        <div class="agent-plan-card">
          <div class="agent-plan-head">
            <div class="agent-plan-name">🏔️ ${escapeHtml(plan.name || 'برنامه تخصصی')}</div>
            <div class="agent-plan-summary">${escapeHtml(plan.summary || '')}</div>
            <div class="agent-plan-meta">
              <span class="agent-plan-pill">📅 ${toPersian(plan.duration || 21)} روز</span>
              <span class="agent-plan-pill">✅ ${toPersian((plan.habits || []).length)} عادت</span>
            </div>
          </div>
          <div class="agent-plan-habits">${habitsHtml}</div>
          <div class="agent-plan-foot">
            <button onclick="applyAgentPlan('${msgId}')" class="agent-btn agent-btn-primary flex-1">
              <span class="material-symbols-outlined text-[16px]">bolt</span>
              اعمال خودکار برنامه
            </button>
          </div>
        </div>
      `;
    }

    function renderAgentChat() {
      const container = document.getElementById('agentChatMessages');
      if (!container) return;
      const msgs = Array.isArray(state.agentChat) ? state.agentChat : [];
      if (msgs.length === 0) {
        container.innerHTML = '<div class="text-center text-on-surface-variant text-xs py-6">گفتگویی وجود ندارد؛ اولین پیامت را بنویس! ✨</div>';
        return;
      }
      let html = '';
      msgs.forEach(m => {
        if (m.role === 'user') {
          html += `<div class="agent-msg-row me"><div class="agent-msg me">${escapeHtml(m.content).replace(/\n/g, '<br>')}</div></div>`;
        } else {
          let planHtml = '';
          if (m.plan && !m.applied) {
            planHtml = agentPlanCardHtml(m.plan, m.id);
          } else if (m.plan && m.applied) {
            planHtml = `<div class="agent-plan-applied">✅ این برنامه اعمال شد — ${toPersian(m.appliedCount || 0)} عادت به برنامه‌های تو اضافه شد</div>`;
          }
          html += `<div class="agent-msg-row bot"><div class="agent-msg-avatar">🤖</div><div class="agent-msg bot">${escapeHtml(m.content).replace(/\n/g, '<br>')}${planHtml}</div></div>`;
        }
      });
      container.innerHTML = html;
      container.scrollTop = container.scrollHeight;
    }

    function pushAgentMessage(role, content, plan) {
      if (!Array.isArray(state.agentChat)) state.agentChat = [];
      const entry = {
        id: 'm' + Date.now() + Math.floor(Math.random() * 1000),
        role: role,
        content: content,
        plan: plan || null,
        ts: Date.now()
      };
      state.agentChat.push(entry);
      if (state.agentChat.length > 50) state.agentChat = state.agentChat.slice(-50);
      saveState();
      renderAgentChat();
      return entry;
    }

    async function sendAgentMessage(text) {
      const input = document.getElementById('agentChatInput');
      const msg = (typeof text === 'string' && text.trim()) ? text.trim() : (input ? input.value.trim() : '');
      if (!msg || agentChatBusy) return;
      if (input) input.value = '';
      pushAgentMessage('user', msg);
      agentChatBusy = true;
      const btn = document.getElementById('agentSendBtn');
      if (btn) btn.disabled = true;
      showAgentTyping(true);
      try {
        const history = (state.agentChat || []).slice(0, -1)
          .filter(m => m.role === 'user' || m.role === 'agent')
          .slice(-8)
          .map(m => ({ role: m.role === 'user' ? 'user' : 'assistant', content: m.content }));
        const res = await fetch('/api/agent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: msg,
            history: history,
            context: getAgentContext()
          })
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        showAgentTyping(false);
        const reply = (data && data.reply) ? data.reply : 'پاسخی دریافت نشد 🙏';
        const plan = (data && data.plan) ? data.plan : null;
        pushAgentMessage('agent', reply, plan);
        if (plan) {
          playCrystalChime();
          updateAgentBadge();
          addNotification('agent', 'برنامه آماده شد!', `برنامه «${plan.name}» با ${toPersian(plan.habits.length)} عادت آماده اعمال است.`, 'auto_awesome');
        }
        if (state.settings.agent && state.settings.agent.voiceEnabled) speakText(reply);
      } catch (e) {
        showAgentTyping(false);
        pushAgentMessage('agent', 'اوپس! ارتباط با مغز هوشمندم برقرار نشد 📡 لطفاً چند لحظه بعد دوباره امتحان کن.');
      } finally {
        agentChatBusy = false;
        if (btn) btn.disabled = false;
        showAgentTyping(false);
      }
    }

    function applyAgentPlan(msgId) {
      const msg = (state.agentChat || []).find(m => m.id === msgId);
      if (!msg || !msg.plan) return;
      if (msg.applied) { showToast('این برنامه قبلاً اعمال شده ✅'); return; }
      const plan = msg.plan;
      const fallbackIcons = { spiritual: '🕊️', productivity: '⚡', 'self-care': '💖', family: '👨‍👩‍👧' };
      let added = 0, skipped = 0;
      (plan.habits || []).forEach(h => {
        const name = String(h.name || '').trim();
        if (!name) return;
        if (state.habits.some(x => (x.name || '').trim() === name)) { skipped++; return; }
        state.habits.push({
          id: 'h' + Date.now() + Math.floor(Math.random() * 100000),
          name: name,
          icon: h.icon || fallbackIcons[h.category] || '🏔️',
          category: h.category || 'productivity',
          completions: {},
          streak: 0,
          alarmTime: h.alarmTime || '08:00',
          alarmEnabled: true,
          notes: [],
          duration: plan.duration || 21
        });
        added++;
      });
      msg.applied = true;
      msg.appliedCount = added;
      saveState();
      renderAll();
      renderAgentChat();
      updateAgentBadge();
      if (added > 0) {
        triggerConfetti();
        playCrystalChime();
        showToast(`برنامه «${plan.name}» فعال شد! ${toPersian(added)} عادت جدید اضافه شد 🎉`);
        addNotification('habit', 'برنامه جدید فعال شد', `${toPersian(added)} عادت از برنامه «${plan.name}» به روزهای تو اضافه شد.`, 'auto_awesome');
      } else {
        showToast('همه عادت‌های این برنامه از قبل وجود داشتند 🙂');
      }
    }

    function clearAgentChat() {
      state.agentChat = [];
      saveState();
      seedAgentWelcome();
      showToast('گفتگو پاک شد 🧹');
    }

    // ================= AI AGENT: SOCIAL MEDIA CONTROL =================
    let socialPlanBusy = false;
    const socialPlatforms = { instagram: true, linkedin: true };

    const socialFieldChips = [
      { icon: '🤖', label: 'هوش مصنوعی', text: 'در حوزه هوش مصنوعی کار می‌کنم و می‌خواهم هر هفته یک پست آموزشی منتشر کنم' },
      { icon: '💻', label: 'برنامه‌نویسی', text: 'برنامه‌نویس هستم و می‌خواهم تجربه‌ها و پروژه‌های فنی‌ام را به اشتراک بگذارم' },
      { icon: '🎓', label: 'آموزش', text: 'معلم و مدرس هستم و می‌خواهم محتوای آموزشی تولید کنم' },
      { icon: '💪', label: 'فیتنس', text: 'مربی تناسب اندام هستم و می‌خواهم برنامه‌های ورزشی و سبک زندگی سالم معرفی کنم' },
      { icon: '🍳', label: 'آشپزی', text: 'آشپز هستم و می‌خواهم دستورپخت‌های خاصم را نمایش بدهم' },
      { icon: '🎨', label: 'طراحی', text: 'طراح گرافیک هستم و می‌خواهم نمونه‌کارهایم را نشان بدهم' }
    ];

    function setSocialField(i) {
      const inp = document.getElementById('agentSocialField');
      if (inp) inp.value = socialFieldChips[i].text;
    }

    function renderSocialChips() {
      const wrap = document.getElementById('agentSocialChips');
      if (!wrap) return;
      wrap.innerHTML = socialFieldChips.map((c, i) =>
        `<button class="agent-quick-chip" onclick="setSocialField(${i})">${c.icon} ${c.label}</button>`
      ).join('');
    }

    function toggleSocialPlatform(btn) {
      const p = btn.dataset.platform;
      socialPlatforms[p] = !socialPlatforms[p];
      btn.classList.toggle('active', socialPlatforms[p]);
    }

    function renderSocialTab() {
      renderSocialChips();
      const wrap = document.getElementById('agentSocialPlans');
      if (!wrap) return;
      const plans = Array.isArray(state.agentSocialPlans) ? state.agentSocialPlans : [];
      if (plans.length === 0) {
        wrap.innerHTML = '<div class="agent-insight-card"><div class="agent-bubble-text">حوزه کاری‌ات را بنویس (مثلاً «در حوزه هوش مصنوعی کار می‌کنم») تا برایت یک برنامه محتوای ۴ هفته‌ای بسازم؛ هر هفته دقیقاً یک پست برای اینستاگرام و لینکدین با پرامت آماده کپی، کپشن، هشتگ و بهترین زمان انتشار 📱✨</div></div>';
        return;
      }
      const platMeta = { instagram: '📸 اینستاگرام', linkedin: '💼 لینکدین' };
      wrap.innerHTML = plans.map(p => {
        const plan = p.plan || {};
        const weeksHtml = (plan.weeks || []).map(w => {
          const plats = ['instagram', 'linkedin'].filter(k => w[k]).map(k => {
            const b = w[k] || {};
            return `
              <div class="agent-social-platform">
                <div class="agent-social-platform-title">${platMeta[k]}</div>
                ${b.topic ? `<div class="agent-social-meta">🎯 موضوع: ${escapeHtml(b.topic)}</div>` : ''}
                <div class="agent-prompt-box">${escapeHtml(b.prompt || '')}<button class="agent-copy-btn" onclick="copySocialPrompt('${p.id}', ${w.week || 0}, '${k}')" title="کپی پرامت"><span class="material-symbols-outlined text-[13px]">content_copy</span></button></div>
                ${b.caption ? `<div class="agent-social-meta">✍️ کپشن آماده: ${escapeHtml(b.caption)}</div>` : ''}
                ${b.hashtags && b.hashtags.length ? `<div class="agent-social-meta">#️⃣ ${b.hashtags.map(escapeHtml).join(' ')}</div>` : ''}
                ${b.bestTime ? `<div class="agent-social-meta">⏰ بهترین زمان انتشار: ${escapeHtml(b.bestTime)}</div>` : ''}
              </div>`;
          }).join('');
          return `<div class="agent-social-week">🗓️ هفته ${toPersian(w.week || '')} — ${escapeHtml(w.theme || '')}</div>${plats}`;
        }).join('');
        return `
          <div class="agent-social-card">
            <div class="agent-plan-name">🚀 ${escapeHtml(plan.title || 'برنامه محتوای هفتگی')}</div>
            ${plan.audience ? `<div class="agent-plan-summary">👥 مخاطب هدف: ${escapeHtml(plan.audience)}</div>` : ''}
            <div class="agent-report-date">حوزه: ${escapeHtml(p.field || '')} · ${new Date(p.createdAt || Date.now()).toLocaleDateString('fa-IR', { day: 'numeric', month: 'long' })}</div>
            ${weeksHtml}
            <div class="agent-plan-foot">
              <button onclick="applySocialHabit('${p.id}')" class="agent-btn agent-btn-primary flex-1">
                <span class="material-symbols-outlined text-[16px]">notifications_active</span>
                یادآور پست هفتگی
              </button>
              <button onclick="deleteSocialPlan('${p.id}')" class="agent-btn agent-btn-secondary" title="حذف برنامه">
                <span class="material-symbols-outlined text-[16px]">delete</span>
              </button>
            </div>
          </div>`;
      }).join('');
    }

    async function generateSocialPlan() {
      if (socialPlanBusy) return;
      const fieldInput = document.getElementById('agentSocialField');
      const field = fieldInput ? fieldInput.value.trim() : '';
      const platforms = Object.keys(socialPlatforms).filter(k => socialPlatforms[k]);
      if (!field) { showToast('اول بنویس چه کار می‌کنی یا در چه حوزه‌ای هستی 🙂'); return; }
      if (platforms.length === 0) { showToast('حداقل یک پلتفرم انتخاب کن 📱'); return; }
      socialPlanBusy = true;
      const btn = document.getElementById('agentSocialBtn');
      const oldHtml = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">hourglass_top</span> در حال طراحی برنامه محتوا...'; }
      try {
        const res = await fetch('/api/agent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mode: 'social-plan', field: field, platforms: platforms, context: getAgentContext() })
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        const plan = data && data.socialPlan;
        if (!plan || !Array.isArray(plan.weeks) || plan.weeks.length === 0) throw new Error('bad plan');
        if (!Array.isArray(state.agentSocialPlans)) state.agentSocialPlans = [];
        state.agentSocialPlans.unshift({
          id: 'sp' + Date.now(),
          field: field,
          platforms: platforms,
          createdAt: Date.now(),
          plan: plan
        });
        state.agentSocialPlans = state.agentSocialPlans.slice(0, 3);
        saveState();
        renderSocialTab();
        playCrystalChime();
        showToast('برنامه محتوای ' + toPersian(plan.weeks.length) + ' هفته‌ای آماده شد! 🎉');
        addNotification('agent', 'برنامه محتوا آماده شد', '«' + (plan.title || 'برنامه محتوا') + '» با پرامت‌های آماده در تب فضای مجازی ایجنت ذخیره شد.', 'smartphone');
      } catch (e) {
        showToast('ساخت برنامه محتوا ناموفق بود؛ دوباره تلاش کن 🙏');
      } finally {
        socialPlanBusy = false;
        if (btn) { btn.disabled = false; btn.innerHTML = oldHtml; }
      }
    }

    function buildFullPostPrompt(b, platform) {
      const tone = platform === 'instagram'
        ? 'لحن صمیمی و پرانرژی، مناسب اینستاگرام'
        : 'لحن حرفه‌ای و آموزشی، مناسب لینکدین';
      let t = '';
      if (b.topic) t += 'یک پست با موضوع «' + b.topic + '» برام بنویس.\n';
      if (b.prompt) t += 'شرح پست: ' + b.prompt + '\n';
      t += 'ساختار: هوک جذاب در خط اول، بدنه آموزشی کوتاه (۳ تا ۵ نکته)، دعوت به اقدام در انتها.\n';
      t += tone + '.\n';
      t += 'خروجی: ۱) متن کامل پست ۲) پیشنهاد تصویر یا قالب ۳) پنج هشتگ مرتبط.';
      return t;
    }

    function copySocialPrompt(planId, week, platform) {
      const p = (state.agentSocialPlans || []).find(x => x.id === planId);
      if (!p || !p.plan) return;
      const w = (p.plan.weeks || []).find(x => Number(x.week) === Number(week));
      if (!w || !w[platform]) return;
      const b = w[platform];
      let text = buildFullPostPrompt(b, platform);
      if (b.caption) text += '\n\nکپشن آماده:\n' + b.caption;
      if (b.hashtags && b.hashtags.length) text += '\n\nهشتگ‌ها: ' + b.hashtags.join(' ');
      copyToClipboard(text, 'پرامت کامل کپی شد! ببرش به ابزار هوش مصنوعی 📋');
    }

    function copyToClipboard(text, okMsg) {
      const done = () => showToast(okMsg || 'کپی شد 📋');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
      } else fallbackCopy(text, done);
    }

    function fallbackCopy(text, done) {
      try {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        done();
      } catch (e) { showToast('کپی خودکار ممکن نشد؛ دستی کپی کن 🙏'); }
    }

    function applySocialHabit(planId) {
      const p = (state.agentSocialPlans || []).find(x => x.id === planId);
      if (!p) return;
      const name = '✍️ آماده‌سازی پست هفتگی';
      if (state.habits.some(h => h.name === name)) { showToast('یادآور از قبل ساخته شده ✅'); return; }
      state.habits.push({
        id: 'h' + Date.now() + Math.floor(Math.random() * 100000),
        name: name,
        icon: '📱',
        category: 'productivity',
        completions: {},
        streak: 0,
        alarmTime: '17:30',
        alarmEnabled: true,
        notes: [],
        duration: 21
      });
      saveState();
      renderAll();
      triggerConfetti();
      showToast('یادآور «آماده‌سازی پست هفتگی» به برنامه‌ات اضافه شد 🎉');
      addNotification('habit', 'یادآور محتوا فعال شد', 'هر هفته یک پست برای فضای مجازی آماده کن؛ برنامه و پرامت‌ها در ایجنت منتظرت است.', 'smartphone');
    }

    function deleteSocialPlan(planId) {
      state.agentSocialPlans = (state.agentSocialPlans || []).filter(x => x.id !== planId);
      saveState();
      renderSocialTab();
      showToast('برنامه محتوا حذف شد 🗑️');
    }

    function updateAgentBadge() {
      const badge = document.getElementById('agentBadge');
      if (!badge) return;
      const pending = (state.agentChat || []).some(m => m.role === 'agent' && m.plan && !m.applied);
      badge.style.display = pending ? 'flex' : 'none';
      badge.textContent = '۱';
    }

    // ================= AI AGENT: AUTO WEEKLY REPORT =================
    let weeklyReportBusy = false;

    function isoWeekKey(d) {
      const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
      const dayNum = date.getUTCDay() || 7;
      date.setUTCDate(date.getUTCDate() + 4 - dayNum);
      const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
      const weekNo = Math.ceil((((date - yearStart) / 86400000) + 1) / 7);
      return date.getUTCFullYear() + '-W' + weekNo;
    }

    function computeWeeklyStats() {
      const days = [];
      for (let i = 6; i >= 0; i--) {
        const d = new Date(); d.setDate(d.getDate() - i);
        days.push(d.toISOString().split('T')[0]);
      }
      const dayNames = ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه'];
      const perDay = days.map(ds => {
        const d = new Date(ds + 'T00:00:00');
        return { date: ds, dayFa: dayNames[d.getDay()], total: state.habits.length, done: state.habits.filter(h => h.completions[ds]).length };
      });
      const totalSlots = perDay.reduce((a, d) => a + d.total, 0);
      const totalDone = perDay.reduce((a, d) => a + d.done, 0);
      const rate7 = totalSlots > 0 ? Math.round((totalDone / totalSlots) * 100) : 0;
      const bestStreak = state.habits.length ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
      const moodScores = (state.moodLog || []).filter(m => days.includes(m.date)).map(m => m.score);
      const moodAvg = moodScores.length ? Math.round((moodScores.reduce((a, b) => a + b, 0) / moodScores.length) * 10) / 10 : null;
      const ranked = perDay.filter(d => d.total > 0).slice().sort((a, b) => (b.done / b.total) - (a.done / a.total));
      const habitRows = state.habits.map(h => ({ name: h.name, category: h.category, streak: h.streak || 0, done7: days.filter(ds => h.completions[ds]).length }));
      habitRows.sort((a, b) => b.done7 - a.done7);
      return {
        rate7: rate7,
        totalDone: totalDone,
        totalSlots: totalSlots,
        totalHabits: state.habits.length,
        bestStreak: bestStreak,
        moodAvg: moodAvg,
        moodCount: moodScores.length,
        bestDay: ranked.length ? ranked[0].dayFa : null,
        weakDay: ranked.length > 1 ? ranked[ranked.length - 1].dayFa : null,
        topHabits: habitRows.slice(0, 3),
        zeroHabits: habitRows.filter(h => h.done7 === 0).map(h => h.name).slice(0, 5),
        perDay: perDay
      };
    }

    function renderWeeklyReportTab() {
      const statsWrap = document.getElementById('agentWeekStats');
      const body = document.getElementById('agentWeeklyReportBody');
      if (!statsWrap || !body) return;
      const s = computeWeeklyStats();
      const cell = (val, label) => `<div class="agent-week-stat"><div class="agent-week-stat-val">${val}</div><div class="agent-week-stat-label">${label}</div></div>`;
      statsWrap.innerHTML =
        cell(toPersian(s.rate7) + '٪', 'تکمیل ۷ روز گذشته') +
        cell(toPersian(s.totalDone), 'کل تکمیل‌ها') +
        cell(toPersian(s.bestStreak), 'بهترین استریک') +
        cell(s.moodAvg !== null ? toPersian(String(s.moodAvg).replace('.', '٫')) : '—', 'میانگین حال') +
        cell(s.bestDay ? s.bestDay : '—', 'بهترین روز') +
        cell(s.topHabits.length ? escapeHtml(s.topHabits[0].name) : '—', 'عادت برتر هفته');

      const toggle = document.getElementById('agentAutoReportToggle');
      if (toggle) toggle.checked = !(state.settings && state.settings.autoWeeklyReport === false);

      const r = state.agentWeeklyReport;
      const wk = isoWeekKey(new Date());
      if (!r || !r.report) {
        body.innerHTML = '<div class="agent-insight-card"><div class="agent-bubble-text">هنوز گزارشی برای این هفته نداریم 📊\nروی «ساخت گزارش تازه این هفته» بزن تا هوش مصنوعی یک تحلیل کامل و صمیمی از هفته‌ات برایت بنویسد. از هفته بعد هم خودکار می‌سازم ✨</div></div>';
        return;
      }
      const isCurrent = r.weekKey === wk;
      const rep = r.report;
      const list = (items, icon) => (items || []).map(x => `<div class="agent-report-item">${icon} ${escapeHtml(x)}</div>`).join('');
      body.innerHTML = `
        <div class="agent-report-card">
          ${isCurrent ? '' : '<div class="agent-report-date">⚠️ این گزارش هفته قبل است — برای هفته جاری دوباره بساز</div>'}
          <div class="agent-report-headline">📈 ${escapeHtml(rep.headline || 'گزارش هفتگی تو')}</div>
          <div class="agent-report-summary">${escapeHtml(rep.summary || '')}</div>
          ${list(rep.highlights, '✅')}
          ${list(rep.issues, '⚠️')}
          ${list(rep.suggestions, '💡')}
          ${rep.focus ? `<div class="agent-report-focus">🎯 تمرکز هفته آینده: ${escapeHtml(rep.focus)}</div>` : ''}
          ${rep.motivation ? `<div class="agent-report-motivation">🔥 ${escapeHtml(rep.motivation)}</div>` : ''}
          <div class="agent-report-date">تاریخ تولید: ${new Date(r.generatedAt || Date.now()).toLocaleDateString('fa-IR', { weekday: 'long', day: 'numeric', month: 'long' })}</div>
        </div>`;
    }

    async function generateWeeklyReport(auto) {
      if (weeklyReportBusy) return;
      weeklyReportBusy = true;
      const btn = document.getElementById('agentReportBtn');
      const oldHtml = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">hourglass_top</span> در حال تحلیل هفته‌ات...'; }
      try {
        const res = await fetch('/api/agent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mode: 'weekly-report', stats: computeWeeklyStats(), context: getAgentContext() })
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        if (!data || !data.report) throw new Error('no report');
        state.agentWeeklyReport = { weekKey: isoWeekKey(new Date()), generatedAt: Date.now(), report: data.report };
        saveState();
        renderWeeklyReportTab();
        if (!auto) {
          playCrystalChime();
          showToast('گزارش هفتگی آماده شد! 📊');
        }
        addNotification('agent', 'گزارش هفتگی آماده شد', data.reply || 'تحلیل کامل هفته‌ات را در تب گزارش هفتگی ایجنت ببین.', 'monitoring');
      } catch (e) {
        if (!auto) showToast('ساخت گزارش ناموفق بود؛ دوباره تلاش کن 🙏');
      } finally {
        weeklyReportBusy = false;
        if (btn) { btn.disabled = false; btn.innerHTML = oldHtml; }
      }
    }

    function toggleAutoWeeklyReport(chk) {
      if (!state.settings) state.settings = {};
      state.settings.autoWeeklyReport = !!chk.checked;
      saveState();
      showToast(chk.checked ? 'گزارش هفتگی خودکار فعال شد ✅' : 'تولید خودکار گزارش خاموش شد');
    }

    function maybeAutoWeeklyReport() {
      renderWeeklyReportTab();
      if (state.settings && state.settings.autoWeeklyReport === false) return;
      if (weeklyReportBusy) return;
      const wk = isoWeekKey(new Date());
      if (state.agentWeeklyReport && state.agentWeeklyReport.weekKey === wk) return;
      setTimeout(() => generateWeeklyReport(true), 800);
    }

    function switchAgentTab(tabName) {
      // Update tabs
      document.querySelectorAll('.agent-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.tab === tabName) tab.classList.add('active');
      });
      
      // Update content
      document.querySelectorAll('.agent-tab-content').forEach(content => {
        content.classList.add('hidden');
      });
      document.getElementById('agentTab' + tabName.charAt(0).toUpperCase() + tabName.slice(1)).classList.remove('hidden');
      
      // Render tab-specific content
      if (tabName === 'chat') {
        renderAgentChat();
      } else if (tabName === 'report') {
        renderWeeklyReportTab();
      } else if (tabName === 'social') {
        renderSocialTab();
      }
    }

    function updateAgentGreeting() {
      const hour = new Date().getHours();
      let greeting = '';
      let subGreeting = '';
      
      if (hour >= 5 && hour < 12) {
        greeting = 'صبح بخیر! ️';
        subGreeting = 'امروز چه برنامه‌ای داری؟';
      } else if (hour >= 12 && hour < 17) {
        greeting = 'ظهر بخیر! 🌤️';
        subGreeting = 'نیمه روز را چطور پیش می‌بری؟';
      } else if (hour >= 17 && hour < 21) {
        greeting = 'عصر بخیر! 🌆';
        subGreeting = 'چه دستاوردهایی داشتی؟';
      } else {
        greeting = 'شب بخیر! 🌙';
        subGreeting = 'وقت مرور روز است';
      }
      
      document.getElementById('agentGreeting').textContent = greeting;
      document.getElementById('agentSubGreeting').textContent = subGreeting;
    }

    // ================= INIT =================
    document.addEventListener('DOMContentLoaded', () => {
      updateDate();
      setDailyQuote();
      renderMoodScorePicker();
      renderAll();
      requestNotificationPermission();
      startAlarmChecker();
      initMusicLibrary();
      startMusicScheduler();
      
      if (state.settings.batterySaver) {
        document.body.classList.add('battery-saver');
        updateBatterySaverToggle();
      }
      
      // Check for unread agent notifications
      const unreadAgent = state.notifications.filter(n => !n.read && n.type === 'agent').length;
      if (unreadAgent > 0) {
        const badge = document.getElementById('agentBadge');
        badge.style.display = 'flex';
        badge.textContent = toPersian(unreadAgent);
      } else {
        updateAgentBadge();
      }
    });

    function updateDate() {
      const options = { weekday: 'long', day: 'numeric', month: 'long' };
      const dateStr = new Date().toLocaleDateString('fa-IR', options);
      document.getElementById('headerDate').textContent = dateStr;
      document.getElementById('modalDate').textContent = dateStr;
    }

    function requestNotificationPermission() {
      if ('Notification' in window && Notification.permission === 'default') Notification.requestPermission();
    }

    function sendNotification(title, body) {
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body, tag: 'habits-tracker-alarm' });
      }
    }

    function startAlarmChecker() {
      setInterval(() => {
        const now = new Date();
        const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
        const todayStr = today();
        state.habits.forEach(habit => {
          if (habit.alarmEnabled && habit.alarmTime === currentTime && !habit.completions[todayStr]) {
            sendNotification('یادآوری عادت', `زمان انجام "${habit.name}" فرا رسیده است!`);
            addNotification('reminder', `یادآوری: ${habit.name}`, `زمان انجام "${habit.name}" فرا رسیده است!`, 'alarm');
          }
        });
      }, 60000);
    }

    // ================= RENDERING =================
    function renderAll() {
      renderStreakCalendar();
      renderHabits();
      renderBadges();
      renderTodayMoodPreview();
      updateBadgeCount();
      renderAlarmSettings();
      renderTrophyCase();
      renderNotebookPreview();
      renderNotifications();
    }

    // ================= STREAK CALENDAR =================
    let streakFilterCategory = 'all';

    function renderStreakCalendar() {
      const wrapper = document.getElementById('streakCalendarWrapper');
      if (!wrapper) return;
      
      const todayStr = today();
      const todayDate = new Date(todayStr);
      const numDays = 31;
      const dayNames = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'];
      
      let html = '<div class="streak-category-header">';
      html += '<div class="flex items-center gap-2">';
      html += '<div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">';
      html += '<span class="material-symbols-outlined text-[18px] text-primary">calendar_month</span>';
      html += '</div>';
      html += '<div>';
      html += '<div class="text-xs font-bold text-on-surface">۳۱ روز اخیر</div>';
      html += '<div class="text-[10px] text-on-surface-variant font-medium">مسیر پیوستگی تو</div>';
      html += '</div>';
      html += '</div>';
      html += '<div class="flex items-center gap-1">';
      html += '<span class="text-[10px] text-primary font-bold bg-on-primary-container px-2 py-1 rounded-full">';
      const totalStreak = state.habits.length > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
      html += ` ${toPersian(totalStreak)} روز`;
      html += '</span>';
      html += '</div>';
      html += '</div>';
      
      html += '<div class="streak-category-tabs">';
      const cats = [
        { id: 'all', label: 'همه', emoji: '📊' },
        { id: 'spiritual', label: 'معنوی', emoji: '🕊️' },
        { id: 'productivity', label: 'بهره‌وری', emoji: '⚡' },
        { id: 'self-care', label: 'مراقبت', emoji: '💖' },
        { id: 'family', label: 'خانواده', emoji: '👨‍👩👧' }
      ];
      cats.forEach(cat => {
        html += `<button class="streak-cat-tab ${streakFilterCategory === cat.id ? 'active' : ''}" onclick="setStreakFilter('${cat.id}')">${cat.emoji} ${cat.label}</button>`;
      });
      html += '</div>';
      
      html += '<div class="streak-days-grid">';
      
      for (let i = numDays - 1; i >= 0; i--) {
        const d = new Date(todayDate);
        d.setDate(todayDate.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        const isToday = dateStr === todayStr;
        const dayNumber = numDays - i;
        
        let allCompleted = false;
        let someCompleted = false;
        let relevantHabits = state.habits;
        
        if (streakFilterCategory !== 'all') {
          relevantHabits = state.habits.filter(h => h.category === streakFilterCategory);
        }
        
        if (relevantHabits.length > 0) {
          allCompleted = relevantHabits.every(h => h.completions[dateStr]);
          someCompleted = relevantHabits.some(h => h.completions[dateStr]);
        }
        
        let cellClass = 'streak-day-cell ';
        if (isToday) cellClass += 'today';
        else if (allCompleted) cellClass += 'completed';
        else if (someCompleted) cellClass += 'partial';
        else cellClass += 'future';
        
        let icon = '';
        if (allCompleted && !isToday) icon = '<span class="streak-day-icon">✓</span>';
        else if (isToday) icon = '<span class="streak-day-icon" style="color: #fbbf24;">●</span>';
        
        html += `
          <div class="${cellClass}" title="${dateStr}">
            ${icon}
            <span class="streak-day-label">روز</span>
            <span class="streak-day-number">${toPersian(dayNumber)}</span>
          </div>
        `;
      }
      
      html += '</div>';
      
      const completedDays = [];
      for (let i = numDays - 1; i >= 0; i--) {
        const d = new Date(todayDate);
        d.setDate(todayDate.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        let relevantHabits = state.habits;
        if (streakFilterCategory !== 'all') {
          relevantHabits = state.habits.filter(h => h.category === streakFilterCategory);
        }
        if (relevantHabits.length > 0 && relevantHabits.every(h => h.completions[dateStr])) {
          completedDays.push(dateStr);
        }
      }
      
      const currentStreak = calculateCurrentStreak();
      const longestStreak = calculateLongestStreak(numDays);
      const completionRate = numDays > 0 ? Math.round((completedDays.length / numDays) * 100) : 0;
      
      html += '<div class="streak-stats-row">';
      html += `
        <div class="streak-stat-card">
          <div class="streak-stat-value">${toPersian(currentStreak)}</div>
          <div class="streak-stat-label">استریک فعلی 🔥</div>
        </div>
        <div class="streak-stat-card">
          <div class="streak-stat-value" style="color: #fbbf24;">${toPersian(longestStreak)}</div>
          <div class="streak-stat-label">طولانی‌ترین ⭐</div>
        </div>
        <div class="streak-stat-card">
          <div class="streak-stat-value" style="color: #34d399;">${toPersian(completionRate)}٪</div>
          <div class="streak-stat-label">نرخ تکمیل 📊</div>
        </div>
      `;
      html += '</div>';
      
      wrapper.innerHTML = html;
      
      document.getElementById('streakTotalLabel').textContent = toPersian(totalStreak) + ' روز';
    }

    function setStreakFilter(cat) {
      streakFilterCategory = cat;
      renderStreakCalendar();
    }

    function calculateCurrentStreak() {
      const todayStr = today();
      const todayDate = new Date(todayStr);
      let streak = 0;
      
      for (let i = 0; i < 365; i++) {
        const d = new Date(todayDate);
        d.setDate(todayDate.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        let relevantHabits = state.habits;
        if (streakFilterCategory !== 'all') {
          relevantHabits = state.habits.filter(h => h.category === streakFilterCategory);
        }
        const allCompleted = relevantHabits.length > 0 && relevantHabits.every(h => h.completions[dateStr]);
        if (allCompleted) streak++;
        else if (i > 0) break;
      }
      
      return streak;
    }

    function calculateLongestStreak(numDays) {
      const todayDate = new Date(today());
      let longest = 0;
      let current = 0;
      
      for (let i = numDays - 1; i >= 0; i--) {
        const d = new Date(todayDate);
        d.setDate(todayDate.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        let relevantHabits = state.habits;
        if (streakFilterCategory !== 'all') {
          relevantHabits = state.habits.filter(h => h.category === streakFilterCategory);
        }
        const allCompleted = relevantHabits.length > 0 && relevantHabits.every(h => h.completions[dateStr]);
        
        if (allCompleted) {
          current++;
          if (current > longest) longest = current;
        } else {
          current = 0;
        }
      }
      
      return longest;
    }

    let currentFilter = 'all';
    function filterByCategory(cat) {
      currentFilter = cat;
      document.querySelectorAll('.category-filter-chip').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.cat === cat) btn.classList.add('active');
      });
      renderHabits();
    }

    function renderHabits() {
      const list = document.getElementById('habitsList');
      list.innerHTML = '';
      const todayStr = today();

      let filteredHabits = state.habits;
      if (currentFilter !== 'all') {
        filteredHabits = state.habits.filter(h => h.category === currentFilter);
      }

      if (filteredHabits.length === 0) {
        const emptyMsg = state.habits.length === 0 ? 'هنوز عادتی نساختی' : 'عادتی در این دسته نیست';
        const emptyCta = state.habits.length === 0 ? 'ساخت اولین عادت' : 'افزودن عادت جدید';
        list.innerHTML = `<div class="text-center py-8 text-on-surface-variant"><span class="float-icon text-4xl block mb-2 opacity-50">🏔️</span><p class="text-sm font-medium mb-3">${emptyMsg}</p><button onclick="openModal('addHabitModal')" class="px-5 py-3 rounded-2xl bg-gradient-to-br from-primary-container to-primary text-on-primary text-xs font-bold shadow-lg active:scale-95 transition-transform inline-flex items-center gap-1.5"><span class="material-symbols-outlined text-[17px]">add</span>${emptyCta}</button></div>`;
        return;
      }

      filteredHabits.forEach(habit => {
        const isCompleted = habit.completions[todayStr];
        const cat = categories[habit.category] || categories.productivity;
        
        const card = document.createElement('div');
        card.className = `habit-card bg-white rounded-2xl p-3.5 transition-all duration-300 shadow-sm border border-surface-container-highest ${isCompleted ? 'completed' : ''}`;
        card.dataset.id = habit.id;
        card.dataset.category = habit.category;
        
        let checkState = '';
        if (isCompleted) {
          checkState = `<div class="w-6 h-6 rounded-lg bg-primary text-on-primary flex items-center justify-center flex-shrink-0 shadow-sm"><span class="material-symbols-outlined text-[16px] font-bold">check</span></div>`;
        } else {
          checkState = `<div class="w-6 h-6 rounded-lg border-2 border-outline-variant bg-transparent flex items-center justify-center flex-shrink-0"></div>`;
        }
        
        card.innerHTML = `
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center shadow-sm flex-shrink-0" style="background: ${cat.color}20; color: ${cat.color};">
              <span class="material-symbols-outlined text-[16px]">${cat.icon}</span>
            </div>
            <div class="flex-1 flex flex-col text-right pr-1 cursor-pointer" onclick="toggleHabitExpand('${habit.id}')">
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="text-[13px] font-bold text-on-surface">${habit.name}</span>
                ${isCompleted ? `<span class="px-1.5 py-0.5 text-[9px] font-bold rounded-md bg-on-primary-container text-primary">تثبیت‌شده</span>` : ''}
                <span class="px-1.5 py-0.5 text-[9px] font-bold rounded-md" style="background: ${cat.color}20; color: ${cat.color};">${cat.emoji} ${cat.label}</span>
              </div>
              <div class="flex items-center gap-2 mt-1">
                ${habit.streak > 0 ? `<span class="text-[10px] text-tertiary font-bold flex items-center gap-0.5">🔥 ${toPersian(habit.streak)} روز</span>` : '<span class="text-[10px] text-on-surface-variant">شروع کن</span>'}
                <span class="text-[10px] text-on-surface-variant">⏰ ${habit.alarmTime || 'بدون آلارم'}</span>
              </div>
            </div>
            <button onclick="toggleHabit('${habit.id}', event)" class="flex-shrink-0">
              ${checkState}
            </button>
          </div>
        `;
        list.appendChild(card);
      });
    }

    function toggleHabitExpand(id) {
      const card = document.querySelector(`.habit-card[data-id="${id}"]`);
      if (card) card.classList.toggle('expanded');
    }

    function renderTodayMoodPreview() {
      const preview = document.getElementById('todayMoodPreview');
      const todayLog = state.moodLog.find(m => m.date === today());
      if (todayLog) {
        const emojis = ['😫', '😕', '😐', '🙂', '🤩'];
        preview.innerHTML = `
          <span class="text-[10px] text-on-surface-variant">امروز:</span>
          <div class="flex items-center gap-2">
            <span class="text-lg">${emojis[todayLog.score - 1]}</span>
            <span class="text-[10px] text-tertiary font-bold">انرژی: ${toPersian(todayLog.score)}/۵</span>
          </div>
        `;
      } else {
        preview.innerHTML = `<span class="text-[10px] text-on-surface-variant">وضعیت امروز:</span><span class="text-[10px] text-on-surface-variant">هنوز ثبت نشده</span>`;
      }
    }

    // ================= XP ANIMATION =================
    function triggerXpAnimation(habitCardElement) {
      if (state.settings.batterySaver) return;
      if (!habitCardElement) return;
      
      const mountainBtn = document.querySelector('[onclick="openModal(\'mountainModal\')"]');
      if (!mountainBtn) return;
      
      const startRect = habitCardElement.getBoundingClientRect();
      const endRect = mountainBtn.getBoundingClientRect();
      
      const startX = startRect.left + startRect.width / 2;
      const startY = startRect.top + startRect.height / 2;
      const endX = endRect.left + endRect.width / 2;
      const endY = endRect.top + endRect.height / 2;
      
      const dx = endX - startX;
      const dy = endY - startY;
      
      for (let i = 0; i < 3; i++) {
        setTimeout(() => {
          const coin = document.createElement('div');
          coin.className = 'xp-coin';
          coin.style.left = startX + 'px';
          coin.style.top = startY + 'px';
          coin.style.setProperty('--dx', dx + 'px');
          coin.style.setProperty('--dy', dy + 'px');
          document.body.appendChild(coin);
          setTimeout(() => coin.remove(), 1300);
        }, i * 150);
      }
      
      mountainBtn.style.transform = 'scale(1.2)';
      setTimeout(() => { mountainBtn.style.transform = ''; }, 300);
    }

    // ================= MY MOUNTAINS (REBUILT) =================
    function mountainStats() {
      const totalMountains = state.habits.length;
      const totalStreakDays = state.habits.reduce((s, h) => s + (h.streak || 0), 0);
      const conquered = state.habits.filter(h => Math.min(1, (h.streak || 0) / (h.duration || 21)) >= 0.95).length;
      const avgGrowth = totalMountains > 0
        ? state.habits.reduce((s, h) => s + Math.min(1, (h.streak || 0) / (h.duration || 21)), 0) / totalMountains
        : 0;
      return { totalMountains, totalStreakDays, conquered, avgGrowth, overallPercent: Math.round(avgGrowth * 100) };
    }

    function mountainStage(percent) {
      if (percent >= 95) return { emoji: '🏆', name: 'فتح قله', message: 'قله را فتح کردی! تو یک قهرمانی 🏆' };
      if (percent >= 75) return { emoji: '🏔️', name: 'نزدیک قله', message: 'به قله نزدیک شدی؛ آخرین تلاش را بکن' };
      if (percent >= 50) return { emoji: '🧗', name: 'نیمه‌راه', message: 'نیمه راه را طی کردی؛ قله نزدیک است' };
      if (percent >= 25) return { emoji: '⛺', name: 'پایگاه اول', message: 'پایگاه اول را فتح کردی؛ ادامه بده' };
      if (percent > 0) return { emoji: '🥾', name: 'شروع مسیر', message: 'قدم‌های اول را برداشتی؛ مسیر آغاز شده' };
      return { emoji: '🥾', name: 'آماده صعود', message: 'اولین قدم را بردار و مسیر صعود را آغاز کن' };
    }

    function mountainHeroSvg() {
      return `<svg class="mtn-hero-svg" viewBox="0 0 400 100" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0 100 L60 46 L105 72 L175 20 L245 76 L310 38 L400 100 Z" fill="rgba(255,255,255,0.13)"/>
        <path d="M140 100 L228 24 L316 100 Z" fill="rgba(255,255,255,0.20)"/>
        <path d="M210 40 L228 24 L246 40 L237 47 L228 40 L219 47 Z" fill="rgba(255,255,255,0.75)"/>
        <line x1="228" y1="24" x2="228" y2="10" stroke="rgba(255,255,255,0.85)" stroke-width="2"/>
        <path d="M228 10 L242 14 L228 19 Z" fill="#fbbf24"/>
        <circle cx="356" cy="20" r="11" fill="rgba(255,255,255,0.45)"/>
        <ellipse cx="70" cy="26" rx="26" ry="7" fill="rgba(255,255,255,0.30)"/>
        <ellipse cx="320" cy="52" rx="22" ry="6" fill="rgba(255,255,255,0.22)"/>
      </svg>`;
    }

    function renderMountains() {
      const container = document.getElementById('mountainModalBody');
      if (!container) return;
      const stats = mountainStats();
      const stage = mountainStage(stats.overallPercent);

      if (stats.totalMountains === 0) {
        container.innerHTML = `
          <div class="text-center py-10 px-4">
            <div class="text-6xl mb-4 opacity-60">🏔️</div>
            <h4 class="font-bold text-on-surface text-base mb-1.5">هنوز کوهی برای صعود نساخته‌ای</h4>
            <p class="text-xs text-on-surface-variant leading-relaxed mb-5">هر عادت یک کوه است؛ با هر روز استمرار، یک قدم به قله نزدیک‌تر می‌شوی.</p>
            <button onclick="closeAllModals(); setTimeout(() => openModal('addHabitModal'), 120);" class="agent-btn agent-btn-primary mx-auto px-8">
              <span class="material-symbols-outlined text-[18px]">add</span>
              ساخت اولین کوه
            </button>
          </div>
        `;
        return;
      }

      const cards = state.habits.map((habit, i) => {
        const duration = habit.duration || 21;
        const streak = habit.streak || 0;
        const growth = Math.min(1, streak / duration);
        const percent = Math.round(growth * 100);
        const isConquered = growth >= 0.95;
        const remaining = Math.max(0, duration - streak);
        const cat = categories[habit.category] || categories.productivity;
        const accent = isConquered ? '#f59e0b' : cat.color;
        return `
        <div class="mtn-card ${isConquered ? 'mtn-conquered' : ''}" style="animation-delay: ${i * 0.06}s" onclick="openMountainDetail('${habit.id}')">
          <div class="mtn-icon-wrap" style="background: ${cat.color}1c; border: 1.5px solid ${cat.color}59;">
            ${habit.icon || '🏔️'}
            ${isConquered ? '<span class="absolute -top-1.5 -left-1.5 text-[13px]">🏆</span>' : ''}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="text-[13px] font-bold text-on-surface truncate">${habit.name}</span>
                <span class="text-[8.5px] font-bold px-1.5 py-0.5 rounded-md flex-shrink-0 whitespace-nowrap" style="color: ${cat.color}; background: ${cat.color}1a;">${cat.emoji} ${cat.label}</span>
              </div>
              <span class="text-[13px] font-black flex-shrink-0" style="color: ${accent};">${toPersian(percent)}٪</span>
            </div>
            <div class="mtn-bar mb-1.5"><div class="mtn-bar-fill" style="width: ${percent}%; background: linear-gradient(90deg, ${cat.color}, ${isConquered ? '#fbbf24' : cat.color + 'b3'});"></div></div>
            <div class="flex items-center justify-between text-[9.5px] text-on-surface-variant">
              <span>🔥 ${toPersian(streak)} روز پیوستگی</span>
              <span class="font-bold" style="color: ${accent};">${isConquered ? '🏆 قله فتح شد' : toPersian(remaining) + ' روز تا قله'}</span>
            </div>
          </div>
        </div>`;
      }).join('');

      container.innerHTML = `
        <div class="mtn-hero">
          ${mountainHeroSvg()}
          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <span class="mtn-stage-chip">${stage.emoji} مرحله: ${stage.name}</span>
              <span class="text-[10px] font-bold opacity-80">کوهستان اراده</span>
            </div>
            <div class="flex items-end gap-1.5 mb-3">
              <span class="text-[44px] leading-none font-black">${toPersian(stats.overallPercent)}</span>
              <span class="text-base font-bold opacity-90 mb-1.5">٪ صعود کلی</span>
            </div>
            <div class="mtn-hero-bar mb-3"><div class="mtn-hero-fill" style="width: ${stats.overallPercent}%"></div></div>
            <p class="text-[11.5px] font-semibold opacity-95 leading-relaxed relative z-10">${stage.message} ✨</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center text-lg flex-shrink-0">🏔️</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.totalMountains)}</div>
              <div class="text-[9px] text-on-surface-variant mt-1">کوه فعال</div>
            </div>
          </div>
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-secondary/10 flex items-center justify-center text-lg flex-shrink-0">🔥</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.totalStreakDays)}</div>
              <div class="text-[9px] text-on-surface-variant mt-1">روزهای پیوستگی</div>
            </div>
          </div>
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-tertiary-fixed flex items-center justify-center text-lg flex-shrink-0">📈</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.overallPercent)}٪</div>
              <div class="text-[9px] text-on-surface-variant mt-1">میانگین رشد</div>
            </div>
          </div>
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center text-lg flex-shrink-0">🏆</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.conquered)}</div>
              <div class="text-[9px] text-on-surface-variant mt-1">قله‌های فتح‌شده</div>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between mt-1">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[18px] text-primary">hiking</span>
            <h4 class="font-bold text-on-surface text-sm">کوه‌های در حال صعود</h4>
          </div>
          <span class="text-[10px] text-on-surface-variant bg-surface-container-low px-2 py-1 rounded-lg border border-surface-container-highest">برای جزئیات بزن</span>
        </div>

        <div class="flex flex-col gap-2.5">
          ${cards}
        </div>
      `;
    }

    function openMountainDetail(habitId) {
      const habit = state.habits.find(h => h.id === habitId);
      if (!habit) return;
      const duration = habit.duration || 21;
      const streak = habit.streak || 0;
      const percent = Math.round(Math.min(1, streak / duration) * 100);
      if (percent >= 95) {
        showToast('🏆 ' + habit.name + ': قله فتح شد! ' + toPersian(streak) + ' روز استمرار');
      } else {
        showToast((habit.icon || '🏔️') + ' ' + habit.name + ': ' + toPersian(percent) + '٪ صعود — ' + toPersian(duration - streak) + ' روز تا قله');
      }
    }
    // ================= NOTEBOOK =================
    let selectedNoteTags = [];

    function toggleNoteTag(btn, tag) {
      if (selectedNoteTags.includes(tag)) {
        selectedNoteTags = selectedNoteTags.filter(t => t !== tag);
        btn.classList.remove('bg-primary', 'text-on-primary', 'border-primary');
        btn.classList.add('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      } else {
        selectedNoteTags.push(tag);
        btn.classList.add('bg-primary', 'text-on-primary', 'border-primary');
        btn.classList.remove('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      }
    }

    function saveNotebookEntry() {
      const text = document.getElementById('notebookText').value.trim();
      if (!text) { showToast('لطفاً متنی بنویس'); return; }
      
      state.notebookEntries.unshift({
        id: 'n' + Date.now(),
        date: today(),
        timestamp: new Date().toISOString(),
        text: text,
        tags: [...selectedNoteTags]
      });
      
      saveState();
      document.getElementById('notebookText').value = '';
      selectedNoteTags = [];
      document.querySelectorAll('#notebookTags button').forEach(btn => {
        btn.classList.remove('bg-primary', 'text-on-primary', 'border-primary');
        btn.classList.add('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      });
      renderNotebookHistory();
      renderNotebookPreview();
      showToast('یادداشت ذخیره شد 📔');
    }

    function renderNotebookHistory() {
      const container = document.getElementById('notebookHistory');
      if (!container) return;
      
      if (state.notebookEntries.length === 0) {
        container.innerHTML = '<div class="text-center text-on-surface-variant text-xs py-4">هنوز یادداشتی نداری</div>';
        return;
      }
      
      const tagEmojis = { thought: '💭', challenge: '🔥', achievement: '', gratitude: '🙏' };
      const tagLabels = { thought: 'فکر', challenge: 'چالش', achievement: 'دستاورد', gratitude: 'سپاس' };
      
      container.innerHTML = state.notebookEntries.slice(0, 10).map(entry => {
        const d = new Date(entry.timestamp);
        const dateStr = d.toLocaleDateString('fa-IR', { day: 'numeric', month: 'short' });
        const timeStr = d.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
        const tags = entry.tags.map(t => `<span class="text-[9px] px-1.5 py-0.5 rounded-full bg-primary/10 text-primary">${tagEmojis[t] || ''} ${tagLabels[t] || t}</span>`).join(' ');
        
        return `
          <div class="notebook-entry">
            <div class="flex items-center justify-between mb-1">
              <span class="text-[9px] text-on-surface-variant font-mono">${dateStr} • ${timeStr}</span>
              <button onclick="deleteNotebookEntry('${entry.id}')" class="text-on-surface-variant hover:text-error">
                <span class="material-symbols-outlined text-[14px]">delete</span>
              </button>
            </div>
            <p class="text-xs text-on-surface leading-relaxed mb-1">${escapeHtml(entry.text)}</p>
            ${tags ? `<div class="flex gap-1 flex-wrap">${tags}</div>` : ''}
          </div>
        `;
      }).join('');
    }

    function deleteNotebookEntry(id) {
      state.notebookEntries = state.notebookEntries.filter(e => e.id !== id);
      saveState();
      renderNotebookHistory();
      renderNotebookPreview();
    }

    function renderNotebookPreview() {
      const container = document.getElementById('notebookPreview');
      if (!container) return;
      
      if (state.notebookEntries.length === 0) {
        container.innerHTML = '<div class="text-center text-on-surface-variant text-xs py-4"><span class="material-symbols-outlined text-3xl opacity-30 block mb-2">auto_stories</span>هنوز یادداشتی ننوشتی. افکار، چالش‌ها و دستاوردهایت را ثبت کن.</div>';
        return;
      }
      
      const recent = state.notebookEntries.slice(0, 2);
      container.innerHTML = recent.map(entry => {
        const d = new Date(entry.timestamp);
        const dateStr = d.toLocaleDateString('fa-IR', { day: 'numeric', month: 'short' });
        return `
          <div class="bg-surface-container-low rounded-lg p-2 border-r-2 border-primary">
            <div class="text-[9px] text-on-surface-variant mb-1">${dateStr}</div>
            <p class="text-[11px] text-on-surface leading-relaxed truncate">${escapeHtml(entry.text)}</p>
          </div>
        `;
      }).join('');
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // ================= BADGES =================
    function renderBadges() {
      const grid = document.getElementById('badgesGrid');
      if (!grid) return;
      grid.innerHTML = '';

      const maxStreak = state.habits.length > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
      const totalCompletions = state.habits.reduce((acc, h) => acc + Object.keys(h.completions || {}).length, 0);
      const activeHabits = state.habits.length;
      const journalDays = Object.keys(state.journal).length;
      const moodDays = state.moodLog.length;

      const badges = [
        { id: 'streak_7', unlocked: maxStreak >= 7, name: 'شعله‌ی هفت‌روزه', desc: '۷ روز استریک پیوسته', icon: '🔥' },
        { id: 'streak_10', unlocked: maxStreak >= 10, name: 'استاد استقامت', desc: '۱۰ روز استریک', icon: '⚡' },
        { id: 'master', unlocked: totalCompletions >= 50, name: 'استاد عادت', desc: '۵۰ تکمیل موفق', icon: '🏆' },
        { id: 'morning', unlocked: activeHabits >= 3 && maxStreak >= 3, name: 'سحرخیز منظم', desc: 'نظم در ۳ عادت', icon: '☀️' },
        { id: 'journaler', unlocked: journalDays >= 5, name: 'خودآگاه', desc: '۵ روز ژورنال', icon: '' },
        { id: 'self-aware', unlocked: moodDays >= 7, name: 'آگاه به حال', desc: '۷ روز ثبت حال', icon: '💗' },
        { id: 'streak_30', unlocked: maxStreak >= 30, name: 'افسانه‌ی نظم', desc: '۳۰ روز استریک', icon: '👑' },
        { id: 'consistency', unlocked: totalCompletions >= 100, name: 'استمرار افسانه‌ای', desc: '۰۰ تکمیل', icon: '💎' }
      ];

      badges.forEach(badge => {
        const div = document.createElement('div');
        div.className = `rounded-2xl p-4 flex flex-col items-center text-center gap-2 transition-all ${badge.unlocked ? 'badge-unlocked' : 'badge-locked bg-white border border-surface-container-highest'}`;
        div.innerHTML = `
          <div class="w-14 h-14 rounded-full bg-surface-container-low flex items-center justify-center mb-1 text-3xl">${badge.icon}</div>
          <h4 class="font-bold text-sm text-on-surface">${badge.name}</h4>
          <p class="text-[10px] text-on-surface-variant">${badge.desc}</p>
          ${!badge.unlocked ? '<span class="text-[9px] bg-surface-container-low px-2 py-0.5 rounded-full text-on-surface-variant mt-1">قفل 🔒</span>' : '<span class="text-[9px] bg-primary/10 px-2 py-0.5 rounded-full text-primary mt-1">✓ کسب شد</span>'}
        `;
        grid.appendChild(div);
      });
    }

    function updateBadgeCount() {
      const maxStreak = state.habits.length > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
      const totalCompletions = state.habits.reduce((acc, h) => acc + Object.keys(h.completions || {}).length, 0);
      const activeHabits = state.habits.length;
      const journalDays = Object.keys(state.journal).length;
      const moodDays = state.moodLog.length;
      
      let count = 0;
      if (maxStreak >= 7) count++;
      if (maxStreak >= 10) count++;
      if (maxStreak >= 30) count++;
      if (totalCompletions >= 50) count++;
      if (totalCompletions >= 100) count++;
      if (activeHabits >= 3 && maxStreak >= 3) count++;
      if (journalDays >= 5) count++;
      if (moodDays >= 7) count++;
      
      const el = document.getElementById('badgeCount');
      if (el) el.textContent = toPersian(count);
    }

    function renderTrophyCase() {
      const container = document.getElementById('trophyCase');
      if (!container) return;
      
      const maxStreak = state.habits.length > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
      const totalCompletions = state.habits.reduce((acc, h) => acc + Object.keys(h.completions || {}).length, 0);
      
      const medals = [
        { id: 'medalDiamond', threshold: 100 },
        { id: 'medalPlatinum', threshold: 70 },
        { id: 'medalGold', threshold: 40 },
        { id: 'medalSilver', threshold: 21 },
        { id: 'medalBronze', threshold: 7 }
      ];
      
      medals.forEach(medal => {
        const el = document.getElementById(medal.id);
        if (maxStreak >= medal.threshold) {
          el.classList.remove('medal-locked');
        } else {
          el.classList.add('medal-locked');
        }
      });
      
      const challengesList = document.getElementById('challengesList');
      const challenges = [
        { id: 'weekly_streak', title: 'چالش هفتگی', desc: '۷ روز متوالی تمام عادت‌ها', progress: Math.min(100, (maxStreak / 7) * 100), reward: '🥉 مدال برنز', unlocked: maxStreak >= 7 },
        { id: 'monthly_streak', title: 'چالش ماهانه', desc: '۲۱ روز پیوستگی', progress: Math.min(100, (maxStreak / 21) * 100), reward: ' مدال نقره', unlocked: maxStreak >= 21 },
        { id: 'master_challenge', title: 'چالش استاد', desc: '۴۰ روز استریک طلایی', progress: Math.min(100, (maxStreak / 40) * 100), reward: '🥇 مدال طلا', unlocked: maxStreak >= 40 },
        { id: 'platinum_challenge', title: 'چالش پلاتین', desc: '۷۰ روز استقامت', progress: Math.min(100, (maxStreak / 70) * 100), reward: '🏅 مدال پلاتین', unlocked: maxStreak >= 70 },
        { id: 'diamond_challenge', title: 'چالش الماس', desc: '۱۰۰ روز افسانه‌ای', progress: Math.min(100, (maxStreak / 100) * 100), reward: '💎 مدال الماس', unlocked: maxStreak >= 100 },
        { id: 'completion_challenge', title: 'چالش تکمیل', desc: '۰ تکمیل عادت', progress: Math.min(100, (totalCompletions / 50) * 100), reward: '🏆 نشان استاد', unlocked: totalCompletions >= 50 },
        { id: 'mood_challenge', title: 'چالش خودآگاهی', desc: '۷ روز ثبت حال', progress: Math.min(100, (state.moodLog.length / 7) * 100), reward: '💗 نشان آگاهی', unlocked: state.moodLog.length >= 7 },
        { id: 'journal_challenge', title: 'چالش ژورنال', desc: '۵ روز نوشتن', progress: Math.min(100, (Object.keys(state.journal).length / 5) * 100), reward: '📔 نشان خودآگاه', unlocked: Object.keys(state.journal).length >= 5 }
      ];
      
      challengesList.innerHTML = challenges.map(ch => `
        <div class="challenge-card">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <span class="text-lg">${ch.unlocked ? '✅' : '🎯'}</span>
              <div>
                <div class="text-xs font-bold text-on-surface">${ch.title}</div>
                <div class="text-[9px] text-on-surface-variant">${ch.desc}</div>
              </div>
            </div>
            <span class="text-[9px] font-bold ${ch.unlocked ? 'text-primary' : 'text-on-surface-variant'} bg-white px-2 py-0.5 rounded-full">${ch.reward}</span>
          </div>
          <div class="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-primary to-secondary rounded-full transition-all" style="width: ${ch.progress}%"></div>
          </div>
          <div class="text-[9px] text-on-surface-variant mt-1 text-left">${toPersian(Math.round(ch.progress))}٪</div>
        </div>
      `).join('');

      let unlockedCount = 0;
      if (maxStreak >= 7) unlockedCount++;
      if (maxStreak >= 21) unlockedCount++;
      if (maxStreak >= 40) unlockedCount++;
      if (maxStreak >= 70) unlockedCount++;
      if (maxStreak >= 100) unlockedCount++;
      if (totalCompletions >= 50) unlockedCount++;
      if (state.moodLog.length >= 7) unlockedCount++;
      if (Object.keys(state.journal).length >= 5) unlockedCount++;
      
      document.getElementById('trophyCount').textContent = toPersian(unlockedCount) + ' کسب شده';
    }

    function renderAlarmSettings() {
      const container = document.getElementById('alarmSettingsList');
      if (!container) return;
      container.innerHTML = '';

      if (state.habits.length === 0) {
        container.innerHTML = '<div class="text-center text-on-surface-variant text-xs py-2">هنوز عادتی نداری</div>';
        return;
      }

      state.habits.forEach(habit => {
        const div = document.createElement('div');
        div.className = 'flex items-center justify-between gap-3 bg-surface-container-low rounded-xl p-3';
        div.innerHTML = `
          <div class="flex items-center gap-2 flex-1 min-w-0">
            <span class="text-lg">${habit.icon || '🏔️'}</span>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-on-surface truncate">${habit.name}</div>
              <input type="time" value="${habit.alarmTime || ''}" onchange="updateAlarmTime('${habit.id}', this.value)" class="text-[10px] text-on-surface-variant bg-transparent border-none focus:outline-none mt-0.5">
            </div>
          </div>
          <div class="w-11 h-6 bg-surface-container-highest rounded-full relative cursor-pointer transition-all ${habit.alarmEnabled ? 'bg-primary' : ''}" onclick="toggleAlarm('${habit.id}')">
            <div class="absolute top-0.5 ${habit.alarmEnabled ? 'left-0.5' : 'right-0.5'} w-5 h-5 bg-white rounded-full transition-all shadow-sm"></div>
          </div>
        `;
        container.appendChild(div);
      });
    }

    // ================= BATTERY SAVER =================
    function toggleBatterySaver() {
      state.settings.batterySaver = !state.settings.batterySaver;
      saveState();
      
      if (state.settings.batterySaver) {
        document.body.classList.add('battery-saver');
        showToast('🔋 حالت ذخیره باتری فعال شد');
      } else {
        document.body.classList.remove('battery-saver');
        showToast('✨ حالت عادی بازیابی شد');
      }
      
      updateBatterySaverToggle();
    }

    function updateBatterySaverToggle() {
      const toggle = document.getElementById('batterySaverToggle');
      if (!toggle) return;
      
      if (state.settings.batterySaver) {
        toggle.classList.add('bg-primary');
        toggle.classList.remove('bg-surface-container-highest');
        toggle.querySelector('div').style.right = 'auto';
        toggle.querySelector('div').style.left = '2px';
      } else {
        toggle.classList.remove('bg-primary');
        toggle.classList.add('bg-surface-container-highest');
        toggle.querySelector('div').style.left = 'auto';
        toggle.querySelector('div').style.right = '2px';
      }
    }

    // ================= MOOD CHART =================
    function renderMoodChart() {
      const container = document.getElementById('moodLineChartContainer');
      const labelsContainer = document.getElementById('moodChartLabels');
      const insightContainer = document.getElementById('moodInsight');
      if (!container) return;
      
      const last7Days = [];
      for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        last7Days.push(d.toISOString().split('T')[0]);
      }

      const moodData = last7Days.map(date => {
        const log = state.moodLog.find(m => m.date === date);
        return log ? log.score : null;
      });

      const habitsData = last7Days.map(date => {
        const total = state.habits.length;
        if (total === 0) return 0;
        const completed = state.habits.filter(h => h.completions[date]).length;
        return Math.round((completed / total) * 5);
      });

      const height = 180;
      const paddingX = 5;
      const paddingY = 15;
      
      let svgContent = `<svg width="100%" height="100%" viewBox="0 0 100 ${height}" preserveAspectRatio="none">`;
      
      for(let i = 1; i <= 5; i++) {
        const y = height - paddingY - ((i - 1) / 4) * (height - paddingY * 2);
        svgContent += `<line x1="${paddingX}" y1="${y}" x2="${100 - paddingX}" y2="${y}" stroke="rgba(24,20,69,0.05)" stroke-width="0.5" />`;
      }

      const moodPoints = [];
      moodData.forEach((score, i) => {
        if (score !== null) {
          const x = paddingX + (i / 6) * (100 - paddingX * 2);
          const y = height - paddingY - ((score - 1) / 4) * (height - paddingY * 2);
          moodPoints.push({ x, y });
        }
      });

      const habitPoints = [];
      habitsData.forEach((score, i) => {
        const x = paddingX + (i / 6) * (100 - paddingX * 2);
        const y = height - paddingY - ((score - 1) / 4) * (height - paddingY * 2);
        habitPoints.push({ x, y });
      });

      if (moodPoints.length > 1) {
        svgContent += `<polyline points="${moodPoints.map(p => `${p.x},${p.y}`).join(' ')}" fill="none" stroke="#843700" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />`;
        moodPoints.forEach(p => { svgContent += `<circle cx="${p.x}" cy="${p.y}" r="2.5" fill="#fcf8ff" stroke="#843700" stroke-width="1.5" />`; });
      }

      if (habitPoints.length > 1) {
        svgContent += `<polyline points="${habitPoints.map(p => `${p.x},${p.y}`).join(' ')}" fill="none" stroke="#630ed4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 1" />`;
        habitPoints.forEach(p => { svgContent += `<circle cx="${p.x}" cy="${p.y}" r="2" fill="#fcf8ff" stroke="#630ed4" stroke-width="1.5" />`; });
      }
      
      svgContent += `</svg>`;
      container.innerHTML = svgContent;

      const dayNames = ['ی', 'د', 'س', 'چ', 'پ', 'ج', 'ش'];
      labelsContainer.innerHTML = last7Days.map((d, i) => {
        const isToday = i === 6;
        return `<div class="flex-1 text-center ${isToday ? 'text-primary font-bold' : 'text-on-surface-variant'}">${dayNames[new Date(d).getDay()]}</div>`;
      }).join('');

      const validMoods = moodData.filter(m => m !== null);
      if (validMoods.length >= 3) {
        const avg = validMoods.reduce((a, b) => a + b, 0) / validMoods.length;
        insightContainer.innerHTML = `<div class="flex items-start gap-2"><span class="material-symbols-outlined text-[18px] text-tertiary">insights</span><div><p class="text-xs font-bold text-on-surface">میانگین انرژی</p><p class="text-[10px] text-on-surface-variant mt-1">${toPersian(avg.toFixed(1))} از  در ۷ روز گذشته</p></div></div>`;
      } else {
        insightContainer.innerHTML = `<div class="flex items-start gap-2"><span class="material-symbols-outlined text-[18px] text-on-surface-variant">info</span><div><p class="text-xs font-bold text-on-surface">داده کافی نیست</p><p class="text-[10px] text-on-surface-variant mt-1">حداقل  روز حال خود را ثبت کن.</p></div></div>`;
      }
    }

    // ================= ACTIONS =================
    function toggleHabit(id, event) {
      const habit = state.habits.find(h => h.id === id);
      if (!habit) return;
      
      const todayStr = today();
      if (!habit.completions) habit.completions = {};
      
      if (habit.completions[todayStr]) {
        delete habit.completions[todayStr];
        habit.streak = Math.max(0, (habit.streak || 0) - 1);
      } else {
        habit.completions[todayStr] = true;
        habit.streak = (habit.streak || 0) + 1;
        
        if (state.settings.sound) playCrystalChime();
        
        const card = event?.currentTarget?.closest('.habit-card');
        if (card) triggerXpAnimation(card);
        
        if (habit.streak === 7) {
          showToast('🥉 آفرین! مدال برنز کسب کردی!');
          addNotification('achievement', 'مدال برنز', '۷ روز استریک پیوسته!', 'emoji_events');
          triggerConfetti();
        } else if (habit.streak === 21) {
          showToast('🥈 تبریک! مدال نقره گرفتی!');
          addNotification('achievement', 'مدال نقره', '۲۱ روز استریک پیوسته!', 'emoji_events');
          triggerConfetti();
        } else if (habit.streak === 40) {
          showToast('🥇 فوق‌العاده! مدال طلا!');
          addNotification('achievement', 'مدال طلا', '۴۰ روز استریک پیوسته!', 'emoji_events');
          triggerConfetti();
        } else if (habit.streak === 70) {
          showToast('🏅 شگفت‌انگیز! مدال پلاتین!');
          addNotification('achievement', 'مدال پلاتین', '۷۰ روز استریک پیوسته!', 'emoji_events');
          triggerConfetti();
        } else if (habit.streak === 100) {
          showToast('💎 افسانه‌ای! مدال الماس!');
          addNotification('achievement', 'مدال الماس', '۱۰۰ روز استریک پیوسته!', 'emoji_events');
          triggerConfetti();
        } else {
          showToast('آفرین! یک قدم به قله نزدیک‌تر 🏔️');
        }
      }
      
      saveState();
      renderAll();
    }

    function selectCategory(btn, category) {
      document.querySelectorAll('.category-btn').forEach(el => {
        el.className = 'category-btn flex items-center justify-between p-3 rounded-2xl bg-surface-container-low text-on-surface border border-surface-container-highest font-semibold text-[12px] hover:bg-surface-container transition-all active:scale-95';
        const iconWrap = el.querySelector('.cat-icon-wrap');
        if (iconWrap) { 
          const cat = el.onclick.toString().match(/'([^']+)'/)?.[1];
          const catData = categories[cat];
          iconWrap.className = 'cat-icon-wrap w-7 h-7 rounded-xl flex items-center justify-center';
          iconWrap.style.background = catData ? catData.color + '20' : '';
          const iconSpan = iconWrap.querySelector('.cat-icon'); 
          if (iconSpan) { iconSpan.className = 'material-symbols-outlined cat-icon text-[18px]'; iconSpan.style.color = catData ? catData.color : ''; }
        }
        const check = el.querySelector('.cat-check');
        if (check) { check.textContent = 'radio_button_unchecked'; check.className = 'material-symbols-outlined cat-check text-[18px] text-outline-variant'; }
      });
      btn.className = 'category-btn selected flex items-center justify-between p-3 rounded-2xl bg-primary text-on-primary shadow-sm font-bold text-[12px] border-2 border-primary transition-all active:scale-95';
      const activeWrap = btn.querySelector('.cat-icon-wrap');
      if (activeWrap) { activeWrap.className = 'cat-icon-wrap w-7 h-7 rounded-xl bg-white/20 flex items-center justify-center'; const activeIcon = activeWrap.querySelector('.cat-icon'); if (activeIcon) activeIcon.className = 'material-symbols-outlined cat-icon text-[18px] text-on-primary'; }
      const activeCheck = btn.querySelector('.cat-check');
      if (activeCheck) { activeCheck.textContent = 'check_circle'; activeCheck.className = 'material-symbols-outlined cat-check text-[18px] text-on-primary'; }
      window.selectedCategory = category;
    }

    function selectDuration(btn, duration) {
      document.querySelectorAll('.duration-btn').forEach(el => {
        el.className = 'duration-btn bg-surface-container-low hover:bg-surface-container text-on-surface rounded-xl p-2 flex flex-col items-center justify-center text-center border border-surface-container-highest active:scale-95 transition-all';
        el.querySelectorAll('span').forEach(s => { s.classList.remove('text-on-primary'); s.classList.add('text-on-surface'); });
      });
      btn.className = 'duration-btn selected bg-primary text-on-primary rounded-xl p-2 flex flex-col items-center justify-center text-center shadow-md border-2 border-primary active:scale-95 transition-all';
      btn.querySelectorAll('span').forEach(s => { s.classList.remove('text-on-surface', 'text-on-surface-variant'); s.classList.add('text-on-primary'); });
      window.selectedDuration = duration;
      document.getElementById('progressLabel').textContent = `۰ از ${toPersian(duration)} روز`;
      
      const durationLabels = {
        7: '۷ روزه (شروع سریع)',
        21: '۲۱ روزه (تثبیت)',
        40: '۴۰ روزه (شکوه عهد)',
        70: '۷۰ روزه (استاد)',
        100: '۱۰۰ روزه (ریشه‌داری)'
      };
      document.getElementById('timelineSubtitle').textContent = `${durationLabels[duration] || '۲۱ روزه'} • مسیر صعود به قله`;
      
      renderMountainPreview(duration);
    }

    function selectHabitEmoji(btn, emoji) {
      window.selectedHabitEmoji = emoji;
      document.querySelectorAll('#habitEmojiPicker .habit-emoji-chip').forEach(el => el.classList.toggle('active', el === btn));
      const badge = document.getElementById('newHabitEmojiBadge');
      if (badge) badge.textContent = emoji;
    }
    function fillHabitSuggestion(name, emoji) {
      const input = document.getElementById('newHabitName');
      if (input) { input.value = name; input.focus(); }
      const chip = Array.from(document.querySelectorAll('#habitEmojiPicker .habit-emoji-chip')).find(el => el.textContent.trim() === emoji);
      if (chip) selectHabitEmoji(chip, emoji);
      else {
        window.selectedHabitEmoji = emoji;
        const badge = document.getElementById('newHabitEmojiBadge');
        if (badge) badge.textContent = emoji;
      }
      showToast(`«${name}» پر شد — دسته‌بندی و ساعت را تنظیم کن ✨`);
    }
    function toggleNewHabitAlarm() {
      window.newHabitAlarmEnabled = !window.newHabitAlarmEnabled;
      const wrap = document.getElementById('newHabitAlarmToggle');
      const knob = document.getElementById('newHabitAlarmKnob');
      if (!wrap || !knob) return;
      const on = window.newHabitAlarmEnabled !== false;
      wrap.style.background = on ? '#630ed4' : '#e3dfff';
      knob.classList.toggle('left-0.5', on);
      knob.classList.toggle('right-0.5', !on);
    }

    function renderMountainPreview(duration) {
      const svg = document.getElementById('mountainPreviewSvg');
      const labelsContainer = document.getElementById('mountainPreviewLabels');
      if (!svg || !labelsContainer) return;
      
      const width = 300;
      const height = 100;
      const peakX = width * 0.5;
      const peakY = height * 0.15;
      const baseLeftX = width * 0.05;
      const baseRightX = width * 0.95;
      const baseY = height * 0.85;
      
      const numPoints = 7;
      const pathPoints = [];
      for (let i = 0; i < numPoints; i++) {
        const t = i / (numPoints - 1);
        const x = baseLeftX + t * (peakX - baseLeftX);
        const baseY_at_t = baseY - t * (baseY - peakY);
        const zigzag = Math.sin(t * Math.PI * 2.5) * (width * 0.05);
        const y = baseY_at_t + zigzag;
        pathPoints.push({ x, y, t });
      }
      
      let svgContent = '';
      svgContent += `<path d="M 0 ${height * 0.7} L ${width * 0.2} ${height * 0.5} L ${width * 0.4} ${height * 0.6} L ${width * 0.6} ${height * 0.45} L ${width * 0.8} ${height * 0.55} L ${width} ${height * 0.5} L ${width} ${height} L 0 ${height} Z" fill="#94a3b8" opacity="0.2"/>`;
      svgContent += `<path d="M ${baseLeftX} ${baseY} L ${peakX - 10} ${peakY + 15} L ${peakX} ${peakY} L ${peakX + 10} ${peakY + 15} L ${baseRightX} ${baseY} Z" fill="#64748b" opacity="0.5"/>`;
      svgContent += `<path d="M ${peakX - 12} ${peakY + 15} L ${peakX} ${peakY} L ${peakX + 12} ${peakY + 15} L ${peakX + 6} ${peakY + 20} L ${peakX - 6} ${peakY + 20} Z" fill="white" opacity="0.8"/>`;
      
      const pathD = pathPoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
      svgContent += `<path d="${pathD}" fill="none" stroke="#630ed4" stroke-width="2" stroke-dasharray="4 3" class="mountain-preview-path" opacity="0.7"/>`;
      
      pathPoints.forEach((p, i) => {
        svgContent += `<circle cx="${p.x}" cy="${p.y}" r="4" fill="#dc2626" stroke="white" stroke-width="1.5" class="mountain-node" style="animation-delay: ${i * 0.1}s;"/>`;
      });
      
      svgContent += `<g class="flag-waver" style="transform-origin: ${peakX}px ${peakY}px;">`;
      svgContent += `<line x1="${peakX}" y1="${peakY}" x2="${peakX}" y2="${peakY - 15}" stroke="#1e293b" stroke-width="1.5"/>`;
      svgContent += `<path d="M ${peakX} ${peakY - 15} L ${peakX + 10} ${peakY - 12} L ${peakX} ${peakY - 9} Z" fill="#dc2626"/>`;
      svgContent += `</g>`;
      
      svg.innerHTML = svgContent;
      
      const durationMilestones = {
        7: ['روز  (قله)', 'روز ۵', 'روز ۳', 'روز ۱ (شروع)'],
        21: ['روز ۲۱ (قله)', 'روز ۱۴', 'روز ۷', 'روز ۱ (شروع)'],
        40: ['روز ۴۰ (قله)', 'روز ۲۷', 'روز ۱۴', 'روز ۱ (شروع)'],
        70: ['روز ۷۰ (قله)', 'روز ۴۷', 'روز ۳', 'روز ۱ (شروع)'],
        100: ['روز ۱۰۰ (قله)', 'روز ۶۷', 'روز ۳', 'روز ۱ (شروع)']
      };
      
      const milestones = durationMilestones[duration] || durationMilestones[21];
      labelsContainer.innerHTML = milestones.map((m, i) => 
        `<span class="${i === 0 ? 'text-primary font-extrabold' : ''}">${m}</span>`
      ).join('');
    }

    function saveNewHabit() {
      const name = document.getElementById('newHabitName').value.trim();
      if (!name) { showToast('لطفاً نام عادت را وارد کن'); return; }

      const catEmojis = { spiritual: '🕊️', productivity: '⚡', 'self-care': '💖', family: '👨‍👩‍👧' };
      const category = window.selectedCategory || 'productivity';
      const alarmInput = document.getElementById('newHabitAlarmTime');
      const alarmTime = (alarmInput && alarmInput.value) ? alarmInput.value : '08:00';
      const alarmEnabled = window.newHabitAlarmEnabled !== false;
      
      state.habits.push({
        id: 'h' + Date.now(),
        name,
        icon: window.selectedHabitEmoji || catEmojis[category] || '🏔️',
        category: category,
        completions: {},
        streak: 0,
        alarmTime: alarmTime,
        alarmEnabled: alarmEnabled,
        notes: [],
        duration: window.selectedDuration || 21
      });

      saveState();
      closeAllModals();
      document.getElementById('newHabitName').value = '';
      window.selectedCategory = null;
      window.selectedDuration = null;
      window.selectedHabitEmoji = null;
      window.newHabitAlarmEnabled = true;
      renderAll();
      showToast('عادت جدید با موفقیت اضافه شد 🏔️');
      addNotification('habit', 'عادت جدید', `عادت "${name}" با موفقیت ایجاد شد!`, 'add_circle');
    }

    function updateAlarmTime(habitId, time) {
      const habit = state.habits.find(h => h.id === habitId);
      if (habit) { habit.alarmTime = time; habit.alarmEnabled = !!time; saveState(); renderAll(); }
    }

    function toggleAlarm(habitId) {
      const habit = state.habits.find(h => h.id === habitId);
      if (habit) { habit.alarmEnabled = !habit.alarmEnabled; saveState(); renderAll(); showToast(habit.alarmEnabled ? 'آلارم فعال شد' : 'آلارم غیرفعال شد'); }
    }

    function saveMonthlyGoals() {
      closeAllModals();
      showToast('ذخیره شد');
    }

    let selectedMoodScore = 3;
    function renderMoodScorePicker() {
      const container = document.getElementById('moodScorePicker');
      if (!container) return;
      const emojis = ['😫', '😕', '😐', '🙂', '🤩'];
      container.innerHTML = '';
      emojis.forEach((emoji, index) => {
        const score = index + 1;
        const btn = document.createElement('button');
        btn.className = `flex-1 py-3 rounded-xl bg-surface-container-low border-2 transition-all active:scale-90 flex flex-col items-center gap-1 ${score === selectedMoodScore ? 'border-primary bg-on-primary-container scale-105' : 'border-surface-container-highest'}`;
        btn.innerHTML = `<span class="text-2xl">${emoji}</span>`;
        btn.onclick = () => { selectedMoodScore = score; renderMoodScorePicker(); };
        container.appendChild(btn);
      });
    }

    function saveMoodAndReflection() {
      const text = document.getElementById('reflectionText').value.trim();
      const todayStr = today();
      
      state.moodLog = state.moodLog.filter(m => m.date !== todayStr);
      state.moodLog.push({ date: todayStr, score: selectedMoodScore, reflection: text });

      saveState();
      closeAllModals();
      document.getElementById('reflectionText').value = '';
      showToast('حال و بازتاب امروز ذخیره شد ✍️');
      renderAll();
    }

    function saveJournal() {
      const text = document.getElementById('journalText').value.trim();
      if (!text) { showToast('لطفاً متنی بنویس'); return; }
      state.journal[today()] = { text, date: new Date().toISOString() };
      saveState();
      closeAllModals();
      document.getElementById('journalText').value = '';
      showToast('ژورنال ذخیره شد 📓');
      renderAll();
    }

    // ================= MUSIC LIBRARY =================
    const musicCategories = {
      calm:       { label: 'آرامش',  emoji: '🌙', grad: 'linear-gradient(135deg,#8b5cf6,#6d28d9)', stickers: ['🌙', '✨', '⭐'] },
      energy:     { label: 'انرژی',  emoji: '⚡', grad: 'linear-gradient(135deg,#fb923c,#f43f5e)', stickers: ['⚡', '🔥', '💥'] },
      focus:      { label: 'تمرکز',  emoji: '🎯', grad: 'linear-gradient(135deg,#38bdf8,#2563eb)', stickers: ['🎯', '💡', '📌'] },
      motivation: { label: 'انگیزه', emoji: '🚀', grad: 'linear-gradient(135deg,#34d399,#059669)', stickers: ['🚀', '🌟', '⭐'] }
    };
    const musicCollEmojiPool = ['🎧', '💜', '🎸', '🎹', '🌊', '☕', '🕌', '📚', '🌅', '🧘', '💪', '🌙'];
    const musicCollGradPool = [
      'linear-gradient(135deg,#a78bfa,#7c3aed)',
      'linear-gradient(135deg,#f472b6,#db2777)',
      'linear-gradient(135deg,#38bdf8,#2563eb)',
      'linear-gradient(135deg,#34d399,#059669)',
      'linear-gradient(135deg,#fb923c,#ea580c)',
      'linear-gradient(135deg,#facc15,#d97706)',
      'linear-gradient(135deg,#f87171,#dc2626)',
      'linear-gradient(135deg,#2dd4bf,#0d9488)'
    ];
    const musicStickerPool = ['✨', '🌟', '⭐', '💫', '🎶', '🎵', '🌈', '🦉', '🌸', '🍀', '🌙', '💛'];
    function allMusicCats() {
      const merged = {};
      Object.keys(musicCategories).forEach(k => { merged[k] = musicCategories[k]; });
      (state.musicCollections || []).forEach((c, i) => {
        merged[c.id] = {
          label: c.name,
          emoji: c.emoji,
          grad: c.grad,
          custom: true,
          stickers: [musicStickerPool[i % musicStickerPool.length], musicStickerPool[(i + 3) % musicStickerPool.length], musicStickerPool[(i + 7) % musicStickerPool.length]]
        };
      });
      return merged;
    }
    const musicEmojiPool = ['🎵', '🎧', '🎹', '🎸', '🥁', '🎤', '🎺', '🎻'];
    let currentMusicTab = 'all';
    let musicDB = null;
    let musicQueue = [];
    let currentMusicModalId = null;
    window.__musicModalDraft = { category: 'calm', schedule: { enabled: false, time: '07:00' } };
    window.__musicModalId = null;

    const musicAudio = new Audio();
    musicAudio.preload = 'auto';
    let currentPlayingId = null;
    let currentMusicUrl = null;

    // ---- Music IndexedDB (audio blobs) ----
    function openMusicDB() {
      return new Promise(resolve => {
        if (musicDB) return resolve(musicDB);
        if (!('indexedDB' in window)) return resolve(null);
        try {
          const req = indexedDB.open('musicLibraryDB', 1);
          req.onupgradeneeded = e => { try { e.target.result.createObjectStore('tracks', { keyPath: 'id' }); } catch (err) {} };
          req.onsuccess = e => { musicDB = e.target.result; resolve(musicDB); };
          req.onerror = () => resolve(null);
          setTimeout(() => resolve(musicDB), 2000);
        } catch (e) { resolve(null); }
      });
    }
    function idbMusicPut(rec) {
      return openMusicDB().then(db => new Promise(resolve => {
        if (!db) return resolve(false);
        try {
          const tx = db.transaction('tracks', 'readwrite');
          tx.objectStore('tracks').put(rec);
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) { resolve(false); }
      }));
    }
    function idbMusicGet(id) {
      return openMusicDB().then(db => new Promise(resolve => {
        if (!db) return resolve(null);
        try {
          const rq = db.transaction('tracks', 'readonly').objectStore('tracks').get(id);
          rq.onsuccess = () => resolve(rq.result || null);
          rq.onerror = () => resolve(null);
        } catch (e) { resolve(null); }
      }));
    }
    function idbMusicDelete(id) {
      return openMusicDB().then(db => new Promise(resolve => {
        if (!db) return resolve(false);
        try {
          const tx = db.transaction('tracks', 'readwrite');
          tx.objectStore('tracks').delete(id);
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) { resolve(false); }
      }));
    }

    // ---- Upload flow ----
    function musicCleanName(fileName) {
      return String(fileName || '').replace(/\.[^.]+$/, '').replace(/[_\-]+/g, ' ').replace(/\s+/g, ' ').trim() || 'موزیک بدون نام';
    }
    function musicIsAudio(f) {
      if (!f) return false;
      if ((f.type || '').startsWith('audio/')) return true;
      return /\.(mp3|wav|ogg|oga|m4a|aac|flac|opus|weba|webm|wma|aiff?)$/i.test(f.name || '');
    }
    function musicGetDuration(blob) {
      return new Promise(resolve => {
        let url;
        try { url = URL.createObjectURL(blob); } catch (e) { return resolve(0); }
        const a = new Audio();
        a.preload = 'metadata';
        let settled = false;
        const done = d => { if (settled) return; settled = true; try { URL.revokeObjectURL(url); } catch (e) {} resolve(d); };
        a.onloadedmetadata = () => { const d = a.duration; done(isFinite(d) && d > 0 ? Math.round(d) : 0); };
        a.onerror = () => done(0);
        setTimeout(() => done(0), 5000);
        a.src = url;
      });
    }
    async function handleMusicUpload(fileList) {
      const files = Array.from(fileList || []).filter(musicIsAudio);
      if (!files.length) { showToast('فایل صوتی معتبری انتخاب نشد 🎵'); return; }
      const input = document.getElementById('musicFileInput');
      if (input) input.value = '';
      let added = 0;
      for (const f of files) {
        if (f.size > 80 * 1024 * 1024) { showToast(`«${musicCleanName(f.name)}» بزرگ‌تر از ۸۰ مگابایت است`); continue; }
        const id = 'mu' + Date.now() + Math.floor(Math.random() * 1000);
        const ok = await idbMusicPut({ id: id, blob: f, addedAt: new Date().toISOString() });
        if (!ok) { showToast('حافظه مرورگر اجازه ذخیره نداد 😕'); continue; }
        const duration = await musicGetDuration(f);
        state.musicTracks.push({
          id: id,
          name: musicCleanName(f.name),
          category: 'calm',
          emoji: musicEmojiPool[state.musicTracks.length % musicEmojiPool.length],
          favorite: false,
          schedule: { enabled: false, time: '07:00', lastPlayedOn: null },
          playCount: 0,
          durationSec: duration,
          sizeBytes: f.size,
          addedAt: today()
        });
        added++;
      }
      if (added > 0) {
        saveState();
        renderMusicLibrary();
        triggerConfetti();
        showToast(`${toPersian(added)} موزیک به کتابخانه اضافه شد 🎉`);
      }
    }

    // ---- Music page open/close / tabs ----
    function openMusicPage() {
      document.getElementById('musicPage').classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      renderMusicLibrary();
    }
    function closeMusicPage() {
      document.getElementById('musicPage').classList.add('hidden');
      document.body.style.overflow = '';
    }
    function setMusicTab(tabId) { currentMusicTab = tabId; renderMusicLibrary(); }
    function musicFilteredTracks() {
      if (currentMusicTab === 'fav') return state.musicTracks.filter(t => t.favorite);
      if (currentMusicTab === 'sched') return state.musicTracks.filter(t => t.schedule && t.schedule.enabled);
      if (allMusicCats()[currentMusicTab]) return state.musicTracks.filter(t => t.category === currentMusicTab);
      return state.musicTracks.slice();
    }
    function updateMusicCountLabel() {
      const el = document.getElementById('musicCountLabel');
      if (el) el.textContent = `${toPersian(state.musicTracks.length)} موزیک در قفسه`;
    }

    // ---- Rendering ----
    function renderMusicTabs() {
      const wrap = document.getElementById('musicTabs');
      if (!wrap) return;
      const cats = allMusicCats();
      const countIn = k => state.musicTracks.filter(t => t.category === k).length;
      const tabs = [
        { id: 'all', label: `همه (${toPersian(state.musicTracks.length)})` },
        ...Object.keys(cats).map(k => ({ id: k, label: `${cats[k].emoji} ${cats[k].label} (${toPersian(countIn(k))})` })),
        { id: 'fav', label: `⭐ محبوب‌ها (${toPersian(state.musicTracks.filter(t => t.favorite).length)})` },
        { id: 'sched', label: `⏰ زمان‌بندی (${toPersian(state.musicTracks.filter(t => t.schedule && t.schedule.enabled).length)})` }
      ];
      wrap.innerHTML = tabs.map(t => `<button class="music-tab ${currentMusicTab === t.id ? 'active' : ''}" onclick="setMusicTab('${t.id}')">${t.label}</button>`).join('') +
        `<button class="music-tab music-tab-new" onclick="openNewMusicCollectionModal()"><span class="font-extrabold">+</span> کالکشن جدید</button>`;
    }
    function playMusicCollection(k) {
      const ids = state.musicTracks.filter(t => t.category === k).map(t => t.id);
      if (!ids.length) { showToast('این کالکشن خالی است — اول موزیک اضافه کن 🎵'); return; }
      musicQueue = ids;
      playMusicTrack(ids[0]);
    }
    function renderMusicCollections() {
      const wrap = document.getElementById('musicCollections');
      if (!wrap) return;
      const cats = allMusicCats();
      const keys = Object.keys(cats).filter(k => state.musicTracks.some(t => t.category === k) || (cats[k].custom && currentMusicTab === 'all'));
      if (currentMusicTab !== 'all' || keys.length === 0) { wrap.innerHTML = ''; wrap.classList.add('hidden'); return; }
      wrap.classList.remove('hidden');
      const heights = [84, 66, 76, 58, 80, 70];
      const tilts = [-2.5, 1.6, -1, 2.4, -1.8, 1.2];
      wrap.innerHTML = keys.map(k => {
        const c = cats[k];
        const tracks = state.musicTracks.filter(t => t.category === k);
        const shown = tracks.slice(0, 6);
        const extra = tracks.length - shown.length;
        const spines = shown.map((t, i) =>
          `<div class="music-book-spine" style="height:${heights[i % heights.length]}px; transform:rotate(${tilts[i % tilts.length]}deg); background: linear-gradient(180deg, rgba(255,255,255,0.3), rgba(255,255,255,0.04) 55%), ${c.grad}; z-index:${10 - i};">${t.emoji}</div>`
        ).join('');
        const moreSpine = extra > 0 ? `<div class="music-book-spine" style="height:${heights[(shown.length) % heights.length]}px; transform:rotate(1.5deg); background: rgba(255,255,255,0.3); backdrop-filter: blur(3px);"><span class="text-[11px] font-extrabold text-white">+${toPersian(extra)}</span></div>` : '';
        const shelfInner = tracks.length ? spines + moreSpine :
          `<div class="music-book-spine" style="height:64px; border:1.5px dashed rgba(255,255,255,0.65); background:rgba(255,255,255,0.14); font-size:14px;">🎶</div><div class="music-book-spine" style="height:52px; border:1.5px dashed rgba(255,255,255,0.5); background:rgba(255,255,255,0.1); font-size:13px;">➕</div>`;
        const deleteBtn = c.custom ? `<button onclick="event.stopPropagation(); deleteMusicCollection('${k}')" class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/35 text-white flex items-center justify-center transition-all active:scale-90" title="حذف کالکشن"><span class="material-symbols-outlined text-[15px]">delete</span></button>` : '';
        return `
          <div class="music-collection-card relative overflow-hidden rounded-[28px] p-4 pt-4 cursor-pointer active:scale-[0.98] transition-transform" style="background: ${c.grad};" onclick="setMusicTab('${k}')">
            <span class="absolute top-3 left-3 text-xl opacity-85 select-none">${c.stickers[0]}</span>
            <span class="absolute top-9 left-14 text-sm opacity-60 select-none">${c.stickers[1]}</span>
            <span class="absolute bottom-16 left-4 text-base opacity-70 select-none">${c.stickers[2]}</span>
            <div class="flex items-start justify-between mb-3 relative z-10">
              <div>
                <h4 class="text-white font-extrabold text-[16px] drop-shadow-sm">${c.emoji} ${c.label}</h4>
                <span class="text-white/80 text-[10.5px] font-bold">${toPersian(tracks.length)} موزیک ${c.custom ? '· کالکشن من' : ''}</span>
              </div>
              <div class="flex items-center gap-1.5">
                ${deleteBtn}
                <button onclick="event.stopPropagation(); playMusicCollection('${k}')" class="w-9 h-9 rounded-full bg-white/25 hover:bg-white/40 text-white flex items-center justify-center transition-all active:scale-90 shadow-md" title="پخش کالکشن">
                  <span class="material-symbols-outlined text-[18px]">play_arrow</span>
                </button>
              </div>
            </div>
            <div class="music-shelf-row relative z-10">${shelfInner}</div>
            <div class="music-shelf-line relative z-10"></div>
          </div>`;
      }).join('');
    }
    function musicFmtDur(sec) {
      const s = Math.max(0, Math.round(sec || 0));
      return toPersian(Math.floor(s / 60)) + ':' + toPersian(String(s % 60).padStart(2, '0'));
    }
    function renderMusicList() {
      const list = document.getElementById('musicTrackList');
      if (!list) return;
      const tracks = musicFilteredTracks();
      if (state.musicTracks.length === 0) {
        list.innerHTML = `
          <div class="music-empty-card p-8 text-center">
            <div class="w-16 h-16 mx-auto rounded-3xl bg-gradient-to-br from-emerald-400 to-green-600 flex items-center justify-center text-white text-3xl shadow-lg shadow-emerald-500/25 mb-3">🎵</div>
            <p class="text-sm font-bold text-on-surface mb-1">هنوز موزیکی آپلود نکردی!</p>
            <p class="text-[11px] text-on-surface-variant leading-relaxed mb-4">با دکمه سبز پایین صفحه اولین موزیکت را آپلود کن،<br>بعد ساعت پخش خودکارش را تنظیم کن یا با میکروفون اسمش را بگو.</p>
            <button onclick="document.getElementById('musicFileInput').click()" class="px-5 py-2.5 rounded-2xl bg-primary text-white text-xs font-bold shadow-lg shadow-primary/25 active:scale-95 transition-transform">آپلود اولین موزیک</button>
          </div>`;
        return;
      }
      if (tracks.length === 0) {
        const msgs = { fav: 'هنوز موزیکی را محبوب نکردی ⭐', sched: 'هنوز پخش خودکاری تنظیم نشده ⏰' };
        list.innerHTML = `<div class="text-center py-8 text-on-surface-variant text-xs font-medium">${msgs[currentMusicTab] || 'موزیکی در این کالکشن نیست 🎵'}</div>`;
        return;
      }
      list.innerHTML = tracks.map(t => {
        const cat = allMusicCats()[t.category] || musicCategories.calm;
        const isPlaying = currentPlayingId === t.id && !musicAudio.paused;
        const sched = t.schedule && t.schedule.enabled;
        return `
          <div class="music-track-row bg-white rounded-2xl p-3 border border-surface-container-highest shadow-sm flex items-center gap-3" data-mid="${t.id}">
            <button onclick="playMusicTrackFromList('${t.id}')" class="w-[52px] h-[52px] rounded-2xl flex items-center justify-center text-2xl flex-shrink-0 relative active:scale-90 transition-transform text-white shadow-md" style="background: ${cat.grad};">
              ${t.emoji}
              ${isPlaying ? '<span class="absolute inset-0 rounded-2xl bg-black/30 flex items-end justify-center pb-1.5 text-white"><span class="music-eq"><span></span><span></span><span></span></span></span>' : ''}
            </button>
            <div class="flex-1 min-w-0 cursor-pointer" onclick="openMusicTrackModal('${t.id}')">
              <div class="flex items-center gap-1.5">
                <span class="text-[13px] font-bold text-on-surface truncate">${t.name}</span>
                ${t.favorite ? '<span class="text-[11px]">⭐</span>' : ''}
              </div>
              <div class="flex items-center gap-2 mt-1 flex-wrap">
                <span class="text-[10px] text-on-surface-variant">${musicFmtDur(t.durationSec)}</span>
                <span class="px-1.5 py-0.5 text-[9px] font-bold rounded-md text-white" style="background: ${cat.grad};">${cat.label}</span>
                ${sched ? `<span class="text-[10px] font-bold text-emerald-600 flex items-center gap-1"><span class="music-sched-dot"></span>${toPersian(t.schedule.time)}</span>` : ''}
              </div>
            </div>
            <button onclick="${isPlaying ? 'toggleMusicPlay()' : `playMusicTrackFromList('${t.id}')`}" class="music-play-btn" style="background: ${isPlaying ? '#181445' : 'linear-gradient(135deg,#630ed4,#8b5cf6)'};">
              <span class="material-symbols-outlined text-[20px]">${isPlaying ? 'pause' : 'play_arrow'}</span>
            </button>
          </div>`;
      }).join('');
    }
    function renderMusicLibrary() {
      if (!document.getElementById('musicPage')) return;
      renderMusicTabs();
      renderMusicCollections();
      renderMusicList();
      updateMusicCountLabel();
    }

    // ---- Play engine & mini player ----
    function playMusicTrackFromList(id) {
      musicQueue = musicFilteredTracks().map(t => t.id);
      playMusicTrack(id);
    }
    async function playMusicTrack(id) {
      const meta = state.musicTracks.find(t => t.id === id);
      if (!meta) return;
      const rec = await idbMusicGet(id);
      if (!rec || !rec.blob) { showToast('فایل این موزیک پیدا نشد — دوباره آپلودش کن 🎵'); return; }
      try { if (currentMusicUrl) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
      currentMusicUrl = URL.createObjectURL(rec.blob);
      musicAudio.src = currentMusicUrl;
      try {
        await musicAudio.play();
      } catch (e) {
        currentPlayingId = id;
        renderMusicList();
        updateMusicMiniPlayer();
        showToast('پخش خودکار مرورگر اجازه نداد — دکمه پخش را بزن ▶️');
        return;
      }
      currentPlayingId = id;
      if (!musicQueue.includes(id)) musicQueue = [id];
      meta.playCount = (meta.playCount || 0) + 1;
      saveState();
      renderMusicList();
      updateMusicMiniPlayer();
    }
    function toggleMusicPlay() {
      if (!currentPlayingId) {
        const first = musicFilteredTracks()[0] || state.musicTracks[0];
        if (first) playMusicTrackFromList(first.id);
        return;
      }
      if (musicAudio.paused) { musicAudio.play().catch(() => {}); } else { musicAudio.pause(); }
    }
    function stopMusic() {
      musicAudio.pause();
      try { musicAudio.currentTime = 0; } catch (e) {}
      currentPlayingId = null;
      musicQueue = [];
      try { if (currentMusicUrl) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
      currentMusicUrl = null;
      const player = document.getElementById('musicMiniPlayer');
      if (player) player.classList.add('hidden');
      const fw = document.getElementById('musicFabWrap');
      if (fw) fw.style.bottom = '';
      renderMusicList();
    }
    function seekMusic(ev) {
      if (!musicAudio.duration || !isFinite(musicAudio.duration)) return;
      const bar = ev.currentTarget;
      if (!bar) return;
      const rect = bar.getBoundingClientRect();
      let ratio = (rect.right - ev.clientX) / rect.width;
      ratio = Math.min(1, Math.max(0, ratio));
      musicAudio.currentTime = ratio * musicAudio.duration;
    }
    musicAudio.addEventListener('play', () => { updateMusicMiniPlayer(); renderMusicList(); });
    musicAudio.addEventListener('pause', () => { updateMusicMiniPlayer(); renderMusicList(); });
    musicAudio.addEventListener('timeupdate', () => {
      if (!musicAudio.duration || !isFinite(musicAudio.duration)) return;
      const bar = document.getElementById('musicMiniProgress');
      const lbl = document.getElementById('musicMiniTime');
      if (bar) bar.style.width = Math.min(100, (musicAudio.currentTime / musicAudio.duration) * 100) + '%';
      if (lbl) lbl.textContent = `${musicFmtDur(musicAudio.currentTime)} / ${musicFmtDur(musicAudio.duration)}`;
    });
    musicAudio.addEventListener('ended', () => {
      const idx = musicQueue.indexOf(currentPlayingId);
      const next = musicQueue[idx + 1];
      if (next) { playMusicTrack(next); }
      else {
        currentPlayingId = null;
        renderMusicList();
        const player = document.getElementById('musicMiniPlayer');
        if (player) player.classList.add('hidden');
        const fw = document.getElementById('musicFabWrap');
        if (fw) fw.style.bottom = '';
      }
    });
    function updateMusicMiniPlayer() {
      const meta = state.musicTracks.find(t => t.id === currentPlayingId);
      const player = document.getElementById('musicMiniPlayer');
      if (!meta || !player) return;
      player.classList.remove('hidden');
      const fw = document.getElementById('musicFabWrap');
      if (fw) fw.style.bottom = '128px';
      const cat = allMusicCats()[meta.category] || musicCategories.calm;
      const cover = document.getElementById('musicMiniCover');
      if (cover) { cover.textContent = meta.emoji; cover.style.background = cat.grad; }
      const name = document.getElementById('musicMiniName');
      if (name) name.textContent = meta.name;
      const icon = document.getElementById('musicMiniPlayIcon');
      if (icon) icon.textContent = musicAudio.paused ? 'play_arrow' : 'pause';
      const lbl = document.getElementById('musicMiniTime');
      if (lbl) lbl.textContent = `${musicFmtDur(musicAudio.currentTime || 0)} / ${musicFmtDur(meta.durationSec || musicAudio.duration || 0)}`;
    }
    // Unlock audio on first user gesture (helps scheduled autoplay)
    (function musicUnlockAudio() {
      const unlock = () => {
        document.removeEventListener('pointerdown', unlock);
        if (musicAudio.src) return;
        try {
          musicAudio.muted = true;
          const p = musicAudio.play();
          if (p && p.then) p.then(() => { musicAudio.pause(); musicAudio.currentTime = 0; musicAudio.muted = false; }).catch(() => { musicAudio.muted = false; });
        } catch (e) { musicAudio.muted = false; }
      };
      document.addEventListener('pointerdown', unlock);
    })();

    // ---- Auto-play scheduler (پخش خودکار روزانه) ----
    function startMusicScheduler() {
      setInterval(() => {
        const now = new Date();
        const ct = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
        const d = today();
        let changed = false;
        state.musicTracks.forEach(t => {
          if (t.schedule && t.schedule.enabled && t.schedule.time === ct && t.schedule.lastPlayedOn !== d) {
            t.schedule.lastPlayedOn = d;
            changed = true;
            addNotification('music', `🎵 پخش خودکار: ${t.name}`, `ساعت ${t.schedule.time} فرا رسید و موزیک شروع شد!`, 'music_note');
            sendNotification('پخش خودکار موزیک', `«${t.name}» سر ساعت ${t.schedule.time} شروع شد`);
            showToast(`🎵 پخش خودکار: ${t.name}`);
            playMusicTrack(t.id);
          }
        });
        if (changed) saveState();
      }, 15000);
    }

    // ---- Track modal (edit / schedule / favorite / delete) ----
    function renderMusicScheduleToggle(on) {
      return `<div class="w-11 h-6 rounded-full relative cursor-pointer transition-all ${on ? 'bg-primary' : 'bg-surface-container-highest'}" onclick="toggleMusicModalSchedule()"><div class="absolute top-0.5 ${on ? 'left-0.5' : 'right-0.5'} w-5 h-5 bg-white rounded-full transition-all shadow-sm"></div></div>`;
    }
    function toggleMusicModalSchedule() {
      window.__musicModalDraft.schedule.enabled = !window.__musicModalDraft.schedule.enabled;
      const wrap = document.getElementById('musicModalScheduleToggle');
      if (wrap) wrap.innerHTML = renderMusicScheduleToggle(window.__musicModalDraft.schedule.enabled);
    }
    function openMusicTrackModal(id) {
      const t = state.musicTracks.find(x => x.id === id);
      if (!t) return;
      currentMusicModalId = id;
      window.__musicModalId = id;
      window.__musicModalDraft = { category: t.category, schedule: { enabled: t.schedule.enabled, time: t.schedule.time } };
      const cat = allMusicCats()[t.category] || musicCategories.calm;
      document.getElementById('musicModalName').textContent = t.name;
      const cover = document.getElementById('musicModalCover');
      cover.textContent = t.emoji;
      cover.style.background = cat.grad;
      document.getElementById('musicModalMeta').textContent = `${musicFmtDur(t.durationSec)} · ${toPersian(t.playCount || 0)} بار پخش شده`;
      document.getElementById('musicModalTime').value = t.schedule.time || '07:00';
      document.getElementById('musicModalCategories').innerHTML = Object.keys(allMusicCats()).map(k => {
        const cc = allMusicCats()[k];
        return `<button class="music-modal-cat ${k === t.category ? 'active' : ''}" style="${k === t.category ? 'background:' + cc.grad + ';' : ''}" onclick="selectMusicModalCategory('${k}')">${cc.emoji} ${cc.label}</button>`;
      }).join('');
      document.getElementById('musicModalScheduleToggle').innerHTML = renderMusicScheduleToggle(t.schedule.enabled);
      openModal('musicTrackModal');
    }
    function selectMusicModalCategory(k) {
      window.__musicModalDraft.category = k;
      const cats = allMusicCats();
      document.querySelectorAll('#musicModalCategories .music-modal-cat').forEach(el => {
        const key = el.getAttribute('onclick').match(/'([^']+)'/)[1];
        const active = key === k;
        el.classList.toggle('active', active);
        el.style.background = active ? cats[key].grad : '';
      });
    }
    function saveMusicTrackModal() {
      const t = state.musicTracks.find(x => x.id === currentMusicModalId);
      if (!t) { closeAllModals(); return; }
      t.category = window.__musicModalDraft.category || t.category;
      t.schedule.enabled = !!window.__musicModalDraft.schedule.enabled;
      t.schedule.time = document.getElementById('musicModalTime').value || t.schedule.time || '07:00';
      if (t.schedule.enabled) t.schedule.lastPlayedOn = null;
      saveState();
      closeAllModals();
      renderMusicLibrary();
      showToast(t.schedule.enabled ? `⏰ «${t.name}» هر روز ساعت ${toPersian(t.schedule.time)} پخش می‌شود` : 'تغییرات ذخیره شد ✅');
    }
    function deleteMusicTrack(id) {
      const t = state.musicTracks.find(x => x.id === id);
      if (!t) return;
      if (!confirm(`«${t.name}» از کتابخانه حذف شود؟`)) return;
      if (currentPlayingId === id) stopMusic();
      idbMusicDelete(id);
      state.musicTracks = state.musicTracks.filter(x => x.id !== id);
      saveState();
      closeAllModals();
      renderMusicLibrary();
      showToast('موزیک از کتابخانه حذف شد 🗑️');
    }
    function toggleMusicFavorite(id) {
      const t = state.musicTracks.find(x => x.id === id);
      if (!t) return;
      t.favorite = !t.favorite;
      saveState();
      renderMusicLibrary();
      showToast(t.favorite ? `«${t.name}» به محبوب‌ها اضافه شد ⭐` : 'از محبوب‌ها حذف شد');
    }

    // ---- Custom collections (+ کالکشن جدید) ----
    window.__musicCollDraft = { emoji: '🎧', grad: musicCollGradPool[0] };
    function openNewMusicCollectionModal() {
      window.__musicCollDraft = { emoji: musicCollEmojiPool[(state.musicCollections || []).length % musicCollEmojiPool.length], grad: musicCollGradPool[(state.musicCollections || []).length % musicCollGradPool.length] };
      const nameInput = document.getElementById('musicCollName');
      if (nameInput) nameInput.value = '';
      renderMusicCollPickers();
      openModal('musicNewCollectionModal');
      setTimeout(() => { if (nameInput) nameInput.focus(); }, 250);
    }
    function renderMusicCollPickers() {
      const emojiRow = document.getElementById('musicCollEmojiRow');
      if (emojiRow) emojiRow.innerHTML = musicCollEmojiPool.map(e =>
        `<button class="music-emoji-pick ${e === window.__musicCollDraft.emoji ? 'active' : ''}" onclick="pickMusicCollEmoji(this, '${e}')">${e}</button>`).join('');
      const gradRow = document.getElementById('musicCollGradRow');
      if (gradRow) gradRow.innerHTML = musicCollGradPool.map(g =>
        `<button class="music-grad-pick ${g === window.__musicCollDraft.grad ? 'active' : ''}" style="background:${g};" onclick="pickMusicCollGrad(this, '${g}')"></button>`).join('');
    }
    function pickMusicCollEmoji(btn, e) {
      window.__musicCollDraft.emoji = e;
      document.querySelectorAll('#musicCollEmojiRow .music-emoji-pick').forEach(el => el.classList.toggle('active', el === btn));
    }
    function pickMusicCollGrad(btn, g) {
      window.__musicCollDraft.grad = g;
      document.querySelectorAll('#musicCollGradRow .music-grad-pick').forEach(el => el.classList.toggle('active', el === btn));
    }
    function createMusicCollection() {
      const name = (document.getElementById('musicCollName') || {}).value?.trim();
      if (!name) { showToast('یک نام برای کالکشن بنویس ✍️'); return; }
      if ((state.musicCollections || []).length >= 10) { showToast('حداکثر ۱۰ کالکشن سفارشی می‌توانی بسازی 😅'); return; }
      const id = 'mc' + Date.now();
      state.musicCollections.push({ id, name, emoji: window.__musicCollDraft.emoji, grad: window.__musicCollDraft.grad });
      saveState();
      closeAllModals();
      currentMusicTab = id;
      renderMusicLibrary();
      triggerConfetti();
      showToast(`قفسه «${name}» ساخته شد 🎉 موزیک‌ها را با مودال تری‌نقطه به آن منتقل کن`);
      addNotification('music', '📚 کالکشن جدید', `کالکشن «${name}» به کتابخانه موزیک اضافه شد.`, 'library_music');
    }
    function deleteMusicCollection(id) {
      const c = (state.musicCollections || []).find(x => x.id === id);
      if (!c) return;
      const count = state.musicTracks.filter(t => t.category === id).length;
      if (count > 0) { showToast(`اول ${toPersian(count)} موزیک داخلش را جابه‌جا یا حذف کن 🙏`); return; }
      if (!confirm(`کالکشن «${c.name}» حذف شود؟`)) return;
      state.musicCollections = state.musicCollections.filter(x => x.id !== id);
      if (currentMusicTab === id) currentMusicTab = 'all';
      saveState();
      renderMusicLibrary();
      showToast('کالکشن حذف شد 🗑️');
    }

    // ---- Voice command (اسم موزیک را بگو تا پخش شود) ----
    let musicRecognition = null;
    let isMusicListening = false;
    const musicVoiceFillers = ['پخش', 'پخشش', 'کن', 'بزن', 'بذار', 'بزار', 'اجرا', 'بگو', 'شروع', 'موزیک', 'موسیقی', 'اهنگ', 'ترانه', 'لطفا', 'خواهش', 'برام', 'برای', 'من', 'رو', 'را', 'یه', 'یک', 'از', 'ده'];
    function musicNormalize(s) {
      return String(s || '')
        .toLowerCase()
        .replace(/[\u200c\u200f\u200e\u064b-\u0652]/g, '')
        .replace(/[يى]/g, 'ی')
        .replace(/ك/g, 'ک')
        .replace(/[أإآ]/g, 'ا')
        .replace(/ة/g, 'ه')
        .replace(/ؤ/g, 'و')
        .replace(/ئ/g, 'ی')
        .replace(/[^0-9a-z\u0600-\u06FF\s]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    }
    function musicExtractQuery(text) {
      let q = musicNormalize(text);
      musicVoiceFillers.forEach(w => { q = q.replace(new RegExp('(^|\\s)' + w + '(?=\\s|$)', 'g'), ' '); });
      return q.replace(/\s+/g, ' ').trim();
    }
    function musicFindTrack(query) {
      const q = musicNormalize(query);
      if (!q) return null;
      let best = null, bestScore = 0;
      state.musicTracks.forEach(t => {
        const n = musicNormalize(t.name);
        if (!n) return;
        let score = 0;
        if (n === q) score = 100;
        else if (n.includes(q) || q.includes(n)) score = 80 - Math.abs(n.length - q.length);
        else {
          const qt = q.split(' ').filter(w => w.length > 1);
          const nt = n.split(' ');
          let hits = 0;
          qt.forEach(w => { if (nt.some(x => x.includes(w) || w.includes(x))) hits++; });
          if (qt.length > 0 && hits / qt.length >= 0.5) score = 40 + hits * 5;
        }
        if (score > bestScore) { bestScore = score; best = t; }
      });
      return bestScore >= 25 ? best : null;
    }
    function setMusicListeningUI(on) {
      isMusicListening = on;
      ['musicMicFab', 'musicVoiceBtnHeader'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.toggle('music-mic-listening', on);
      });
    }
    function startMusicVoice() {
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SR) { showToast('مرورگر شما از دستیار صوتی پشتیبانی نمی‌کند 😕'); return; }
      if (isMusicListening) { try { musicRecognition.stop(); } catch (e) {} return; }
      try {
        musicRecognition = new SR();
        musicRecognition.lang = 'fa-IR';
        musicRecognition.interimResults = false;
        musicRecognition.maxAlternatives = 3;
        musicRecognition.onstart = () => { setMusicListeningUI(true); showToast('در حال گوش دادن... اسم موزیک را بگو 🎤'); };
        musicRecognition.onend = () => setMusicListeningUI(false);
        musicRecognition.onerror = ev => { setMusicListeningUI(false); if (ev.error === 'not-allowed') showToast('دسترسی میکروفون داده نشد 🎙️'); };
        musicRecognition.onresult = e => {
          const alts = e.results[0];
          let handled = false;
          for (let i = 0; i < Math.min(alts.length, 3); i++) {
            const text = alts[i].transcript;
            const n = musicNormalize(text);
            if (n === 'بعدی' || n.includes('بعدی')) {
              const idx = musicQueue.indexOf(currentPlayingId);
              const nextId = musicQueue[idx + 1] || musicQueue[0];
              if (nextId) { showToast('⏭️ موزیک بعدی'); playMusicTrack(nextId); handled = true; break; }
            }
            const track = musicFindTrack(musicExtractQuery(text));
            if (track) { showToast(`🎵 در حال پخش: ${track.name}`); playMusicTrack(track.id); handled = true; break; }
          }
          if (!handled) showToast('موزیکی با این اسم در کتابخانه نبود 🤔');
        };
        musicRecognition.start();
      } catch (e) { setMusicListeningUI(false); showToast('دستیار صوتی در دسترس نیست 😕'); }
    }

    // ---- Music init ----
    async function initMusicLibrary() {
      await openMusicDB();
      renderMusicLibrary();
    }

    // ================= MODAL HELPERS =================
    function openModal(id) {
      document.getElementById('modalBackdrop').classList.remove('hidden');
      document.getElementById('modalBackdrop').classList.add('visible');
      document.getElementById(id).classList.remove('hidden');
      document.getElementById(id).classList.add('visible');
      document.body.style.overflow = 'hidden';
      
      if (id === 'moodChartModal') renderMoodChart();
      if (id === 'badgesModal') renderBadges();
      if (id === 'profileModal') {
        renderAlarmSettings();
        renderTrophyCase();
        updateBatterySaverToggle();
        renderNotebookPreview();
      }
      if (id === 'notebookModal') {
        renderNotebookHistory();
      }
      if (id === 'moodModal') {
        const todayLog = state.moodLog.find(m => m.date === today());
        if (todayLog) {
          selectedMoodScore = todayLog.score;
          document.getElementById('reflectionText').value = todayLog.reflection || '';
          renderMoodScorePicker();
        }
      }
      if (id === 'mountainModal') {
        renderMountains();
      }
      if (id === 'notificationsModal') {
        renderNotifications();
      }
      if (id === 'agentModal') {
        updateAgentGreeting();
        switchAgentTab('chat');
        seedAgentWelcome();
        maybeAutoWeeklyReport();
        // Clear badge
        const badge = document.getElementById('agentBadge');
        badge.style.display = 'none';
        // Mark agent notifications as read
        state.notifications.forEach(n => {
          if (n.type === 'agent') n.read = true;
        });
        saveState();
      }
      if (id === 'addHabitModal') {
        window.selectedCategory = 'spiritual';
        window.selectedDuration = 21;
        window.selectedHabitEmoji = '🏔️';
        window.newHabitAlarmEnabled = true;
        const nameInput = document.getElementById('newHabitName');
        if (nameInput) nameInput.value = '';
        const emojiBadge = document.getElementById('newHabitEmojiBadge');
        if (emojiBadge) emojiBadge.textContent = '🏔️';
        const alarmTimeInput = document.getElementById('newHabitAlarmTime');
        if (alarmTimeInput) alarmTimeInput.value = '08:00';
        const alarmToggle = document.getElementById('newHabitAlarmToggle');
        if (alarmToggle) alarmToggle.style.background = '#630ed4';
        const alarmKnob = document.getElementById('newHabitAlarmKnob');
        if (alarmKnob) { alarmKnob.classList.add('left-0.5'); alarmKnob.classList.remove('right-0.5'); }
        document.querySelectorAll('#habitEmojiPicker .habit-emoji-chip').forEach((el, i) => el.classList.toggle('active', i === 0));
        setTimeout(() => {
          const spiritualBtn = document.getElementById('catBtnSpiritual');
          if (spiritualBtn) selectCategory(spiritualBtn, 'spiritual');
          const duration21Btn = document.querySelector('[onclick*="selectDuration(this, 21)"]');
          if (duration21Btn) selectDuration(duration21Btn, 21);
          renderMountainPreview(21);
        }, 100);
      }
    }

    function closeAllModals() {
      document.getElementById('modalBackdrop').classList.add('hidden');
      document.getElementById('modalBackdrop').classList.remove('visible');
      document.querySelectorAll('.modal-sheet').forEach(m => {
        m.classList.add('hidden');
        m.classList.remove('visible');
      });
      document.body.style.overflow = '';
    }

    function showToast(message) {
      const toast = document.getElementById('toast');
      document.getElementById('toastText').textContent = message;
      toast.style.transform = 'translate(-50%, 0)';
      setTimeout(() => { toast.style.transform = 'translate(-50%, -150%)'; }, 3000);
    }

    function triggerConfetti() {
      if (state.settings.batterySaver) return;
      const colors = ['#630ed4', '#843700', '#ec4899', '#6b38d4', '#fbbf24', '#06b6d4'];
      for (let i = 0; i < 40; i++) {
        const conf = document.createElement('div');
        conf.style.position = 'fixed';
        conf.style.width = (4 + Math.random() * 4) + 'px';
        conf.style.height = conf.style.width;
        conf.style.background = colors[Math.floor(Math.random() * colors.length)];
        conf.style.left = '50%';
        conf.style.top = '40%';
        conf.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        conf.style.pointerEvents = 'none';
        conf.style.zIndex = '100';
        conf.style.setProperty('--x', (Math.random() - 0.5) * 400 + 'px');
        conf.style.animation = `confettiFall ${1 + Math.random()}s ease-out forwards`;
        document.body.appendChild(conf);
        setTimeout(() => conf.remove(), 2000);
      }
    }

    let timerInterval = null, timerSeconds = 25 * 60, totalTimerSeconds = 25 * 60, isTimerRunning = false;
    function updateTimerDisplay() {
      const m = Math.floor(timerSeconds / 60), s = timerSeconds % 60;
      document.getElementById('timerDisplay').textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
      const circumference = 2 * Math.PI * 45;
      document.getElementById('timerRing').style.strokeDashoffset = circumference - (1 - (timerSeconds / totalTimerSeconds)) * circumference;
    }
    function toggleTimer() {
      const icon = document.getElementById('timerIcon');
      if (isTimerRunning) {
        clearInterval(timerInterval); isTimerRunning = false;
        icon.textContent = 'play_arrow';
        document.getElementById('timerStatus').textContent = 'متوقف شده';
      } else {
        isTimerRunning = true;
        icon.textContent = 'pause';
        document.getElementById('timerStatus').textContent = 'در حال تمرکز...';
        timerInterval = setInterval(() => {
          timerSeconds--; updateTimerDisplay();
          if (timerSeconds <= 0) {
            clearInterval(timerInterval); isTimerRunning = false;
            icon.textContent = 'play_arrow';
            document.getElementById('timerStatus').textContent = 'تمام شد! 🎉';
            showToast('زمان تمرکز به پایان رسید. آفرین!');
            triggerConfetti(); resetTimer();
          }
        }, 1000);
      }
    }
    function resetTimer() {
      clearInterval(timerInterval); isTimerRunning = false; timerSeconds = totalTimerSeconds;
      updateTimerDisplay();
      document.getElementById('timerIcon').textContent = 'play_arrow';
      document.getElementById('timerStatus').textContent = 'آماده شروع';
    }

    function toPersian(num) { return String(num).replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]); }

    const style = document.createElement('style');
    style.textContent = `
      @keyframes confettiFall { 0% { transform: translate(0, 0) rotate(0deg); opacity: 1; } 100% { transform: translate(var(--x), 300px) rotate(720deg); opacity: 0; } }
      @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
      @keyframes animated-line { from { stroke-dashoffset: 1000; } to { stroke-dashoffset: 0; } }
      @keyframes animated-area { from { opacity: 0; } to { opacity: 0.2; } }
      @keyframes chart-point-animated { from { opacity: 0; transform: scale(0); } to { opacity: 1; transform: scale(1); } }
      .animated-line { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: animated-line 2s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
      .animated-area { opacity: 0; animation: animated-area 1s ease-out 1.5s forwards; }
      .chart-point-animated { opacity: 0; transform-origin: center; animation: chart-point-animated 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
    `;
    document.head.appendChild(style);

    // ================= FLOATING ICONS: STAGGER ENGINE =================
    (function () {
      const rand = () => (-(Math.random() * 3.6)).toFixed(2) + 's';
      const SEL = '.material-symbols-outlined, .float-icon, .streak-day-icon, .habit-emoji-chip, .music-emoji-pick';
      const mark = (el) => { if (!el.style.animationDelay) el.style.animationDelay = rand(); };
      const scan = (node) => {
        if (!node || node.nodeType !== 1) return;
        if (node.matches && node.matches(SEL)) mark(node);
        if (node.querySelectorAll) node.querySelectorAll(SEL).forEach(mark);
      };
      scan(document.body);
      new MutationObserver((muts) => {
        for (const m of muts) for (const n of m.addedNodes) scan(n);
      }).observe(document.body, { childList: true, subtree: true });
    })();

    // ================= AGENT BOOT SCREEN (CINEMATIC ROBOT — LONG CUT) =================
    function buildBootLines() {
      const habits = state.habits || [];
      const n = habits.length;
      const doneToday = habits.filter(h => h.completions && h.completions[today()]).length;
      return [
        'اتصال به شبکه عصبی مرکزی...',
        `شناسایی ${toPersian(n)} عادت فعال...`,
        'بارگذاری مغز دیجیتال...',
        'کالیبره‌سازی مدل زبانی فارسی...',
        'همگام‌سازی حافظه بلندمدت...',
        'تحلیل الگوهای رفتاری تو...',
        'فعال‌سازی ماژول انگیزش...',
        `بررسی پیشرفت امروز: ${toPersian(doneToday)} از ${toPersian(n)} عادت`,
        'آخرین بررسی امنیتی...'
      ];
    }
    let bootTimers = [];
    let bootActive = false;

    function playBootSound() {
      try {
        if (state.settings.batterySaver) return;
        initAudio();
        const now = audioCtx.currentTime;
        // 1) deep reactor swell
        const sub = audioCtx.createOscillator();
        const subG = audioCtx.createGain();
        sub.type = 'sine';
        sub.frequency.setValueAtTime(55, now);
        sub.frequency.exponentialRampToValueAtTime(190, now + 1.6);
        subG.gain.setValueAtTime(0.0001, now);
        subG.gain.exponentialRampToValueAtTime(0.05, now + 0.5);
        subG.gain.exponentialRampToValueAtTime(0.0001, now + 1.9);
        sub.connect(subG); subG.connect(masterGain);
        sub.start(now); sub.stop(now + 2);
        // 2) rising power sweep
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(760, now + 1.1);
        g.gain.setValueAtTime(0.0001, now);
        g.gain.exponentialRampToValueAtTime(0.045, now + 0.35);
        g.gain.exponentialRampToValueAtTime(0.0001, now + 1.35);
        osc.connect(g); g.connect(masterGain);
        osc.start(now); osc.stop(now + 1.4);
        // 3) ready beeps
        [880, 1174.66].forEach((f, i) => {
          const o2 = audioCtx.createOscillator();
          const g2 = audioCtx.createGain();
          o2.type = 'triangle'; o2.frequency.value = f;
          const t0 = now + 2.35 + i * 0.16;
          g2.gain.setValueAtTime(0.0001, t0);
          g2.gain.exponentialRampToValueAtTime(0.05, t0 + 0.02);
          g2.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.24);
          o2.connect(g2); g2.connect(masterGain);
          o2.start(t0); o2.stop(t0 + 0.27);
        });
        // 4) final rising arpeggio
        [659.25, 830.61, 987.77].forEach((f, i) => {
          const o3 = audioCtx.createOscillator();
          const g3 = audioCtx.createGain();
          o3.type = 'triangle'; o3.frequency.value = f;
          const t0 = now + 4.75 + i * 0.12;
          g3.gain.setValueAtTime(0.0001, t0);
          g3.gain.exponentialRampToValueAtTime(0.045, t0 + 0.02);
          g3.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.3);
          o3.connect(g3); g3.connect(masterGain);
          o3.start(t0); o3.stop(t0 + 0.33);
        });
        // 5) ready chord on flash
        [523.25, 659.25].forEach((f) => {
          const o4 = audioCtx.createOscillator();
          const g4 = audioCtx.createGain();
          o4.type = 'sine'; o4.frequency.value = f;
          const t0 = now + 5.32;
          g4.gain.setValueAtTime(0.0001, t0);
          g4.gain.exponentialRampToValueAtTime(0.05, t0 + 0.04);
          g4.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.85);
          o4.connect(g4); g4.connect(masterGain);
          o4.start(t0); o4.stop(t0 + 0.9);
        });
      } catch (e) { /* silent */ }
    }

    function stopBootTimers() { bootTimers.forEach(clearTimeout); bootTimers = []; }

    function openAgentModalMaterialized() {
      const m = document.getElementById('agentModal');
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (m && !reduce) {
        m.classList.remove('agent-materialize');
        void m.offsetWidth;
        m.classList.add('agent-materialize');
        setTimeout(() => m.classList.remove('agent-materialize'), 1300);
      }
      openModal('agentModal');
    }

    function hideBootScreen(thenOpen) {
      stopBootTimers();
      const scr = document.getElementById('agentBootScreen');
      if (!scr || !scr.classList.contains('active')) {
        if (thenOpen) openAgentModalMaterialized();
        return;
      }
      scr.classList.remove('active');
      scr.classList.remove('boot-final');
      bootActive = false;
      if (thenOpen) setTimeout(() => openAgentModalMaterialized(), 140);
    }

    function openAgentWithBoot() {
      if (bootActive) return;
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        openModal('agentModal');
        return;
      }
      bootActive = true;
      playBootSound();
      const scr = document.getElementById('agentBootScreen');
      const term = document.getElementById('bootTerminal');
      const fill = document.getElementById('bootProgressFill');
      const pct = document.getElementById('bootPercent');
      const flash = document.getElementById('bootFlash');
      const status = document.getElementById('bootStatus');
      const eq = document.getElementById('bootEq');
      term.innerHTML = '';
      fill.style.width = '0%';
      pct.textContent = '۰٪';
      status.textContent = 'فاز ۱ — انرژی‌رسانی هسته';
      flash.classList.remove('fire');
      scr.classList.remove('boot-final');
      eq.classList.remove('on');
      if (!eq.childElementCount) {
        for (let i = 0; i < 13; i++) {
          const bar = document.createElement('span');
          bar.style.animationDelay = (-(Math.random() * 0.9)).toFixed(2) + 's';
          bar.style.animationDuration = (0.6 + Math.random() * 0.7).toFixed(2) + 's';
          eq.appendChild(bar);
        }
      }
      scr.classList.add('active');
      const setPhase = (txt) => { if (bootActive) status.textContent = txt; };
      const LINES = buildBootLines();
      const t0 = performance.now(), DUR = 5250;
      const plateau = (v) => {
        if (v > 0.32 && v < 0.4) v = 0.32 + (v - 0.32) * 0.22;
        if (v > 0.68 && v < 0.76) v = 0.68 + (v - 0.68) * 0.22;
        return v;
      };
      const step = (t) => {
        if (!bootActive) return;
        const k = Math.min(1, (t - t0) / DUR);
        const eased = plateau(1 - Math.pow(1 - k, 2.2));
        const v = Math.round(eased * 100);
        fill.style.width = v + '%';
        pct.textContent = toPersian(v) + '٪';
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      bootTimers.push(setTimeout(() => setPhase('فاز ۲ — متریالایز پوسته ربات'), 900));
      bootTimers.push(setTimeout(() => { if (bootActive) eq.classList.add('on'); }, 2050));
      bootTimers.push(setTimeout(() => setPhase('فاز ۳ — اتصال شبکه عصبی'), 2150));
      bootTimers.push(setTimeout(() => setPhase('فاز ۴ — همگام‌سازی حافظه'), 3550));
      LINES.forEach((line, i) => {
        bootTimers.push(setTimeout(() => {
          if (!bootActive) return;
          term.querySelectorAll('.cur').forEach(cc => cc.remove());
          const div = document.createElement('div');
          div.className = 'boot-line';
          div.innerHTML = line + ' <span class="cur"></span>';
          term.appendChild(div);
        }, 1150 + i * 430));
      });
      bootTimers.push(setTimeout(() => {
        if (!bootActive) return;
        scr.classList.add('boot-final');
        setPhase('فاز ۵ — آماده‌به‌کار نهایی');
      }, 4700));
      bootTimers.push(setTimeout(() => {
        if (!bootActive) return;
        term.querySelectorAll('.cur').forEach(cc => cc.remove());
        const ok = document.createElement('div');
        ok.className = 'boot-line ok';
        ok.textContent = '✅ دستیار هوشمند آنلاین است — خوش آمدی';
        term.appendChild(ok);
      }, 4820));
      bootTimers.push(setTimeout(() => { if (bootActive) flash.classList.add('fire'); }, 5300));
      bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, 5650));
      bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, 9000));
    }

    document.getElementById('agentBootScreen').addEventListener('pointerdown', () => hideBootScreen(true));

    if ('serviceWorker' in navigator) {
      const swCode = `self.addEventListener('install', e => self.skipWaiting()); self.addEventListener('activate', e => e.waitUntil(clients.claim())); self.addEventListener('fetch', e => { e.respondWith(fetch(e.request).catch(() => new Response('Offline'))); });`;
      navigator.serviceWorker.register(URL.createObjectURL(new Blob([swCode], { type: 'application/javascript' }))).catch(() => {});
    }
  