/* Layout enhancement only: the existing form owns validation and the single POST. */
(function(){
'use strict';
const app=document.getElementById('rsv-app');if(!app)return;
const standalone=/\/reserve(?:\.html)?\/?$/.test(location.pathname);
let stage=1,renderedForm=null,inView=standalone;
const bar=document.createElement('div');bar.className='booking-bar';bar.setAttribute('role','region');bar.setAttribute('aria-label','予約の操作');bar.hidden=true;
const status=document.createElement('span'),next=document.createElement('button');next.type='button';bar.append(status,next);document.body.append(bar);
function text(el,value){if(el&&el.textContent!==value)el.textContent=value;}
function focusStage(){const heading=app.querySelector(stage===2?'.booking-contact-heading':'.booking-steps');app.querySelector('.booking-steps')?.scrollIntoView({behavior:'smooth',block:'start'});heading?.focus({preventScroll:true});}
function back(){if(rsvSubmitting)return;if(history.state?.shibasunBookingStep===2)history.back();else{stage=1;refresh();focusStage();}}
function enhanceCandidateDates(){
 for(const id of ['k-d1','k-d2']){
  const input=document.getElementById(id);if(!input||input.dataset.monthDayPicker)return;
  input.dataset.monthDayPicker='true';input.type='hidden';
  const control=document.createElement('div');control.className='booking-date-control';input.before(control);control.append(input);
  const toggle=document.createElement('button');toggle.type='button';toggle.className='booking-date-toggle';toggle.setAttribute('aria-label',id==='k-d1'?'第1希望の日付を選ぶ':'第2希望の日付を選ぶ');control.append(toggle);
  const panel=document.createElement('div');panel.className='booking-candidate-calendar';panel.id=id+'-calendar';panel.hidden=true;
  input.closest('.two').after(panel);toggle.setAttribute('aria-controls',panel.id);toggle.setAttribute('aria-expanded','false');
  let start=input.value||input.min;
  const label=()=>{text(toggle,input.value?`${fmtDate(input.value).md}（${fmtDate(input.value).w}）`:'日付を選ぶ');};
  const close=()=>{panel.hidden=true;toggle.setAttribute('aria-expanded','false');};
  function draw(){
   panel.replaceChildren();const nav=document.createElement('div');nav.className='booking-week-nav';
   const prev=document.createElement('button'),range=document.createElement('span'),after=document.createElement('button');prev.type=after.type='button';prev.textContent='‹';after.textContent='›';prev.setAttribute('aria-label','希望日の前の週');after.setAttribute('aria-label','希望日の次の週');prev.disabled=start<=input.min;
   const end=new Date(start+'T00:00:00Z');end.setUTCDate(end.getUTCDate()+6);const last=end.toISOString().slice(0,10);
   // The full ISO date stays in the existing payload; there is no year-selection control.
   range.textContent=fmtDate(start).md+'〜'+fmtDate(last).md;
   nav.append(prev,range,after);panel.append(nav);
   const days=document.createElement('div');days.className='booking-days';
   for(let i=0;i<7;i++){
    const d=new Date(start+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+i);const date=d.toISOString().slice(0,10),f=fmtDate(date);
    const b=document.createElement('button');b.type='button';b.className='date-chip'+(input.value===date?' on':'');b.disabled=date<input.min;b.setAttribute('aria-label',`${id==='k-d1'?'第1希望':'第2希望'} ${f.md} ${f.w}曜日`);b.setAttribute('aria-pressed',String(input.value===date));
    const number=document.createElement('span'),weekday=document.createElement('span');number.className='d';number.textContent=d.getUTCDate();weekday.className='w';weekday.textContent=f.w;b.append(number,weekday);
    b.addEventListener('click',()=>{input.value=date;label();close();input.dispatchEvent(new Event('input',{bubbles:true}));toggle.focus({preventScroll:true});});days.append(b);
   }
   panel.append(days);
   function move(n){const d=new Date(start+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+n*7);start=[d.toISOString().slice(0,10),input.min].sort()[1];draw();panel.querySelector(n<0?'button[aria-label="希望日の前の週"]':'button[aria-label="希望日の次の週"]')?.focus({preventScroll:true});}
   prev.addEventListener('click',()=>move(-1));after.addEventListener('click',()=>move(1));
   const clear=document.createElement('button');clear.type='button';clear.className='booking-edit';clear.textContent=id==='k-d2'?'第2希望を取り消す':'閉じる';clear.addEventListener('click',()=>{if(id==='k-d2'){input.value='';label();input.dispatchEvent(new Event('input',{bubbles:true}));}close();toggle.focus({preventScroll:true});});panel.append(clear);
  }
  toggle.addEventListener('click',()=>{if(!panel.hidden){close();return;}document.querySelectorAll('.booking-candidate-calendar').forEach(el=>el.hidden=true);document.querySelectorAll('.booking-date-toggle').forEach(el=>el.setAttribute('aria-expanded','false'));start=input.value||input.min;panel.hidden=false;toggle.setAttribute('aria-expanded','true');draw();});
  panel.addEventListener('keydown',e=>{if(e.key==='Escape'){close();toggle.focus({preventScroll:true});}});label();
 }
}

function refresh(){
 enhanceCandidateDates();
 const form=app.querySelector('#rsv-form'),chosen=app.querySelector('.slot-btn.on'),done=!!app.querySelector('.rsv-done');
 const candidateOpen=stage===1&&!!document.getElementById('kouho-in')?.classList.contains('open');document.body.classList.toggle('booking-candidate',inView&&candidateOpen);
 bar.hidden=!inView||done||!form||candidateOpen;document.body.classList.toggle('booking-active',!bar.hidden);
 app.classList.toggle('booking-ready',!!form||done||!!app.querySelector('.error'));
 if(!form)return;
 if(form!==renderedForm){
  renderedForm=form;
  const one=document.createElement('div');one.className='booking-stage-one';
  const two=document.createElement('div');two.className='booking-stage-two';
  [...app.childNodes].forEach(node=>{if(node!==form)one.append(node);});
  const steps=document.createElement('div');steps.className='booking-steps';steps.tabIndex=-1;steps.innerHTML='<span data-step="1">1 日時選択</span><span data-step="2">2 連絡先入力</span>';
  app.prepend(steps);app.append(one,two);two.append(form);
  const heading=document.createElement('h2');heading.className='booking-contact-heading';heading.tabIndex=-1;heading.textContent='連絡先を入力する';
  const backButton=document.createElement('button');backButton.type='button';backButton.className='booking-back';backButton.textContent='‹ 日時選択に戻る';backButton.addEventListener('click',back);
  two.prepend(backButton,heading);
  const edit=document.createElement('button');edit.type='button';edit.className='booking-edit';edit.textContent='日時を変更する';edit.addEventListener('click',back);form.querySelector('.rsv-selection')?.after(edit);
  // Keep the existing method controls and field nodes so restoration and listeners remain intact.
  const method=form.querySelector('.method-chips')?.closest('.rsv-field');if(method){form.querySelector('.rsv-field')?.before(method);method.querySelectorAll('.mchip').forEach(b=>{text(b,b.dataset.m==='online'?'オンライン':'来店');b.setAttribute('aria-pressed',String(b.classList.contains('on')));});}
  const contactLabel=form.querySelector('.rsv-step-label');if(contactLabel)contactLabel.hidden=true;
  const email=form.querySelector('#rsv-email');if(email){const hint=document.createElement('p');hint.className='booking-email-note';hint.textContent='入力いただくと、確認メールをお送りします。';email.after(hint);}
  one.querySelectorAll('.slot-btn').forEach(b=>{b.setAttribute('aria-pressed',String(b.classList.contains('on')));});
 }
 if(!chosen)stage=1;
 app.dataset.bookingStage=String(stage);
 const one=app.querySelector('.booking-stage-one'),two=app.querySelector('.booking-stage-two');one.hidden=stage!==1;two.hidden=stage!==2;
 app.querySelectorAll('[data-step]').forEach(el=>el.setAttribute('aria-current',Number(el.dataset.step)===stage?'step':'false'));
 const busy=!!form.querySelector('.rsv-submit:disabled');
 text(status,chosen?(form.querySelector('.rsv-selection')?.textContent||'日時を選択済み'):'時間を選んでください。');
 text(next,busy?'送信中…':stage===1?'連絡先の入力へ':'この日時で予約を申し込む');
 next.disabled=busy||!chosen;
 app.querySelectorAll('.booking-back,.booking-edit,[data-week]').forEach(el=>{if(el.matches('[data-week]')){const d=el.dataset.week==='-1'?rsvWeekStart<=rsvMonday(rsvFirstVisibleDate()):(()=>{const x=new Date(rsvWeekStart+'T00:00:00Z');x.setUTCDate(x.getUTCDate()+6);return x.toISOString().slice(0,10)>=rsvLastVisibleDate();})();if(el.disabled!==(busy||d))el.disabled=busy||d;}else if(el.disabled!==busy)el.disabled=busy;});
 const original=form.querySelector('.rsv-submit');if(original&&!busy)text(original,'この日時で予約を申し込む');
}
next.addEventListener('click',()=>{
 if(next.disabled||rsvSubmitting)return;
 if(stage===1){stage=2;history.pushState({...history.state,shibasunBookingStep:2},'',location.href);rsvTrack('contact_step');refresh();focusStage();}
 else app.querySelector('.rsv-submit')?.click();
});
window.addEventListener('popstate',()=>{if(rsvSubmitting)return;stage=history.state?.shibasunBookingStep===2?2:1;refresh();focusStage();});
app.addEventListener('click',()=>requestAnimationFrame(refresh));
new MutationObserver(refresh).observe(app,{childList:true,subtree:true,attributes:true,attributeFilter:['disabled']});
if(!standalone)new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;refresh();},{threshold:0}).observe(app);
refresh();
})();
