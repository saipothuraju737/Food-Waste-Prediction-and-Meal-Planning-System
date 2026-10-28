const $=s=>document.querySelector(s),DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];let MENU={};
const post=(u,b)=>fetch(u,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}).then(r=>r.json());
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{document.querySelectorAll("nav button").forEach(x=>x.classList.remove("on"));b.classList.add("on");
 document.querySelectorAll(".tab").forEach(t=>t.classList.add("hide"));$("#"+b.dataset.t).classList.remove("hide")});
function fill(){const d=new Date($("#date").value+"T00:00"),m=MENU[DAYS[(d.getDay()+6)%7]][$("#meal").value];
 $("#menu").textContent=DAYS[(d.getDay()+6)%7]+": "+m.menu;$("#special").value=m.special;$("#nonveg").checked=!!m.nonveg;$("#dessert").checked=!!m.dessert}
async function init(){MENU=await(await fetch("/api/menu")).json();const t=new Date(Date.now()+864e5).toISOString().slice(0,10);$("#date").value=$("#ldate").value=t;fill();
 $("#date").onchange=$("#meal").onchange=fill;loadModels();loadStats()}
async function loadModels(){const r=await(await fetch("/api/metrics")).json();const mx=Math.max(...r.metrics.map(m=>m.mae));
 $("#model").innerHTML=`<option value="">Best (${r.best})</option>`+r.metrics.map(m=>`<option>${m.model}</option>`).join("");
 $("#mt").innerHTML="<tr><th>Model</th><th>MAE</th><th>RMSE</th><th>R²</th><th></th></tr>"+r.metrics.map(m=>`<tr><td>${m.model}${m.model==r.best?" 🏆":""}</td><td>${m.mae}</td><td>${m.rmse}</td><td>${m.r2}</td><td style="width:30%"><div class="bar" style="width:${m.mae/mx*100}%"></div></td></tr>`).join("");
 const b=r.backtest;$("#bt").innerHTML=`<h3>Back-test (${b.test_rows} meals, trained on ${r.rows} records)</h3><p>Average prepared now: <b>${b.avg_prepared_now}</b> → suggested: <b>${b.avg_prepared_suggested}</b><br>Average leftover meals now: <b>${b.avg_leftover_now}</b> → suggested: <b>${b.avg_leftover_suggested}</b><br>Meals where suggestion would fall short: <b>${b.shortfall_pct}%</b></p><p class="muted">${b.note}</p>`}
async function loadStats(){const s=await(await fetch("/api/stats")).json();
 $("#st").innerHTML="<tr><th>Day</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr>"+DAYS.map(d=>`<tr><td>${d}</td>`+["breakfast","lunch","dinner"].map(m=>`<td>${s[d][m]}</td>`).join("")+"</tr>").join("")}
$("#go").onclick=async()=>{const r=await post("/api/predict",{date:$("#date").value,meal:$("#meal").value,special:$("#special").value,nonveg:+$("#nonveg").checked,dessert:+$("#dessert").checked,exam:+$("#exam").checked,festival:+$("#festival").checked,model:$("#model").value,current:$("#current").value});
 $("#result").innerHTML=`<h2>${r.day} · ${$("#meal").value}</h2><div class="big"><div class="kpi"><b>${r.predicted}</b>expected students</div><div class="kpi hl"><b>${r.suggested}</b>cook for (with safety margin)</div></div>
 <p>Currently cooking for <b>${r.current}</b> → about <b>${r.extra_now}</b> extra meals (~${r.kg_avoidable} kg) could be avoided <span class="muted">(estimate; measure in the pilot week)</span>.</p>
 <h3>All models</h3><table>${Object.entries(r.all).map(([k,v])=>`<tr><td>${k}</td><td>${v}</td></tr>`).join("")}</table>`};
$("#lgo").onclick=async()=>{$("#lmsg").textContent="Saving & retraining…";const r=await post("/api/log",{date:$("#ldate").value,meal:$("#lmeal").value,prepared:$("#lprep").value,served:$("#lserved").value,leftover_kg:$("#lkg").value,exam:+$("#lexam").checked,festival:+$("#lfest").checked});
 $("#lmsg").textContent=r.ok?`Saved. ${r.rows} records, best model: ${r.best}`:"Error";loadModels();loadStats()};
init();
