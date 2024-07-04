const formEl = document.getElementById("adminForm")
const startDate = document.getElementById("startDate")
const endDate = document.getElementById("endDate")
const checkbox = document.getElementById("current")

function validateForm() {
    const manager = document.forms["adminForm"]["manager"].value
    const team = document.forms["adminForm"]["team"].value
    const startDate = document.forms["adminForm"]["start-date"].value

    if (manager == "" || team == "" || startDate == ""){
        console.log("Invalid inputs")
        return false;
    }
}

if (checkbox != null){
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            endDate.disabled = true;
            startDate.value = todayFormatted;
            endDate.value = "";
        } else {
            endDate.disabled = false;
            startDate.value = lastWeekFormatted;
            endDate.value = todayFormatted;
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

if (checkbox != null){
    checkbox.checked = true;
    startDate.value = todayFormatted;
    endDate.disabled = true;
}

