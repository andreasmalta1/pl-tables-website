const formEl = document.getElementById("adminForm")
const startDateEl = document.getElementById("startDate")
const endDateEl = document.getElementById("endDate")
const checkboxEl = document.getElementById("current")

function validateForm() {
    const manager = document.forms["adminForm"]["manager"].value
    const team = document.forms["adminForm"]["team"].value
    const startDate = document.forms["adminForm"]["start-date"].value
    const endDate = document.forms["adminForm"]["end-date"].value

    if (manager == "" || team == "" || startDate == ""){
        addMessage("Inputs not complete")
        return false;
    }

    if (!checkboxEl.checked){
        if (endDate < startDate){
            addMessage("End date must be after start date")
            return false;
        }
    }
}

if (checkboxEl != null){
    checkboxEl.addEventListener('change', function() {
        if (this.checked) {
            endDateEl.disabled = true;
            startDateEl.value = todayFormatted;
            endDateEl.value = "";
        } else {
            endDateEl.disabled = false;
            startDateEl.value = lastWeekFormatted;
            endDateEl.value = todayFormatted;
        }
    });
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}

let today = new Date();
let todayFormatted = today.toISOString().split('T')[0];

let lastWeek = new Date();
lastWeek.setDate(today.getDate() - 7);
let lastWeekFormatted = lastWeek.toISOString().split('T')[0];

if (checkboxEl != null){
    checkboxEl.checked = true;
    startDateEl.value = todayFormatted;
    endDateEl.disabled = true;
}

