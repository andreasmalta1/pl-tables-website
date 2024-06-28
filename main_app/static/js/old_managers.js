const stintsUrl = `${SCRIPT_ROOT}/api/stints`
const managerUrl = `${SCRIPT_ROOT}/api/managers`

const managersTable = document.getElementById("memorableManagers")
const managersTableBody = managersTable.getElementsByTagName('tbody')[0];
const managersRows = Array.from(managersTableBody.getElementsByTagName('tr'));
const managerBtns = document.querySelectorAll('.down-button');
const tableDiv = document.getElementById('standings')
const managerProfileDiv = document.getElementById('managerProfile')
const managersDiv = document.getElementById('oldManagersDiv')

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
}

function createManagerCard(data){
    managerProfileDiv.innerHTML = '';

    let breakLine = document.createElement("br")

    let managerTitle = document.createElement('h1');
    managerTitle.textContent = data.name

    let managerFace = document.createElement('img');
    managerFace.src = data.face_url
    managerFace.style.width = '30px';

    let managerNation = document.createElement('h1');
    managerNation.textContent = data.nation_name

    let nationFlag = document.createElement('img');
    nationFlag.src = data.nation_flag_url
    nationFlag.style.width = '30px';

    let managerTeam = document.createElement('h1');
    managerTeam.textContent = data.team_name

    let teamCrest = document.createElement('img');
    teamCrest.src = data.team_crest_url
    teamCrest.style.width = '30px';

    let managerStart = document.createElement('p');
    managerStart.textContent = `Manager Start: ${data.date_start}`

    let managerEnd = document.createElement('p');
    managerEnd.textContent = `Manager End: ${data.date_end}`

    let daysElapsedValue = daysDifference(data.date_start, data.date_end);
    let managerDays = document.createElement('p');
    managerDays.textContent = daysElapsedValue


    managerProfileDiv.appendChild(managerTitle)
    managerProfileDiv.appendChild(managerFace)
    managerProfileDiv.appendChild(managerNation)
    managerProfileDiv.appendChild(nationFlag)
    managerProfileDiv.appendChild(managerTeam)
    managerProfileDiv.appendChild(teamCrest)
    managerProfileDiv.appendChild(breakLine)
    managerProfileDiv.appendChild(managerStart)
    managerProfileDiv.appendChild(breakLine)
    managerProfileDiv.appendChild(managerEnd)
    managerProfileDiv.appendChild(breakLine)
    managerProfileDiv.appendChild(managerDays)
}

managerBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        let stintId = btn.name;
        fetch(`${stintsUrl}/${stintId}`)
        .then(response => response.json())
        .then(data => {
            table = createTable(data)
            sortTable(table, 0)
            hideManagers()
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
        fetch(`${managerUrl}/${stintId}`)
        .then(response => response.json())
        .then(data => {
            createManagerCard(data)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});