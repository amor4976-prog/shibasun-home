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
  .nav-overlay a{display:flex;align-items:baseline;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.14);color:#fff;text-decoration:none;font-family:'Zen Kaku Gothic New',sans-serif;font-size:15px;font-weight:500;letter-spacing:.06em;transform:translateY(10px);opacity:0;transition:transform .4s,opacity .4s,color .2s}
  body.nav-open .nav-overlay a{transform:none;opacity:1}
  .nav-overlay a .ne{font-family:'Jost',sans-serif;font-size:10px;letter-spacing:.3em;color:#8f8f8d;text-transform:uppercase;min-width:62px}
  .nav-overlay a.cur{color:#fff}
  .nav-overlay a.cur .ne{color:#fff}
  .nav-overlay a:hover{color:#fff}
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
  .line-fab{position:fixed;right:16px;bottom:74px;z-index:150;display:inline-flex;align-items:center;gap:6px;height:46px;padding:0 17px;border-radius:24px;background:#06c755;box-shadow:0 4px 14px rgba(0,0,0,.22);color:#fff;font-family:'Noto Sans JP',sans-serif;font-size:12.5px;letter-spacing:.04em;font-weight:500;text-decoration:none;white-space:nowrap}
  .line-fab .lw{font-family:'Jost',sans-serif;font-weight:700;letter-spacing:.02em}
  .line-fab:hover{filter:brightness(.96)}
  @media(min-width:900px){
    .nav-overlay{align-items:center}
    .nav-overlay a{font-size:24px;justify-content:center}
    .line-fab{bottom:24px}
  }
  /* 改行の最適化：見出しは行を均等に、本文は最後の1〜2文字の孤立を防ぐ */
  h1,h2,h3{text-wrap:balance}
  p,li,.lead,.sub,.note,.sim-note,.rsv-note,.enote,.pickhint{text-wrap:pretty}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

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
    NAV.map(p => `<a href="${p.href}" class="${cur(p.href)}"><span class="ne">${p.en}</span>${p.label}</a>`).join('') +
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
    const lf = document.createElement('a');
    lf.className = 'line-fab';
    lf.href = LINE_URL; lf.target = '_blank'; lf.rel = 'noopener';
    lf.setAttribute('aria-label', 'LINEで聞く');
    lf.innerHTML = '<span class="lw">LINE</span>で聞く';
    lf.addEventListener('click', () => { if (window.gtag) window.gtag('event', 'line_click'); });
    document.body.appendChild(lf);
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
