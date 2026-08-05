
let addBtn = document.getElementById("add-btn");
let modal = document.getElementById("add-modal");
let overlay = document.getElementById("overlay");
let closeBtn = document.getElementById("close-btn");
let okBtn = document.getElementById("ok-btn");

let Scroll = document.getElementById("scroll");

document.querySelectorAll(".delete-btn")
.forEach(btn=>{
    btn.addEventListener("click",(e)=>{
        e.preventDefault();
        e.stopPropagation();
        let card = btn.closest(".word-card");
        let id = card.dataset.id;
        if(confirm("确定删除这个词条吗？")){
            deleteWord(id, card);
        }
    });
});
// let btnList = [addBtn];

// btnList.forEach(element => {
//     if(element){
//         element.addEventListener("click", ()=>{
//             Navi(element);
//         })
//     }
// })

function deleteWord(id, card){
    fetch(`/delete/${id}`,{
        method:"POST"
    })
    .then(res=>{
        if(res.ok){
            // 删除页面上的卡片
            card.remove();
        }
    });
}
addBtn?.addEventListener("click", modalApp)
closeBtn?.addEventListener("click", modalDisapp)

function modalDisapp(){
    overlay?.classList.remove("show");
    modal?.classList.remove("show");
    modal?.classList.add("close");
    closeBtn?.classList.remove("show");
    Scroll?.classList.remove("no-scroll");

    addBtn?.classList.remove("disapp");

}

function modalApp(){
    overlay?.classList.add("show");
    modal?.classList.add("show");
    modal?.classList.remove("close");
    closeBtn?.classList.add("show");
    Scroll?.classList.add("no-scroll");

    addBtn?.classList.add("disapp");
}


function removeClasses(classname, elements){
    elements.forEach(element => {element?.classList.remove(classname);})
}

function Navi(btnname){
    removeClasses("active", [homeBtn, addBtn, editBtn]);
    btnname?.classList.add("active");
}

function updateTime(){
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth()+1).padStart(2,'0');
    const day = String(now.getDate()).padStart(2,'0');
    const hour = String(now.getHours()).padStart(2,'0');
    const minute = String(now.getMinutes()).padStart(2,'0');
    const second = String(now.getSeconds()).padStart(2,'0');

    document.getElementById("time").innerHTML =
        `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}
updateTime();
setInterval(updateTime,500);

document.documentElement.style.setProperty("--screen-height", window.innerHeight+"px");