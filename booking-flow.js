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
function refresh(){
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
