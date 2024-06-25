let seasons_url = `${SCRIPT_ROOT}/api/seasons`

const allSeasonsElement = Array.from(document.getElementsByClassName("all-seasons"))

function createTable(data){
    let table = document.createElement('table');
    table.id = 'pl-table';
    table.className = 'standing-table';

    // Create the table header
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
    table.appendChild(tbody);

    // Append the table to the document body or any other container
    document.body.appendChild(table);

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
        tbody.appendChild(row);

        let teamCell = document.createElement('td');
        teamCell.textContent = team;
        row.appendChild(teamCell);

        let stats = ["played", "win", "draw", "loss", "goals_for", "goals_against", "gd", "points"];
        stats.forEach(stat => {
            let td = document.createElement('td');
            td.textContent = data[team][stat];
            row.appendChild(td);
        });
    }
    
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

allSeasonsElement.forEach(seasonElement => {
    seasonElement.addEventListener('click', () => {
        let inputValue = seasonElement.value.replace("/", "-")
        fetch(`${seasons_url}/${inputValue}`)
        .then(response => response.json())
        .then(data => {
            createTable(data)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
})