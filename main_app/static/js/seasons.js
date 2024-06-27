const seasonUrl = `${SCRIPT_ROOT}/api/seasons`

const dropdownElement = document.getElementById('seasons');
const firstSeason = dropdownElement.options[0].text.replace("/", "-")
const tableDiv = document.getElementById('standings')
const titleDiv = document.getElementById('standings-title')
const genBtn = document.getElementById('genBtn')
getCurrentSeasonTable(firstSeason)

function createTable(data){
    tableDiv.innerHTML = '';
    let table = document.createElement('table');
    table.id = 'pl-table';
    table.className = 'standing-table';

    let thead = document.createElement('thead');
    let headerRow = document.createElement('tr');

    let headers = ['#', '', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS'];

    headers.forEach((headerText, index) => {
        let th = document.createElement('th');
        if (headerText === 'Team') {
            th.className = 'team';
        }
        th.textContent = headerText;
        headerRow.appendChild(th);
        if (index != 1){
            th.addEventListener('click', () => {
                sortTable(table, index)
            });
        }
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

function sortTable(table, n){
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

            if (n != 2){
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
            } else {
                if (dir == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
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

function seasonTitle(season){
    titleDiv.textContent = season
}

function getCurrentSeasonTable(firstSeason){
    fetch(`${seasonUrl}/${firstSeason}`)
        .then(response => response.json())
        .then(data => {
            currentTable = createTable(data)
            sortTable(currentTable, 0)
            sortTable(currentTable, 0)
            seasonTitle(firstSeason.replace("-", "/"))
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

genBtn.addEventListener('click', () => {
    let selectedValue = dropdownElement.value.replace("/", "-")
    fetch(`${seasonUrl}/${selectedValue}`)
    .then(response => response.json())
    .then(data => {
        table = createTable(data)
        sortTable(table, 0)
        seasonTitle(selectedValue.replace("-", "/"))
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
});