const formEl = document.getElementById("adminForm")

function validateForm() {
    const managerName = document.forms["adminForm"]["manager_name"].value.trim()
    const faceUrl = document.forms["adminForm"]["face_url"].value.trim()
    const nation = document.forms["adminForm"]["nation"].value

    if (managerName == "" || faceUrl == "" || nation == ""){
        addMessage("Inputs not complete")
        return false;
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}
