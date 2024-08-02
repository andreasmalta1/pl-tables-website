const menuBtn = document.querySelector(".hamburger")
const mobileMenu = document.querySelector(".mobile-nav")
const footerContainer = document.querySelector(".footer-container")


menuBtn.addEventListener("click", () => {
    menuBtn.classList.toggle("is-active")
    mobileMenu.classList.toggle("is-active")
    footerContainer.classList.toggle("is-active")
})