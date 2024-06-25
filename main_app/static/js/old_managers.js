const managersUrl = `${SCRIPT_ROOT}/api/managers`

const managersTable = document.getElementById("memorableManagers")
const managersTableBody = managersTable.getElementsByTagName('tbody')[0];
const managersRows = Array.from(managersTableBody.getElementsByTagName('tr'));
const managerBtns = document.querySelectorAll('.down-button');
console.log(managerBtns)
const tableDiv = document.getElementById('standings')

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

function createTable(data){
    tableDiv.innerHTML = '';
    let table = document.createElement('table');
    table.id = 'pl-table';
    table.className = 'standing-table';

    let thead = document.createElement('thead');
    let headerRow = document.createElement('tr');

    let headers = ['#', '', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS'];

    headers.forEach(headerText => {
        let th = document.createElement('th');
        if (headerText === 'Team') {
            th.className = 'team';
        }
        th.textContent = headerText;
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create the table body
    let tbody = document.createElement('tbody');

    for (const team in data) {
        let row = document.createElement('tr');
        let rkCell = document.createElement('td');
        rkCell.textContent = data[team]["rk"];
        row.appendChild(rkCell);

        let logoCell = document.createElement('td');
        let img = document.createElement('img');
        img.src = data[team]["url"]
        img.style.width = '30px'; // Adjust the size as needed
        logoCell.appendChild(img);
        row.appendChild(logoCell);

        let teamCell = document.createElement('td');
        teamCell.textContent = team;
        row.appendChild(teamCell);

        let stats = ["played", "win", "draw", "loss", "goals_for", "goals_against", "gd", "points"];
        stats.forEach(stat => {
            let td = document.createElement('td');
            td.textContent = data[team][stat];
            row.appendChild(td);
        });
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    tableDiv.appendChild(table);
    return table
}

function sortTable(table){
    let n = 0
    let rows, switching, i, x, y, shouldSwitch, dir, switchCount = 0;
    switching = true;
    dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (dir == "asc") {
                if (Number(x.innerHTML) > Number(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (Number(x.innerHTML) < Number(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
        } else {
            if (switchCount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}


managerBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        let stintId = btn.name;
        fetch(`${managersUrl}/${stintId}`)
        .then(response => response.json())
        .then(data => {
            table = createTable(data)
            sortTable(table)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});