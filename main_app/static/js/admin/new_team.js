const formEl = document.getElementById("adminForm")

function validateForm() {
    const teamName = document.forms["adminForm"]["team_name"].value.trim()
    const shortcode = document.forms["adminForm"]["shortcode"].value.trim()
    const crestUrl = document.forms["adminForm"]["crest_url"].value.trim()

    if (teamName == "" || shortcode == "" || crestUrl == ""){
        addMessage("Inputs not complete")
        return false;
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}
