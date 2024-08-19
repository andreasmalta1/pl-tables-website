const formEl = document.getElementById("adminForm")

function validateForm() {
    const team = document.forms["adminForm"]["team"]
    const pointsDeducted = document.forms["adminForm"]["points-deducted"].value.trim()
    const reason = document.forms["adminForm"]["reason"].value
    const season = document.forms["adminForm"]["season"].value

    if (team == "" || pointsDeducted == "" || reason == "" || season == ""){
        addMessage("Inputs not complete")
        return false;
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}
