const titleEl = document.getElementById("seasons-title")
const formEl = document.getElementById("seasons-form")

titleEl.addEventListener('click', () => {
    formEl.classList.toggle("form-hidden")
})