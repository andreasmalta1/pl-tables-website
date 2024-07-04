const formEl = document.getElementById("adminForm")

function validateForm() {
    const nationName = document.forms["adminForm"]["nation_name"].value.trim()
    const shortcode = document.forms["adminForm"]["shortcode"].value.trim()
    const flagUrl = document.forms["adminForm"]["flag_url"].value.trim()

    if (nationName == "" || shortcode == "" || flagUrl == ""){
        console.log("Invalid inputs")
        return false;
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}
