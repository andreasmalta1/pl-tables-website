const formEl = document.getElementById("adminForm")
const endDateEl = document.getElementById("endDate")

function validateForm() {
    const stint = document.forms["adminForm"]["stint"].value
    const endDate = document.forms["adminForm"]["end-date"].value

    if (stint == "" || endDate == ""){
        addMessage("Inputs not complete")
        return false;
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}

let today = new Date();
let todayFormatted = today.toISOString().split('T')[0];

endDateEl.value = todayFormatted;
