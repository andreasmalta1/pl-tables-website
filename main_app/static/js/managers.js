const currentTitleEl = document.getElementById("current-manager")
const currentFormEl = document.getElementById("current-form")

const memorableTitleEl = document.getElementById("memorable-manager")
const memorableFormEl = document.getElementById("memorable-form")

currentTitleEl.addEventListener('click', () => {
    currentFormEl.classList.toggle("form-hidden")
})

memorableTitleEl.addEventListener('click', () => {
    memorableFormEl.classList.toggle("form-hidden")
})