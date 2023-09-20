// $(document).ready(function(){
//     $('#menu').click(function(){
//         $(this).toggleClass('fa-times');
//        $('.navbar').toggleClass('nav-toggle');
//     });
// });

const menu = document.getElementById('menu-btn')
const navbar = document.getElementById('navbar')

menu.addEventListener('click',()=>{
    console.log('clicked')
    navbar.classList.toggle('show')
})