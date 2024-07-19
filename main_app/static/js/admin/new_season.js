const formEl = document.getElementById("adminForm")
const relegatedTeamsEl = document.getElementById("relegatedTeams")
const promotedTeamsEl = document.getElementById("promotedTeams")

function validateForm() {
    const nationName = document.forms["adminForm"]["nation_name"].value.trim()
    const shortcode = document.forms["adminForm"]["shortcode"].value.trim()
    const flagUrl = document.forms["adminForm"]["flag_url"].value.trim()

    if (nationName == "" || shortcode == "" || flagUrl == ""){
        addMessage("Inputs not complete")
        return false;
    }
}


if (formEl !== null){
    const numOptionsRelegated = relegatedTeamsEl.options.length;
    const numOptionsPromoted = promotedTeamsEl.options.length;
    relegatedTeamsEl.size = numOptionsRelegated;
    promotedTeamsEl.size = numOptionsPromoted;
    formEl.onsubmit = validateForm
}
 