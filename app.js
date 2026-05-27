let eventi=[];
let current=new Date();
let editId=null;

/* LOAD */
async function load(){
eventi=await fetch("/eventi").then(r=>r.json());
render();
}

/* MONTH */
function nextMonth(){current.setMonth(current.getMonth()+1);render();}
function prevMonth(){current.setMonth(current.getMonth()-1);render();}

/* FIX DATE ISO */
function iso(d){
return d.getFullYear()+"-"+
String(d.getMonth()+1).padStart(2,"0")+"-"+
String(d.getDate()).padStart(2,"0");
}

/* RENDER */
function render(){

const c=document.getElementById("calendar");
c.innerHTML="";

document.getElementById("month").innerText=
current.toLocaleString("it-IT",{month:"long",year:"numeric"});

let y=current.getFullYear();
let m=current.getMonth();

let first=new Date(y,m,1);
let startDay=first.getDay();
let days=new Date(y,m+1,0).getDate();

/* empty */
for(let i=0;i<startDay;i++){
c.appendChild(document.createElement("div"));
}

/* days */
for(let d=1;d<=days;d++){

let date=new Date(y,m,d);
let dayIso=iso(date);

let cell=document.createElement("div");
cell.className="cell";

cell.innerHTML=`<b>${d}</b>`;

/* TODAY */
if(new Date().toDateString()===date.toDateString()){
cell.classList.add("today");
}

/* EVENTS */
eventi.forEach(e=>{
if(dayIso>=e.data_inizio && dayIso<=e.data_fine){

let ev=document.createElement("div");
ev.className="event";

ev.innerText=e.tipo; // 🔴 RIPRISTINO TIPO SEMPRE VISIBILE

ev.ondblclick=()=>open(e);

cell.appendChild(ev);
}
});

/* DROP */
cell.ondragover=e=>e.preventDefault();
cell.ondrop=()=>drop(dayIso);

c.appendChild(cell);
}
}

/* ADD */
async function add(){

await fetch("/aggiungi",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
tipo:tipo.value,
data_inizio:d1.value,
data_fine:d2.value,
descrizione:desc.value
})
});

load();
}

/* OPEN */
function open(e){
editId=e.id;

p_tipo.value=e.tipo;
p_d1.value=e.data_inizio;
p_d2.value=e.data_fine;
p_desc.value=e.descrizione||"";

modal.style.display="flex";
}

/* SAVE */
async function save(){

await fetch("/update/"+editId,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
tipo:p_tipo.value,
data_inizio:p_d1.value,
data_fine:p_d2.value,
descrizione:p_desc.value
})
});

modal.style.display="none";
load();
}

function closeM(){
modal.style.display="none";
}

/* INIT */
window.onload=load;