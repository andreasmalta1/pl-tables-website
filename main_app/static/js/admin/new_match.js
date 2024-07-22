const formEl = document.getElementById("adminForm")
const matchesDiv = document.getElementById("matches")
const addMatchBtn = document.getElementById("addMatch")
const selectElement = document.querySelector('[name=home-team]');
const matchDateInput = document.getElementById("matchDate")
const options = selectElement.options;
const teamOptions = [];
const today = new Date().toISOString().split('T')[0];

for (let i = 0; i < options.length; i++) {
    teamOptions.push({
        value: options[i].value,
        text: options[i].text
    });
}

let matchNum = 2;

function validateForm() {

    const homeTeams = []
    const homeScores = []
    const awayTeams = []
    const awayScores = []
    const matchDates = []

    document.querySelectorAll('select[name="home-team"]').forEach(input => {
        homeTeams.push(input.value);
    });

    document.querySelectorAll('input[name="home-score"]').forEach(input => {
        homeScores.push(input.value);
    });

    document.querySelectorAll('select[name="away-team"]').forEach(input => {
        awayTeams.push(input.value);
    });

    document.querySelectorAll('input[name="away-score"]').forEach(input => {
        awayScores.push(input.value);
    });

    document.querySelectorAll('input[name="match-date"]').forEach(input => {
        matchDates.push(input.value);
    });

    for (let i = 0; i < homeTeams.length; i++) {
        if (homeTeams[i] == "" || homeScores[i] == "" || awayTeams[i] == "" || homeScores[i] == "" || matchDates[i] == ""){
            addMessage("Inputs not complete")
            return false;
        }

        if (homeTeams[i] == awayTeams[i]){
            addMessage("Home & Away Teams cannot be the same for the same match")
            return false;
        }

        if (matchDates[i] > today) {
            addMessage("Match Date cannot be in the future")
            return false;
        }
    }
}

if (formEl !== null){
    formEl.onsubmit = validateForm
}

matchDateInput.value = today;
matchDateInput.max = today;

addMatchBtn.addEventListener("click", () => {
    const matchDiv = document.createElement("div")
    matchDiv.className = "matchInput"

    const matchTitle = document.createElement("h1")
    matchTitle.textContent = `Match ${matchNum}:`
    matchNum ++

    matchDiv.appendChild(matchTitle)

    const homeTeamFieldDiv = document.createElement("div")
    homeTeamFieldDiv.className = "field"

    const homeTeamControlDiv = document.createElement("div")
    homeTeamControlDiv.className = "control"

    let breakLine = document.createElement("br")

    const homeTeamNameLabel = document.createElement("label")
    homeTeamNameLabel.htmlFor = "home-team"
    homeTeamNameLabel.textContent = "Home Team: "

    const homeTeamSelectEl = document.createElement("select")
    homeTeamSelectEl.name = "home-team"

    teamOptions.forEach(option => {
        const newOption = document.createElement('option');
        newOption.value = option.value;
        newOption.text = option.text;
        homeTeamSelectEl.appendChild(newOption);
    });

    homeTeamControlDiv.appendChild(homeTeamNameLabel)
    homeTeamControlDiv.appendChild(breakLine)
    homeTeamControlDiv.appendChild(homeTeamSelectEl)
    homeTeamFieldDiv.appendChild(homeTeamControlDiv)
    matchDiv.appendChild(homeTeamFieldDiv)
    
    const homeScoreFieldDiv = document.createElement("div")
    homeScoreFieldDiv.className = "field"

    const homeScoreControlDiv = document.createElement("div")
    homeScoreControlDiv.className = "control"

    const homeScoreLabel = document.createElement("label")
    homeScoreLabel.htmlFor = "home-score"
    homeScoreLabel.textContent = "Home Score: "

    const homeScoreInput = document.createElement("input")
    homeScoreInput.type = "number"
    homeScoreInput.name = "home-score"
    homeScoreInput.value = "0"
    homeScoreInput.min = "0"
    homeScoreInput.max = "15"

    homeScoreControlDiv.appendChild(homeScoreLabel)
    homeScoreControlDiv.appendChild(homeScoreInput)
    homeScoreFieldDiv.appendChild(homeScoreControlDiv)
    matchDiv.appendChild(homeScoreFieldDiv)

    const awayTeamFieldDiv = document.createElement("div")
    awayTeamFieldDiv.className = "field"

    const awayTeamControlDiv = document.createElement("div")
    awayTeamControlDiv.className = "control"

    breakLine = document.createElement("br")

    const awayTeamNameLabel = document.createElement("label")
    awayTeamNameLabel.htmlFor = "away-team"
    awayTeamNameLabel.textContent = "Away Team: "

    const awayTeamSelectEl = document.createElement("select")
    awayTeamSelectEl.name = "away-team"

    teamOptions.forEach(option => {
        const newOption = document.createElement('option');
        newOption.value = option.value;
        newOption.text = option.text;
        awayTeamSelectEl.appendChild(newOption);
    });

    awayTeamControlDiv.appendChild(awayTeamNameLabel)
    awayTeamControlDiv.appendChild(breakLine)
    awayTeamControlDiv.appendChild(awayTeamSelectEl)
    awayTeamFieldDiv.appendChild(awayTeamControlDiv)
    matchDiv.appendChild(awayTeamFieldDiv)
    
    const awayScoreFieldDiv = document.createElement("div")
    awayScoreFieldDiv.className = "field"

    const awayScoreControlDiv = document.createElement("div")
    homeScoreControlDiv.className = "control"

    const awayScoreLabel = document.createElement("label")
    awayScoreLabel.htmlFor = "away-score"
    awayScoreLabel.textContent = "Away Score: "

    const awayScoreInput = document.createElement("input")
    awayScoreInput.type = "number"
    awayScoreInput.name = "away-score"
    awayScoreInput.value = "0"
    awayScoreInput.min = "0"
    awayScoreInput.max = "15"

    awayScoreControlDiv.appendChild(awayScoreLabel)
    awayScoreControlDiv.appendChild(awayScoreInput)
    awayScoreFieldDiv.appendChild(awayScoreControlDiv)
    matchDiv.appendChild(awayScoreFieldDiv)

    const dateFieldDiv = document.createElement("div")
    dateFieldDiv.className = "field"

    const dateControlDiv = document.createElement("div")
    dateControlDiv.className = "control"

    const dateLabel = document.createElement("label")
    dateLabel.htmlFor = "match-date"
    dateLabel.textContent = "Date: "

    const dateInput = document.createElement("input")
    dateInput.type = "date"
    dateInput.name = "match-date"
    dateInput.value = today;
    dateInput.max = today;

    dateControlDiv.appendChild(dateLabel)
    dateControlDiv.appendChild(dateInput)
    dateFieldDiv.appendChild(dateControlDiv)
    matchDiv.appendChild(dateFieldDiv)
    
    matchesDiv.appendChild(matchDiv)
})

