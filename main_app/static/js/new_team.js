const formEl = document.getElementById("adminForm")

function validateForm() {
    const teamName = document.forms["adminForm"]["team_name"].value.trim()
    const shortcode = document.forms["adminForm"]["shortcode"].value.trim()
    const crest_url = document.forms["adminForm"]["crest_url"].value.trim()

    if (teamName == "" || shortcode == "" || crest_url == ""){
        console.log("Invalid inputs")
        return false;
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}
