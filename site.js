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

const NAV = [
  { href: 'index.html',    label: 'ホーム',     en: 'Home' },
  { href: 'event.html',    label: '無料相談会・お知らせ', en: 'Free Consultation' },
  { href: 'kengaku.html',  label: 'OB様邸見学',  en: "Owner's House" },
  { href: 'jisseki.html',  label: '建築実例',   en: 'Owners Voice' },
  { href: 'works.html',    label: '施工写真',   en: 'Gallery' },
  { href: 'products.html', label: '商品・価格', en: 'Products' },
  { href: 'spec.html',     label: '性能・標準仕様', en: 'Spec' },
  { href: 'flow.html',     label: '家づくりの進め方', en: 'How We Build' },
  { href: 'company.html',  label: '会社案内',   en: 'Company' },
  { href: 'members.html',  label: '私たち（代表紹介）', en: 'Members' },
  { href: 'after.html',    label: 'アフター・保証', en: 'After Service' },
  { href: 'blog.html',   label: 'ブログ',   en: 'Blog' },
  { href: 'reserve.html',  label: '来店予約',   en: 'Reserve' },
  { href: 'catalog.html',  label: '資料請求',   en: 'Catalog' },
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
  .nav-tel{margin-top:22px;flex-direction:column!important;align-items:flex-start!important;gap:3px!important;font-family:'Jost',sans-serif!important;font-size:18px!important;letter-spacing:.06em!important;border-bottom:none!important;color:#fff!important}
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
  ov.innerHTML = '<div class="nav-inner">' +
    NAV.map(p => `<a href="${p.href}" class="${p.href === here ? 'cur' : ''}"><span class="ne">${p.en}</span>${p.label}</a>`).join('') +
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
    lf.setAttribute('aria-label', 'LINEで相談');
    lf.innerHTML = '<span class="lw">LINE</span>で相談';
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
