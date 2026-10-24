#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TASK 18 - Patch B: generative music collections (offline synth) + library integration
import io, sys, re

APP = '/home/z/my-project/public/app.html'
src = io.open(APP, encoding='utf-8').read()

def replace_once(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: found %d' % (tag, n)); sys.exit(1)
    print('OK  [%s]' % tag)
    return s.replace(old, new, 1)

# ---------- B1) CSS ----------
css_anchor = "#agentBootScreen .boot-terminal { max-height: 118px; overflow: hidden; }"
css_add = css_anchor + """
  /* ==== TASK 18: generative music collections ==== */
  .gen-track-row { background: #fff; border: 1px solid var(--surface-container-highest, #e7e0ec); border-radius: 18px; padding: 10px 12px; display: flex; align-items: center; gap: 12px; box-shadow: 0 1px 4px rgba(20,10,50,0.05); }
  .gen-play-btn { width: 46px; height: 46px; border-radius: 14px; display: flex; align-items: center; justify-content: center; color: #fff; flex-shrink: 0; box-shadow: 0 3px 10px rgba(20,10,50,0.18); transition: transform .15s ease; }
  .gen-play-btn:active { transform: scale(0.9); }
  .gen-prog { height: 4px; border-radius: 4px; background: #ece5f3; overflow: hidden; margin-top: 7px; }
  .gen-prog > div { height: 100%; width: 0%; background: linear-gradient(90deg, var(--gen-a, #8b5cf6), var(--gen-b, #22d3ee)); transition: width .6s linear; }
  .gen-badge { font-size: 9px; font-weight: 800; padding: 2px 8px; border-radius: 100px; background: linear-gradient(90deg, rgba(139,92,246,.14), rgba(34,211,238,.14)); color: #7c3aed; border: 1px solid rgba(139,92,246,.25); }"""
src = replace_once(src, css_anchor, css_add, 'B1.css')

# ---------- B2) generative engine JS ----------
anchor = '    // ================= MUSIC LIBRARY ================='
GEN = r'''    // ================= TASK 18: GENERATIVE MUSIC ENGINE (offline, dozens of tracks per collection) =================
    const GEN_COLLECTIONS = [
      { id: 'calm',     name: 'آرامش',  emoji: '🧘', grad: 'linear-gradient(135deg,#6366f1,#8b5cf6 55%,#a78bfa)', a: '#8b5cf6', b: '#22d3ee', count: 24, bpm: 58,  scale: [0, 3, 5, 7, 10],  root: 220.0,  wave: 'calm' },
      { id: 'focus',    name: 'تمرکز',  emoji: '🎯', grad: 'linear-gradient(135deg,#0ea5e9,#6366f1 60%,#8b5cf6)', a: '#0ea5e9', b: '#8b5cf6', count: 24, bpm: 72,  scale: [0, 2, 5, 7, 9],   root: 261.6,  wave: 'flow' },
      { id: 'energy',   name: 'انرژی',  emoji: '⚡', grad: 'linear-gradient(135deg,#f59e0b,#ef4444 55%,#ec4899)', a: '#f59e0b', b: '#ef4444', count: 24, bpm: 112, scale: [0, 2, 4, 7, 9],   root: 293.7,  wave: 'drive' },
      { id: 'sleep',    name: 'خواب',   emoji: '🌙', grad: 'linear-gradient(135deg,#312e81,#4c1d95 60%,#1e1b4b)', a: '#6366f1', b: '#312e81', count: 18, bpm: 44,  scale: [0, 3, 7, 10],     root: 174.6,  wave: 'drift' },
      { id: 'nature',   name: 'طبیعت',  emoji: '🌿', grad: 'linear-gradient(135deg,#10b981,#059669 55%,#34d399)', a: '#10b981', b: '#34d399', count: 24, bpm: 64,  scale: [0, 2, 4, 7, 9],   root: 196.0,  wave: 'air' },
      { id: 'motivate', name: 'انگیزه', emoji: '🔥', grad: 'linear-gradient(135deg,#f43f5e,#8b5cf6 60%,#f59e0b)', a: '#f43f5e', b: '#f59e0b', count: 18, bpm: 96,  scale: [0, 3, 5, 7, 10],  root: 246.9,  wave: 'rise' }
    ];
    const GEN_TOTAL_TRACKS = GEN_COLLECTIONS.reduce((a, c) => a + c.count, 0);
    const GEN_NAMES = {
      calm: ['نفس عمیق', 'دریای آرام', 'مه صبحگاهی', 'شمع و سایه', 'قصه شب', 'پرنده سپید', 'ابریشم', 'نجوای خاموش', 'رسیدن به ساحل', 'برگ و باران', 'آسمان کدر', 'نور ملایم', 'آرامش ذهن', 'رودخانه', 'ستاره‌ها', 'شب بی‌خیال', 'چای داغ', 'کتاب و پتو', 'زمستان آرام', 'باران نرم', 'ابرها', 'عطر باغ', 'صدای دوردست', 'خواب سبک'],
      focus: ['تاندون ذهن', 'جریان عمیق', 'اتاق شیشه‌ای', 'پالس متمرکز', 'مدار بسته', 'خط مستقیم', 'نقطه نور', 'چرخ‌دنده', 'سکوت کار', 'تختال فولادی', 'عقربه‌ها', 'دوگانه حل', 'مرز روشن', 'لنگر ذهن', 'پرواز کروز', 'ثبات', 'نظم زرد', 'شبکه سیمی', 'زنجیره حلقه', 'دقیقه نود', 'تیزی', 'آهن‌ربا', 'چشم عقاب', 'پروژه کامل'],
      energy: ['طلوع برقی', 'ضربان سریع', 'آتش‌بازی', 'صبحانه ورزشی', 'ماشین دویدن', 'ریتم پا', 'خیزران', 'باد پشت سر', 'قله نزدیک', 'توربین', 'شتاب', 'موج پرفشار', 'جام قهرمانی', 'صاعقه', 'دوچرخه کوهستان', 'پمپ', 'جهش', 'خط پایان', 'کهکشان روشن', 'موتور', 'فواره', 'برق نقره', 'بازی تمام‌عیار', 'شعله'],
      sleep: ['وارونگی شب', 'پنجمین پلک', 'بادبادک ابری', 'قندیل نور', 'شب‌تاب', 'لحظه صفر', 'رؤیای آب', 'سکوت سنگین', 'بالشت ستاره', 'چتر مه', 'ماه کج', 'لالایی', 'عمق آبی', 'تخت ستاره', 'ساعت کند', 'خواب زمستانی', 'گل شب', 'رود ماه'],
      nature: ['جنگل بارانی', 'آبشار', 'زمین بعد از باران', 'گلزار', 'باد کوهستان', 'چمن شبنم', 'ساحل صخره‌ای', 'صدای جنگل', 'نسیم دریا', 'دره سبز', 'کاج‌ستان', 'برکه', 'صبح کوهستان', 'خزه و سنگ', 'درخت کهن', 'گل صحرایی', 'جویبار', 'پرواز پرنده', 'افق باز', 'زمستان جنگل', 'تپه نور', 'غار صدا', 'رگبار تابستانی', 'رعد دور'],
      motivate: ['خط عقب نیست', 'امروز همان روز است', 'یک قدم بیشتر', 'دیوار را بپران', 'رویای بزرگ', 'صدای قلب', 'سه دقیقه شجاعت', 'بلندپرواز', 'نترسیدن', 'ضربه آخر', 'پیش به سوی قله', 'آتش درون', 'مسیر من', 'روز من است', 'تا پرچم', 'قدرت عادت', 'مرد آهنی', 'نگهدار قول']
    };
    function genHash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
    function genRng(seed) { let x = seed >>> 0; return function () { x = Math.imul(x ^ (x >>> 15), 2246822519); x = Math.imul(x ^ (x >>> 13), 3266489917); x ^= x >>> 16; return (x >>> 0) / 4294967296; }; }
    function genTrackMeta(colId, n) {
      const col = GEN_COLLECTIONS.find(c => c.id === colId);
      if (!col) return null;
      const names = GEN_NAMES[colId] || [];
      const r = genRng(genHash(colId + ':' + n));
      const dur = 52 + Math.floor(r() * 56);
      return {
        id: 'gen:' + colId + ':' + n,
        colId: colId,
        n: n,
        name: (names[n % names.length] || 'قطعه ' + (n + 1)),
        dur: dur,
        col: col
      };
    }
    function genCollectionTracks(colId) {
      const col = GEN_COLLECTIONS.find(c => c.id === colId);
      if (!col) return [];
      const out = [];
      for (let i = 0; i < col.count; i++) out.push(genTrackMeta(colId, i));
      return out;
    }

    let genAudioCtx = null;
    let genSource = null;
    let genPlayingId = null;
    let genStartedAt = 0;
    let genBufferDur = 0;
    let genProgressTimer = null;
    let genQueueCol = null;

    function genEnsureCtx() {
      if (!genAudioCtx) {
        const AC = window.AudioContext || window.webkitAudioContext;
        genAudioCtx = new AC();
      }
      if (genAudioCtx.state === 'suspended') { try { genAudioCtx.resume(); } catch (e) {} }
      return genAudioCtx;
    }
    function stopGenTrack(silent) {
      try { if (genSource) { genSource.onended = null; try { genSource.stop(); } catch (e) {} genSource = null; } } catch (e) {}
      try { if (genProgressTimer) { clearInterval(genProgressTimer); genProgressTimer = null; } } catch (e) {}
      const was = genPlayingId;
      genPlayingId = null;
      genQueueCol = null;
      if (was && !silent) renderGenList(document.getElementById('musicTrackList'));
    }
    function renderSynthTrack(meta) {
      const col = meta.col;
      const sr = 22050;
      const dur = meta.dur;
      const OAC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      const ctx = new OAC(1, Math.ceil(dur * sr), sr);
      const rng = genRng(genHash(meta.id));
      const master = ctx.createGain();
      master.gain.value = 0.9;
      master.connect(ctx.destination);
      // space echo
      const delay = ctx.createDelay(1.2);
      delay.delayTime.value = Math.max(0.2, 60 / col.bpm * 0.75);
      const fb = ctx.createGain(); fb.gain.value = col.wave === 'drive' ? 0.18 : 0.34;
      const wet = ctx.createGain(); wet.gain.value = 0.3;
      delay.connect(fb); fb.connect(delay); delay.connect(wet); wet.connect(master);
      // pad chord (root + fifth + octave, detuned)
      const padFilter = ctx.createBiquadFilter();
      padFilter.type = 'lowpass';
      padFilter.frequency.value = col.wave === 'drive' ? 1600 : (col.wave === 'drift' ? 520 : 900);
      const padGain = ctx.createGain();
      padGain.gain.setValueAtTime(0.0001, 0);
      padGain.gain.linearRampToValueAtTime(col.wave === 'drift' ? 0.16 : 0.12, 4);
      padGain.gain.setValueAtTime(0.12, dur - 5);
      padGain.gain.linearRampToValueAtTime(0.0001, dur - 0.2);
      padFilter.connect(padGain); padGain.connect(master); padGain.connect(delay);
      [[1, 'sine'], [1.5, 'triangle'], [2, 'sine']].forEach((p, i) => {
        const o = ctx.createOscillator();
        o.type = p[1];
        o.frequency.value = col.root * p[0] * (1 + (rng() - 0.5) * 0.006);
        const g = ctx.createGain(); g.gain.value = 0.5 / (i + 1);
        o.connect(g); g.connect(padFilter);
        o.start(0); o.stop(dur);
      });
      // slow filter LFO
      const lfo = ctx.createOscillator(); lfo.frequency.value = 0.06 + rng() * 0.05;
      const lfoG = ctx.createGain(); lfoG.gain.value = padFilter.frequency.value * 0.4;
      lfo.connect(lfoG); lfoG.connect(padFilter.frequency); lfo.start(0); lfo.stop(dur);
      // sequencer
      const stepDur = 60 / col.bpm / 2;
      const totalSteps = Math.floor(dur / stepDur);
      const bassStep = col.wave === 'drive' ? 4 : 8;
      let prevNote = 0;
      for (let s = 0; s < totalSteps; s++) {
        const t = s * stepDur;
        // arp melody
        if (s % (col.wave === 'drift' ? 4 : 2) === 0 && rng() < (col.wave === 'drive' ? 0.92 : 0.66)) {
          const deg = col.scale[Math.floor(rng() * col.scale.length)];
          const oct = rng() < 0.3 ? 2 : 1;
          const freq = col.root * Math.pow(2, deg / 12) * oct;
          prevNote = freq;
          const o = ctx.createOscillator();
          o.type = col.wave === 'drive' ? 'square' : 'triangle';
          o.frequency.value = freq;
          const g = ctx.createGain();
          const len = stepDur * (col.wave === 'drive' ? 0.9 : 1.8);
          g.gain.setValueAtTime(0.0001, t);
          g.gain.exponentialRampToValueAtTime(col.wave === 'drive' ? 0.11 : 0.075, t + 0.02);
          g.gain.exponentialRampToValueAtTime(0.0001, t + len);
          const fl = ctx.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = 2400;
          o.connect(fl); fl.connect(g); g.connect(master); g.connect(delay);
          o.start(t); o.stop(Math.min(dur, t + len + 0.05));
        }
        // bass
        if (s % bassStep === 0) {
          const o = ctx.createOscillator(); o.type = 'sine';
          o.frequency.value = col.root * 0.5 * (rng() < 0.2 ? 0.75 : 1);
          const g = ctx.createGain();
          g.gain.setValueAtTime(0.0001, t);
          g.gain.exponentialRampToValueAtTime(0.14, t + 0.03);
          g.gain.exponentialRampToValueAtTime(0.0001, t + stepDur * 3);
          o.connect(g); g.connect(master);
          o.start(t); o.stop(t + stepDur * 3.1);
        }
        // hats for energetic moods
        if ((col.wave === 'drive' || col.wave === 'rise') && s % 2 === 1 && rng() < 0.8) {
          const nb = ctx.createBuffer(1, 900, sr);
          const nd = nb.getChannelData(0);
          for (let i = 0; i < 900; i++) nd[i] = (rng() * 2 - 1) * Math.pow(1 - i / 900, 2.5);
          const ns = ctx.createBufferSource(); ns.buffer = nb;
          const nf = ctx.createBiquadFilter(); nf.type = 'highpass'; nf.frequency.value = 6000;
          const ng = ctx.createGain(); ng.gain.value = 0.05;
          ns.connect(nf); nf.connect(ng); ng.connect(master);
          ns.start(t);
        }
        // air shimmer for calm/nature/sleep
        if ((col.wave === 'calm' || col.wave === 'air' || col.wave === 'drift') && s % 16 === 0 && rng() < 0.6) {
          const o2 = ctx.createOscillator(); o2.type = 'sine';
          o2.frequency.value = col.root * Math.pow(2, col.scale[Math.floor(rng() * col.scale.length)] / 12) * 4;
          const g2 = ctx.createGain();
          g2.gain.setValueAtTime(0.0001, t);
          g2.gain.exponentialRampToValueAtTime(0.02, t + 1.2);
          g2.gain.exponentialRampToValueAtTime(0.0001, t + 3.5);
          o2.connect(g2); g2.connect(master); g2.connect(delay);
          o2.start(t); o2.stop(Math.min(dur, t + 3.6));
        }
      }
      return ctx.startRendering();
    }
    function playGenTrack(id) {
      const parts = String(id).split(':');
      if (parts.length !== 3 || parts[0] !== 'gen') return;
      const meta = genTrackMeta(parts[1], parseInt(parts[2], 10));
      if (!meta) return;
      // stop uploaded audio if playing
      try { if (typeof musicAudio !== 'undefined' && musicAudio && !musicAudio.paused) musicAudio.pause(); } catch (e) {}
      try { if (typeof currentPlayingId !== 'undefined') currentPlayingId = null; } catch (e) {}
      stopGenTrack(true);
      try { if (typeof renderMusicList === 'function') renderMusicList(); } catch (e) {}
      genEnsureCtx();
      genPlayingId = id;
      renderGenList(document.getElementById('musicTrackList'));
      showToast('در حال ساختن «' + meta.name + '»... 🎼');
      renderSynthTrack(meta).then(buf => {
        if (genPlayingId !== id) return;
        const ctx = genEnsureCtx();
        const src = ctx.createBufferSource();
        src.buffer = buf;
        const g = ctx.createGain();
        g.gain.setValueAtTime(0.0001, ctx.currentTime);
        g.gain.linearRampToValueAtTime(0.9, 0.4);
        src.connect(g); g.connect(ctx.destination);
        src.onended = () => {
          if (genPlayingId !== id) return;
          // auto-advance within collection
          if (genQueueCol) {
            const list = genCollectionTracks(genQueueCol);
            const idx = list.findIndex(t => t.id === id);
            const next = list[(idx + 1) % list.length];
            setTimeout(() => { if (genPlayingId === id || !genPlayingId) playGenTrack(next.id); }, 600);
            return;
          }
          stopGenTrack();
        };
        genSource = src;
        genBufferDur = buf.duration;
        genStartedAt = Date.now();
        src.start();
        genProgressTimer = setInterval(() => {
          const p = Math.min(100, ((Date.now() - genStartedAt) / 1000 / genBufferDur) * 100);
          document.querySelectorAll('.gen-prog > div').forEach(d => { d.style.width = p + '%'; });
          if (p >= 100) { try { clearInterval(genProgressTimer); } catch (e) {} }
        }, 900);
        renderGenList(document.getElementById('musicTrackList'));
      }).catch(() => { showToast('ساخت قطعه ممکن نشد 😕'); stopGenTrack(true); });
    }
    function playGenCollection(colId) {
      genQueueCol = colId;
      const list = genCollectionTracks(colId);
      if (list.length) playGenTrack(list[Math.floor(Math.random() * list.length)].id);
    }
    function renderGenList(container) {
      if (!container) return;
      const colId = String(currentMusicTab).slice(4);
      const col = GEN_COLLECTIONS.find(c => c.id === colId);
      if (!col) return;
      const tracks = genCollectionTracks(colId);
      container.innerHTML =
        '<div class="rounded-2xl p-3.5 mb-3 flex items-center justify-between" style="background:' + col.grad + ';">' +
          '<div><div class="text-white font-extrabold text-[15px]">' + col.emoji + ' کلکسیون ' + col.name + '</div>' +
          '<div class="text-white/85 text-[10.5px] font-bold mt-0.5">' + toPersian(col.count) + ' قطعه‌ی تولیدی · همین‌جا ساخته می‌شود · آفلاین ✨</div></div>' +
          '<button onclick="playGenCollection(\'' + colId + '\')" class="w-10 h-10 rounded-full bg-white/25 text-white flex items-center justify-center active:scale-90 transition-transform"><span class="material-symbols-outlined text-[20px]">play_arrow</span></button>' +
        '</div>' +
        tracks.map(t => {
          const playing = genPlayingId === t.id;
          return '<div class="gen-track-row" data-gen="' + t.id + '">' +
            '<button onclick="' + (playing ? 'stopGenTrack()' : 'playGenTrack(\'' + t.id + '\')') + '" class="gen-play-btn" style="background:' + col.grad + ';">' +
              '<span class="material-symbols-outlined text-[22px]">' + (playing ? 'stop' : 'play_arrow') + '</span></button>' +
            '<div class="flex-1 min-w-0">' +
              '<div class="flex items-center gap-1.5"><span class="text-[13px] font-bold text-on-surface truncate">' + t.name + '</span>' +
              '<span class="gen-badge">هوشمند</span></div>' +
              '<div class="text-[10px] text-on-surface-variant font-medium mt-0.5">' + col.emoji + ' ' + col.name + ' · ' + toPersian(Math.floor(t.dur / 60)) + ':' + toPersian(String(t.dur % 60).padStart(2, '0')) + '</div>' +
              (playing ? '<div class="gen-prog" style="--gen-a:' + col.a + ';--gen-b:' + col.b + '"><div></div></div>' : '') +
            '</div></div>';
        }).join('');
    }
    function buildGenCollectionCards() {
      return GEN_COLLECTIONS.map(c => {
        const spines = genCollectionTracks(c.id).slice(0, 6).map((t, i) =>
          '<div class="music-book-spine" style="height:' + [84, 66, 76, 58, 80, 70][i] + 'px; transform:rotate(' + [-2.5, 1.6, -1, 2.4, -1.8, 1.2][i] + 'deg); background: linear-gradient(180deg, rgba(255,255,255,0.3), rgba(255,255,255,0.04) 55%), ' + c.grad + '; z-index:' + (10 - i) + ';">' + c.emoji + '</div>'
        ).join('');
        return '<div class="music-collection-card relative overflow-hidden rounded-[28px] p-4 cursor-pointer active:scale-[0.98] transition-transform" style="background:' + c.grad + ';" onclick="setMusicTab(\'gen:' + c.id + '\')">' +
          '<span class="absolute top-3 left-3 text-xl opacity-85 select-none">✨</span>' +
          '<div class="flex items-start justify-between mb-3 relative z-10">' +
            '<div><h4 class="text-white font-extrabold text-[16px] drop-shadow-sm">' + c.emoji + ' ' + c.name + ' · هوشمند</h4>' +
            '<span class="text-white/85 text-[10.5px] font-bold">' + toPersian(c.count) + ' قطعه تولیدی — بدون اینترنت</span></div>' +
            '<button onclick="event.stopPropagation(); playGenCollection(\'' + c.id + '\')" class="w-9 h-9 rounded-full bg-white/25 hover:bg-white/40 text-white flex items-center justify-center transition-all active:scale-90 shadow-md"><span class="material-symbols-outlined text-[18px]">play_arrow</span></button>' +
          '</div>' +
          '<div class="music-shelf-row relative z-10">' + spines + '</div>' +
          '<div class="music-shelf-line relative z-10"></div>' +
        '</div>';
      }).join('');
    }

'''
src = replace_once(src, anchor, GEN + anchor, 'B2.gen-engine')

# ---------- B3) tabs ----------
old_tabs = """      const tabs = [
        { id: 'all', label: `همه (${toPersian(state.musicTracks.length)})` },"""
new_tabs = """      const genTabs = GEN_COLLECTIONS.map(c => ({ id: 'gen:' + c.id, label: `${c.emoji} ${c.name} (${toPersian(c.count)})` }));
      const tabs = [
        ...genTabs,
        { id: 'all', label: `همه (${toPersian(state.musicTracks.length)})` },"""
src = replace_once(src, old_tabs, new_tabs, 'B3.tabs')

# ---------- B4) renderMusicList branch ----------
old_rl = """    function renderMusicList() {
      const list = document.getElementById('musicTrackList');
      if (!list) return;
      const tracks = musicFilteredTracks();"""
new_rl = """    function renderMusicList() {
      const list = document.getElementById('musicTrackList');
      if (!list) return;
      if (String(currentMusicTab).indexOf('gen:') === 0) { renderGenList(list); return; }
      const tracks = musicFilteredTracks();"""
src = replace_once(src, old_rl, new_rl, 'B4.list-branch')

# ---------- B5) gen collection cards on 'all' ----------
old_cards = "      wrap.innerHTML = keys.map(k => {"
new_cards = "      wrap.innerHTML = buildGenCollectionCards() + keys.map(k => {"
src = replace_once(src, old_cards, new_cards, 'B5.cards')

# ---------- B6) count label ----------
old_lbl = "      if (el) el.textContent = `${toPersian(state.musicTracks.length)} موزیک در قفسه`;"
new_lbl = "      if (el) el.textContent = `${toPersian(state.musicTracks.length)} موزیک شخصی · ${toPersian(GEN_TOTAL_TRACKS)} قطعه هوشمند`;"
src = replace_once(src, old_lbl, new_lbl, 'B6.label')

io.open(APP, 'w', encoding='utf-8').write(src)
print('DONE patch B')
