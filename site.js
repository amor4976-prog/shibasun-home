/* ============================================================
   SHIBA SUN HOME — 共通サイト設定（ナビ・ロゴ）
   © 株式会社シバ・サンホーム  無断複製・転用を禁じます
   ------------------------------------------------------------
   ▼ロゴを設定する：下の LOGO_SRC に画像パスを入れるだけ
     例) const LOGO_SRC = 'img/logo.png';
     （空のままだと「SHIBA SUN HOME」の文字ロゴを表示します）
   ============================================================ */
const LOGO_SRC = '';            // ★ここに自社ロゴ画像のパスを設定
const LOGO_ALT = '株式会社シバ・サンホーム';
const TEL = '0120154483';
const TEL_DISP = '0120-154-483';
const LINE_URL = 'https://lin.ee/ueeBddk';   // お客様用「友だち追加」リンク（LINE公式 lin.ee 短縮リンク）
const GA_ID = 'G-REFN8K7K95';  // 現行shibasun.jpと同じGA4プロパティ（データ継続）。本番shibasun.jpでのみ計測（下のガード参照）

// 主要導線（大きく表示）— 引き算：8項目に厳選
const NAV = [
  { href: 'index.html',    label: 'ホーム',     en: 'Home' },
  { href: 'iezukuri.html', label: '私たちの家づくり', en: 'Our Home Building' },
  { href: 'jisseki.html',  label: '建築実例',   en: 'Works' },
  { href: 'kengaku.html',  label: 'OB様邸見学',  en: "Owner's House" },
  { href: 'products.html', label: '商品・価格', en: 'Products' },
  { href: 'spec.html',     label: '性能・標準仕様', en: 'Spec' },
  { href: 'flow.html',     label: '家づくりの進め方', en: 'How We Build' },
  { href: 'company.html',  label: '会社案内',   en: 'Company' },
  { href: 'blog.html',     label: 'ブログ',     en: 'Blog' },
];
// そのほか（控えめに・小さく）— 消さずにたたむ
const NAV_SUB = [
  { href: 'hajimete.html', label: 'はじめての方へ' },
  { href: 'lessons.html',  label: '後悔しない家づくり（動画）' },
  { href: 'members.html',  label: '私たち（代表紹介）' },
  { href: 'after.html',    label: 'アフター・保証' },
  { href: 'reform.html',   label: 'リフォーム' },
  { href: 'event.html',    label: '個別無料相談会' },
];
// 予約・資料（ボタン扱い）
const NAV_CV = [
  { href: 'reserve.html',  label: '来店予約' },
  { href: 'catalog.html',  label: '資料請求' },
];

