const menuBtn = document.querySelector(".hamburger")
const mobileMenu = document.getElementById("mobileNav")


menuBtn.addEventListener("click", () => {
    menuBtn.classList.toggle("isActive")
    mobileMenu.classList.toggle("isActive")
})