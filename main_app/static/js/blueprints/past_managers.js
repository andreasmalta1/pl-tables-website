const stintsUrl = `${SCRIPT_ROOT}/api/stints`
const managerUrl = `${SCRIPT_ROOT}/api/managers`

const managersTable = document.getElementById("managersTable")
const managersTableBody = managersTable.getElementsByTagName('tbody')[0]
const managersRows = Array.from(managersTableBody.getElementsByTagName('tr'))
const managerBtns = document.querySelectorAll('#genBtn')
const tableDiv = document.getElementById('standings')
const managerProfileDiv = document.getElementById('managerProfile')
const managersDiv = document.getElementById('managersTableDiv')
const toggleArrowBtn = document.getElementById('toggleArrowBtn')
const toggleArrowCard = document.getElementById('toggleArrowCard')

let table;

function daysDifference(startDateString, endDateString) {
    const startDate = new Date(startDateString);
    const endDate = new Date(endDateString);
    const timeDifference = endDate - startDate;
    const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    return daysDifference;
}

const memorableDaysElapsed = managersRows.map(row => {
    const startDateCell = row.cells[4];
    const startDateString = startDateCell.textContent.trim();
    const endDateCell = row.cells[5];
    const endDateString = endDateCell.textContent.trim();
    const daysElapsedValue = daysDifference(startDateString, endDateString);
    const daysElapsedCell = row.cells[6];
    daysElapsedCell.textContent = daysElapsedValue;
    return { row, daysElapsedValue };
});

memorableDaysElapsed.sort((a, b) => b.daysElapsedValue - a.daysElapsedValue);
managersTableBody.innerHTML = '';
memorableDaysElapsed.forEach(({ row }) => {
    managersTableBody.appendChild(row);
})

function hideManagers(){
    if (!managersDiv.classList.contains('hidden')) {
        managersDiv.classList.add('hidden');
    }
    managerProfileDiv.classList.remove('hidden');
}

function createManagerCard(data){
   managerProfileDiv.innerHTML = '';

    let managerNameDiv = document.createElement("div")
    managerNameDiv.className = "managerNameCard"

    let managerTitle = document.createElement('h1');
    managerTitle.textContent = data.name
    managerTitle.className = "managerTitle"

    let managerFace = document.createElement('img');
    managerFace.src = data.face_url
    managerFace.className = "managerFaceCard"

    managerNameDiv.appendChild(managerTitle)
    managerNameDiv.appendChild(managerFace)

    let managerNationDiv = document.createElement("div")
    managerNationDiv.className = "managerNationCard"

    let managerNation = document.createElement('h1');
    managerNation.textContent = data.nation_name
    managerNation.className = "managerNation"

    let nationFlag = document.createElement('img');
    nationFlag.src = data.nation_flag_url
    nationFlag.className = "nationFlag"

    managerNationDiv.appendChild(managerNation)
    managerNationDiv.appendChild(nationFlag)

    let managerTeamDiv = document.createElement("div")
    managerTeamDiv.className = "managerTeamCard"

    let managerTeam = document.createElement('h1');
    managerTeam.textContent = data.team_name
    managerTeam.className = "managerTeam"

    let teamCrest = document.createElement('img');
    teamCrest.src = data.team_crest_url
    teamCrest.className = "managerTeamImg"

    managerTeamDiv.appendChild(managerTeam)
    managerTeamDiv.appendChild(teamCrest)

    let managerStart = document.createElement('p');
    managerStart.textContent = `Start Day: ${data.date_start}`
    managerStart.className = "managerStart"

    let managerEnd = document.createElement('p');
    managerEnd.textContent = `End Day: ${data.date_end}`
    managerEnd.className = "managerEnd"

    let daysElapsedValue = daysDifference(data.date_start, data.date_end);
    let managerDays = document.createElement('p');
    managerDays.textContent = `Days in Charge: ${daysElapsedValue}`
    managerDays.className = "managerDays"

    let toggleCard = document.createElement("div");
    toggleCard.id = "toggleArrowCard"
    toggleCard.classList.add("toggleArrow")
    toggleCard.classList.add("toggleCard")
    toggleCard.innerHTML = "&#x25B6; <span class='arrowText'> Change Managerial Stint</span>"
    toggleCard.addEventListener('click', () => {
        managersDiv.classList.remove('hidden');
        managerProfileDiv.classList.add('hidden')
    })

    managerProfileDiv.appendChild(managerNameDiv)
    managerProfileDiv.appendChild(managerNationDiv)
    managerProfileDiv.appendChild(managerTeamDiv)
    managerProfileDiv.appendChild(managerStart)
    managerProfileDiv.appendChild(managerStart)
    managerProfileDiv.appendChild(managerEnd)
    managerProfileDiv.appendChild(toggleCard)
}

managerBtns.forEach(btn => {
    btn.addEventListener('click', async function() {
        let stintId = btn.name;
        const response = await fetch(`${stintsUrl}/${stintId}`)
        .then(response => response.json())
        .then(data => {
            if(Object.keys(data).length === 0 && data.constructor === Object){
                noMatches("No matches played in these dates. Please choose a different stint")
                return;
            }
            table = createTable(data)
            sortTable(table, 0)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
        fetch(`${managerUrl}/${stintId}`)
        .then(response => response.json())
        .then(data => {
            hideManagers()
            createManagerCard(data)
            highlightTeam(table, data)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});

toggleArrowBtn.addEventListener('click', () => {
    managerProfileDiv.classList.remove('hidden');
    managersDiv.classList.add('hidden')
})

toggleArrowCard.addEventListener('click', () => {
    managersDiv.classList.remove('hidden');
    managerProfileDiv.classList.add('hidden')
})