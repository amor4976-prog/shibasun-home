/* 資料請求の流入記録。氏名・連絡先・参照URLのクエリは保存しない。 */
(function () {
  'use strict';
  var KEY='shibasun_inquiry_source_v1', DAY=86400000, now=Date.now(), state={}, q=new URLSearchParams(location.search);
  function clean(v,max){return String(v||'').replace(/[<>"'&\u0000-\u001f\u007f]/g,'').slice(0,max||100);}
  function touch(v){
    if(!v||typeof v!=='object'||!Number.isFinite(v.at)||v.at>now+60000||now-v.at>30*DAY)return null;
    var out={at:v.at,landing:clean(v.landing,160),referrer:clean(v.referrer,120)};
    ['gclid','gbraid','wbraid','utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){if(v[k])out[k]=clean(v[k],k.indexOf('utm_')===0?100:200);});
    return out;
  }
  try{state=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){}
  state={first:touch(state.first),session:touch(state.session),lastKnown:touch(state.lastKnown),lastSeen:Number(state.lastSeen)||0};
  var ref='';try{var u=new URL(document.referrer);if(u.hostname!==location.hostname&&!/^(www\.)?shibasun\.jp$/.test(u.hostname))ref=clean(u.hostname,120);}catch(e){}
  var current={at:now,landing:clean(location.pathname,160),referrer:ref}, tagged=false;
  ['gclid','gbraid','wbraid','utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){var v=q.get(k);if(v){current[k]=clean(v,k.indexOf('utm_')===0?100:200);tagged=true;}});
  if(!state.session||now-state.lastSeen>30*60000||tagged||ref)state.session=current;
  if(!state.first)state.first=state.session;
  if(tagged||ref)state.lastKnown=current;
  state.lastSeen=now;
  try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){}
  function label(t){
    if(!t)return '不明';
    if(t.gclid||t.gbraid||t.wbraid)return 'Google広告（クリック識別子あり）';
    if(t.utm_source||t.utm_medium)return (t.utm_source||'不明')+' / '+(t.utm_medium||'不明')+'（UTM指定）';
    if(/(^|\.)google\.[a-z.]+$/.test(t.referrer))return 'Googleから（広告識別情報なし）';
    if(/(^|\.)(yahoo\.co\.jp|bing\.com)$/.test(t.referrer))return t.referrer+'から（広告識別情報なし）';
    return t.referrer?t.referrer+'（外部サイト参照）':'直接アクセス／参照元不明';
  }
  function row(name,t){
    if(!t)return '';
    var lines=[name+'：'+label(t),'日時：'+new Date(t.at).toISOString(),'入口：'+t.landing];
    ['gclid','gbraid','wbraid','utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){if(t[k])lines.push(k+'：'+t[k]);});
    if(t.referrer)lines.push('参照元ドメイン：'+t.referrer);
    return lines.join('\n');
  }
  window.SHIBASUN_ATTRIBUTION={get:function(){return JSON.parse(JSON.stringify(state));},notes:function(){
    var lines=['【流入経路（自動記録・自己申告とは別）】',row('今回の訪問',state.session),row('このブラウザでの初回（30日以内）',state.first)];
    if(state.lastKnown&&state.lastKnown.at!==state.session.at)lines.push(row('直近の識別できた流入（今回の経路とは別）',state.lastKnown));
    return lines.filter(Boolean).join('\n');
  }};
})();
