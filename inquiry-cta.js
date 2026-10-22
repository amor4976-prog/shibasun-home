/* Inquiry links are intermediate actions, never successful inquiries. */
(function(){
  'use strict';
  var seen=Object.create(null);
  function info(a){
    var u;try{u=new URL(a.getAttribute('href'),location.href);}catch(e){return null;}
    var kind;
    if(u.origin===location.origin){
      if(/^\/catalog(?:\.html)?\/?$/.test(u.pathname))kind='catalog';
      else if(/^\/reserve(?:\.html)?\/?$/.test(u.pathname)||u.hash==='#reserve')kind='reserve';
    }else if(u.hostname==='lin.ee'&&u.pathname==='/ueeBddk')kind='line';
    else if(u.protocol==='tel:')kind='phone';
    if(!kind)return null;
    var p=a.closest('[data-inquiry-location]'),where=p?p.getAttribute('data-inquiry-location'):'content';
    if(!p){if(a.closest('header'))where='header';else if(a.closest('.fixed-cta,.float-cta'))where='fixed';else if(a.closest('footer'))where='footer';}
    return {cta_kind:kind,cta_location:where,page_path:location.pathname};
  }
  function track(event,data){if(typeof window.gtag==='function')window.gtag('event',event,data);}
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var d=info(a);if(d)track('inquiry_cta_click',d);},true);
  if(!('IntersectionObserver' in window))return;
  var observer=new IntersectionObserver(function(entries){entries.forEach(function(e){if(!e.isIntersecting)return;var d=info(e.target);if(!d)return;var key=d.cta_kind+':'+d.cta_location;if(!seen[key]){seen[key]=true;track('inquiry_cta_view',d);}observer.unobserve(e.target);});},{threshold:0.5});
  var watched=new WeakSet();
  function watch(root){var links=root.querySelectorAll?Array.from(root.querySelectorAll('a[href]')):[];if(root.matches&&root.matches('a[href]'))links.push(root);links.forEach(function(a){if(!watched.has(a)&&info(a)){watched.add(a);observer.observe(a);}});}
  watch(document);
  new MutationObserver(function(changes){changes.forEach(function(change){change.addedNodes.forEach(watch);});}).observe(document.body,{childList:true,subtree:true});
})();
