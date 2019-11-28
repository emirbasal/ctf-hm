var navItems = document.getElementsByClassName('nav-item');

Array.from(navItems).forEach((navItem) => {
    navItem.addEventListener('click', function(){
        navItem.classList.add('active');
    });
});
