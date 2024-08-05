const menuBtn = document.querySelector(".hamburger")
const mobileMenu = document.getElementById("mobileNav")


menuBtn.addEventListener("click", () => {
    menuBtn.classList.toggle("is-active")
    mobileMenu.classList.toggle("is-active")
})