(function () {
  const here = (location.pathname.split('/').pop() || 'index.html');

  // ---- 共通CSS（1ファイルで全ページに適用） ----
  const css = `
  /* 日本語の改行（全ページ共通） */
  /* ① 禁則：行頭に「、。ー っ ）」」が来ないようにする */
  /* ⓪ iPhoneの自動文字拡大を止める。これが無いと実機だけ文字が1.8倍になり
     「まじめにつ／くる品質。」のような語中改行が起きる（2026-08-30 専務がiPhone7で発見） */
  html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
  body{line-break:strict;overflow-wrap:break-word}
  h1,h2,h3,h4,p,li,dt,dd,figcaption,span{line-break:strict}
  /* ② 語の途中で改行しない（「無料。し／つこい営業」を防ぐ）
        ブラウザが言葉の切れ目を判断する。対応していないブラウザは無視するだけで崩れない */
  body,h1,h2,h3,h4,p,li,dt,dd,figcaption,summary,button,td,th,blockquote{word-break:auto-phrase}
  /* ③ 見出しは行の長さを均す／本文は最終行が1〜2文字だけにならないようにする */
  h1,h2,h3,h4{text-wrap:balance}
  p,li,dd,dt,figcaption,figcaption b,figcaption span,td,th,summary{text-wrap:pretty}

  .nav-toggle{position:relative;width:30px;height:22px;background:none;border:none;cursor:pointer;padding:0;z-index:402}
  .nav-toggle span{position:absolute;left:0;width:100%;height:1.6px;background:var(--ink,#1c1c1a);transition:.3s}
  .nav-toggle span:nth-child(1){top:0}.nav-toggle span:nth-child(2){top:10px}.nav-toggle span:nth-child(3){top:20px}
  body.nav-open .nav-toggle span{background:#fff}
  body.nav-open .nav-toggle span:nth-child(1){transform:translateY(10px) rotate(45deg)}
  body.nav-open .nav-toggle span:nth-child(2){opacity:0}
  body.nav-open .nav-toggle span:nth-child(3){transform:translateY(-10px) rotate(-45deg)}
  .nav-overlay{position:fixed;inset:0;z-index:400;background:#161614;color:#fff;display:flex;flex-direction:column;justify-content:flex-start;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:30px 32px;opacity:0;visibility:hidden;transition:opacity .35s}
  .nav-inner{margin:auto 0;width:100%}
  body.nav-open{overflow:hidden}
  body.nav-open .nav-overlay{opacity:1;visibility:visible}
  .nav-overlay a{display:flex;align-items:baseline;justify-content:space-between;gap:16px;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.10);color:#fff;text-decoration:none;font-family:'Zen Kaku Gothic New',sans-serif;font-weight:400;transform:translateY(10px);opacity:0;transition:transform .4s,opacity .4s,color .2s,padding-left .3s}
  body.nav-open .nav-overlay a{transform:none;opacity:1}
  .nav-overlay a .nj{font-size:14px;letter-spacing:.14em;line-height:1.5}
  .nav-overlay a .ne{font-family:'Jost',sans-serif;font-size:8.5px;letter-spacing:.28em;color:#7c7a75;text-transform:uppercase;white-space:nowrap}
  .nav-overlay a.cur .nj{color:#fff;position:relative}
  .nav-overlay a.cur .nj::after{content:"";position:absolute;left:0;right:0;bottom:-5px;height:1px;background:rgba(255,255,255,.5)}
  .nav-overlay a.cur .ne{color:#c9c6c0}
  .nav-overlay a:hover{padding-left:6px}
  .nav-overlay a:hover .ne{color:#b7b5b1}
  .nav-cv{display:flex;gap:10px;margin-top:24px}
  .nav-cv a{flex:1;justify-content:center!important;padding:13px 0!important;border:1px solid rgba(255,255,255,.55)!important;border-radius:2px;font-size:14px!important;letter-spacing:.08em!important;color:#fff!important;transform:none!important;opacity:1!important}
  .nav-cv a:first-child{background:#fff!important;color:#161614!important;border-color:#fff!important}
  .nav-sub-h{margin-top:26px;font-family:'Jost',sans-serif;font-size:10px;letter-spacing:.28em;color:#82817e;text-transform:uppercase}
  .nav-sub{display:flex;flex-wrap:wrap;gap:4px 20px;margin-top:12px}
  .nav-sub a{display:inline-block!important;padding:5px 0!important;border-bottom:none!important;font-size:13px!important;letter-spacing:.04em!important;font-weight:400!important;color:#b7b5b1!important;transform:none!important;opacity:1!important}
  .nav-sub a.cur{color:#fff!important}
  .nav-tel{margin-top:24px;flex-direction:column!important;align-items:flex-start!important;gap:3px!important;font-family:'Jost',sans-serif!important;font-size:18px!important;letter-spacing:.06em!important;border-bottom:none!important;color:#fff!important}
  .nav-tel small{display:block;font-family:'Noto Sans JP',sans-serif;font-size:10px;letter-spacing:.16em;color:#9b978f;margin-top:4px}
  .logo-img{height:30px;width:auto;display:block}
  .fixed-cta.three{grid-template-columns:repeat(3,1fr)!important}
  .fixed-cta .fc-line{display:flex;align-items:center;justify-content:center;gap:5px;background:#fff;color:var(--ink,#1a1a1a);font-family:'Noto Sans JP',sans-serif;font-size:12px;letter-spacing:.14em;text-decoration:none;border-right:1px solid var(--linec,#e8e8e6)}
  .fixed-cta .fc-line .lw{font-family:'Jost',sans-serif;font-weight:600;letter-spacing:.04em;font-size:13px;color:#06c755}
  .fixed-cta .fc-line:hover{background:#fafaf8}
  .line-fab{position:fixed;right:16px;bottom:74px;z-index:150;display:inline-flex;align-items:center;gap:6px;height:46px;padding:0 17px;border-radius:24px;background:#06c755;box-shadow:0 4px 14px rgba(0,0,0,.22);color:#fff;font-family:'Noto Sans JP',sans-serif;font-size:12.5px;letter-spacing:.04em;font-weight:500;text-decoration:none;white-space:nowrap}
  .line-fab .lw{font-family:'Jost',sans-serif;font-weight:700;letter-spacing:.02em}
  .line-fab:hover{filter:brightness(.96)}
  @media(min-width:900px){
    .nav-overlay{align-items:center}
    .nav-inner{max-width:620px}
    .nav-overlay a{padding:15px 0}
    .nav-overlay a .nj{font-size:17px}
    .nav-overlay a .ne{font-size:9px}
    .line-fab{bottom:24px}
  }
  /* 改行の最適化：見出しは行を均等に、本文は最後の1〜2文字の孤立を防ぐ */
  h1,h2,h3{text-wrap:balance}
  p,li,.lead,.sub,.note,.sim-note,.rsv-note,.enote,.pickhint{text-wrap:pretty}
  /* ここで囲んだ語は絶対に途中で折り返さない */
  /* ⚠️ページ側の「span{display:block}」を必ず打ち消す。効かないと語が単独行になる（2026-07-26に実例ページで発生） */
  .nb{display:inline!important;white-space:nowrap}
  .no,.rank{white-space:nowrap}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  // ---- 途中で切れると読みにくい語を、折り返し禁止で包む ----
  // ブラウザの言葉区切り（word-break:auto-phrase）でも切れてしまう語を、実測で拾って登録している
  const NOBREAK = ['シバ・サンホーム','チームシバサン会','関西国際空港','大工社長','人となり','突き板',
    'お問い合わせ','立ち上がり','マーク付き','部屋どうし','ひと続き','わがまま','おおよそ','しがちな',
    '自由度','見た目','落として','落とさず','落とし','を通じて','として','という','により','による',
    '明るさ','ぜひ','部屋','にくく','によって','間に合わ',
    '土地さがし','日当たり','ようへき','にとって','なければ','ふさがって','詰まって','はらみ','水抜き穴'];
  (function nobreak(){
    const re = new RegExp('(' + NOBREAK.sort((a,b)=>b.length-a.length).join('|') + ')', 'g');
    const skip = 'script,style,textarea,code,pre,title,.nb';
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(n){
        if (!n.nodeValue || !re.test(n.nodeValue)) return NodeFilter.FILTER_REJECT;
        return n.parentElement && n.parentElement.closest(skip) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    const targets = []; let n;
    while ((n = w.nextNode())) targets.push(n);
    targets.forEach(node => {
      const frag = document.createDocumentFragment();
      let last = 0; const s = node.nodeValue; re.lastIndex = 0; let m;
      while ((m = re.exec(s))) {
        if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
        const sp = document.createElement('span'); sp.className = 'nb'; sp.textContent = m[0];
        frag.appendChild(sp); last = m.index + m[0].length;
      }
      if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  })();

  // ---- 記号が行頭に来ないようにする ----
  // 「2026年の住宅補助金／｜奈良で家を建てる人」のように、区切りの「｜」が
  // 次の行の頭に落ちると、置き忘れた記号に見える（2026-08-30 コラム一覧で発生）。
  // 直前の1文字とくっつけて折り返させない。
  (function kigouAtama(){
    const re = /.[｜|]/g;
    const skip = 'script,style,textarea,code,pre,title,.nb';
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(n){
        if (!n.nodeValue || !/[｜|]/.test(n.nodeValue)) return NodeFilter.FILTER_REJECT;
        return n.parentElement && n.parentElement.closest(skip) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    const targets = []; let n;
    while ((n = w.nextNode())) targets.push(n);
    targets.forEach(node => {
      const frag = document.createDocumentFragment();
      let last = 0; const s = node.nodeValue; re.lastIndex = 0; let m;
      while ((m = re.exec(s))) {
        if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
        const sp = document.createElement('span'); sp.className = 'nb'; sp.textContent = m[0];
        frag.appendChild(sp); last = m.index + m[0].length;
      }
      if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  })();

  // ---- ロゴ画像の差し替え（LOGO_SRC が設定されていれば） ----
  if (LOGO_SRC) {
    document.querySelectorAll('a.logo').forEach(a => {
      a.innerHTML = '<img class="logo-img" src="' + LOGO_SRC + '" alt="' + LOGO_ALT + '">';
    });
  }

  // ---- ハンバーガー＋メニュー注入 ----
  const header = document.querySelector('header');
  if (!header) return;
  // 既存の右側リンク（← Home / Contact）は撤去してメニューに集約
  header.querySelectorAll('.back, .head-cta').forEach(el => el.remove());

  const btn = document.createElement('button');
  btn.className = 'nav-toggle';
  btn.setAttribute('aria-label', 'メニューを開く');
  btn.innerHTML = '<span></span><span></span><span></span>';
  header.appendChild(btn);

  const ov = document.createElement('nav');
  ov.className = 'nav-overlay';
  ov.setAttribute('aria-label', 'メインメニュー');
  const cur = h => h === here ? 'cur' : '';
  ov.innerHTML = '<div class="nav-inner">' +
    NAV.map(p => `<a href="${p.href}" class="${cur(p.href)}"><span class="nj">${p.label}</span><span class="ne">${p.en}</span></a>`).join('') +
    `<div class="nav-cv">` + NAV_CV.map(p => `<a href="${p.href}" class="${cur(p.href)}">${p.label}</a>`).join('') + `</div>` +
    `<div class="nav-sub-h">そのほか</div>` +
    `<div class="nav-sub">` + NAV_SUB.map(p => `<a href="${p.href}" class="${cur(p.href)}">${p.label}</a>`).join('') + `</div>` +
    `<a class="nav-tel" href="tel:${TEL}">${TEL_DISP}<small>受付 9:00-18:00（水曜定休）</small></a></div>`;
  document.body.appendChild(ov);

  btn.addEventListener('click', () => document.body.classList.toggle('nav-open'));
  ov.addEventListener('click', e => { if (e.target === ov || e.target.closest('a')) document.body.classList.remove('nav-open'); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') document.body.classList.remove('nav-open'); });

  // ---- LINE フローティングボタン（LINE_URL を設定したときだけ表示）----
  if (LINE_URL) {
    const bar = document.querySelector('.fixed-cta');
    const mkLine = (cls) => {
      const a = document.createElement('a');
      a.className = cls;
      a.href = LINE_URL; a.target = '_blank'; a.rel = 'noopener';
      a.setAttribute('aria-label', 'LINEで聞く');
      a.innerHTML = '<span class="lw">LINE</span>で聞く';
      a.addEventListener('click', () => { if (window.gtag) window.gtag('event', 'line_click'); });
      return a;
    };
    if (bar) {
      // 下の固定バーを「電話｜LINE｜来店予約」の3分割にする（写真の上に浮かせない）
      if (!bar.querySelector('.fc-line')) {
        bar.classList.add('three');
        const tel = bar.querySelector('.fc-tel');
        const line = mkLine('fc-line');
        if (tel && tel.nextSibling) bar.insertBefore(line, tel.nextSibling);
        else bar.appendChild(line);
      }
    } else {
      document.body.appendChild(mkLine('line-fab'));
    }
    // アフターページ等の「LINEで相談」ボタンも有効化
    document.querySelectorAll('a.hbtn.line').forEach(a => {
      a.href = LINE_URL; a.target = '_blank'; a.rel = 'noopener'; a.onclick = null;
      const ph = a.querySelector('.fillin'); if (ph) ph.remove();
    });
  }

  // ---- 電話タップの計測（成果として記録）----
  document.addEventListener('click', e => {
    const t = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (t && window.gtag) window.gtag('event', 'tel_click');
  });

  // ---- フッターにプライバシーポリシーをひっそり追加（全ページ共通）----
  document.querySelectorAll('footer').forEach(f => {
    if (f.querySelector('a[href="privacy.html"]')) return;
    const d = document.createElement('div');
    d.style.cssText = 'margin-top:12px;font-size:10px;letter-spacing:.1em;opacity:.55';
    d.innerHTML = '<a href="privacy.html" style="color:inherit">プライバシーポリシー</a>';
    f.appendChild(d);
  });

  // ---- スマホの改行崩れ番人（全ページ共通・2026-07-22 専務指示）----
  // センター寄せの文章が2行以上に折り返す場合だけ、自動で左揃えに切り替える。
  // 1行に収まる短いキャッチはセンターのまま。意図的な短い行（brで整えた詩的な行）も触らない。
  // 熟語の行またぎ（「職↵人」「ではあ↵りません」）が"AI感"を出すのを防ぐのが目的。
  function fixCenteredText() {
    if (window.innerWidth >= 600) return;
    document.querySelectorAll('p,li,dd,figcaption').forEach(el => {
      if (el.dataset.keepCenter !== undefined) return;           // data-keep-center で除外可
      const t = (el.innerText || '').trim();
      if (t.replace(/\n/g, '').length < 24) return;              // 短文はそのまま
      const cs = getComputedStyle(el);
      if (cs.textAlign !== 'center' || cs.display === 'none') return;
      const frs = el.innerHTML.split(/<br[^>]*>/i).map(s => s.replace(/<[^>]+>/g, '').trim());
      if (frs.length > 1 && frs.every(f => f.length <= 22)) return; // brで整えた短い行は意図的
      const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.8;
      if (el.getBoundingClientRect().height > lh * 1.5) el.style.textAlign = 'left';
    });
  }
  fixCenteredText();
  window.addEventListener('load', fixCenteredText);              // Webフォント適用後にもう一度
  let fcTimer; window.addEventListener('resize', () => { clearTimeout(fcTimer); fcTimer = setTimeout(fixCenteredText, 200); });

  // ---- GA4 アクセス解析（GA_ID 設定 かつ 本番ドメイン shibasun.jp のときだけ有効）----
  // ローカル・プレビュー・他ドメインでは計測しない（テストのニセ数字でデータを汚さないため）
  if (GA_ID && /(^|\.)shibasun\.jp$/i.test(location.hostname)) {
    const g = document.createElement('script'); g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
  }
})();
