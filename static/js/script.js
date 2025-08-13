let navbar = document.querySelector('.header .navbar');
document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.add('active');
}
document.querySelector('#nav-close').onclick = () =>{
    navbar.classList.remove('active');
}

let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.add('active');
}

document.querySelector('#close-search').onclick = () =>{
    searchForm.classList.remove('active');
}
window.onscroll=()=>{
    navbar.classList.remove('active');
    if(window.scrollY>0){
        document.querySelector('.header').classList.add('active');
    }else{
        document.querySelector('.header').classList.remove('active');
    }
};
window.onload=()=>{
    if(window.scrollY>0){
        document.querySelector('.header').classList.add('active');
    }else{
        document.querySelector('.header').classList.remove('active');
    }
};

function form_submited()
{
    alert("Your Message sended to E-vakeel ");
}
function message_delete()
{
    alert("Your Message is deleted");
}
function member_added()
{
    alert("New Member is added");
}
function update_member()
{
    alert("Your Member is Updated");
}
function delete_member()
{
    alert("Your Member is deleted!!!");
}
function popup_add()
{
    document.getElementById("pop_back_before").classList.toggle("pop_back")
    document.getElementById("add_member_pop_before").classList.toggle("add_member_pop")
    document.getElementById("add_member_pop_back_before").classList.toggle("add_member_pop_back")
   
}
function popup_update()
{
    document.getElementById("pop_back_before").classList.toggle("pop_back")
    document.getElementById("update_member_pop_before").classList.toggle("update_member_pop")
    document.getElementById("update_pop_back_before").classList.toggle("update_pop_back")
   
}
function popup_appointment()
{
    document.getElementById("pop_back_before").classList.toggle("pop_back")
    document.getElementById("add_appointment_pop_before").classList.toggle("add_appointment_pop")
    document.getElementById("add_appointment_pop_back_before").classList.toggle("add_appointment_pop_back")
}
function pop_bookapt()
{
    document.getElementById("pop_back_before").classList.toggle("pop_back")
    document.getElementById("apt_pop_body_before").classList.toggle("apt_pop_body")
    document.getElementById("apt_pop_before").classList.toggle("apt_pop")
}
function notiPop()
{
    document.getElementById("pop_back_before").classList.toggle("pop_back")
    document.getElementById("popbody_notification_before").classList.toggle("popbody_notification")
}


var loader = document.getElementById("preloader");

window.addEventListener("load",function(){
    loader.style.display="none";
})