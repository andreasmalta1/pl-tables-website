function createTable(data){
    tableDiv.innerHTML = '';
    let table = document.createElement('table');
    table.id = 'pl-table';
    table.className = 'standing-table';
    table.value = -1

    let thead = document.createElement('thead');
    let headerRow = document.createElement('tr');

    let headers = ['#', '', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS'];

    headers.forEach((headerText, index) => {
        let th = document.createElement('th');
        if (headerText === 'Team') {
            th.className = 'team-name';
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
        img.className = 'team-logo'
        logoCell.appendChild(img);
        row.appendChild(logoCell);

        let teamCell = document.createElement('td');
        teamCell.textContent = team;
        teamCell.className = 'team-name'
        row.appendChild(teamCell);

        let stats = ["played", "win", "draw", "loss", "goals_for", "goals_against", "gd", "points"];
        stats.forEach(stat => {
            let td = document.createElement('td');
            td.textContent = data[team][stat];
            if (stat === 'points') {
                td.className = 'points';
        }
            row.appendChild(td);
        });
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    tableDiv.appendChild(table);
    return table
}

function sortTable(table, n){
    let rows, switching, i, x, y, shouldSwitch, switchCount = 0;
    switching = true;
    let dir = table.value * -1
    table.value = dir

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (n != 2){
                if (dir == 1) {
                    if (Number(x.innerHTML) > Number(y.innerHTML)) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == -1) {
                    if (Number(x.innerHTML) < Number(y.innerHTML)) {
                        shouldSwitch = true;
                        break;
                    }
                }
            } else {
                if (dir == 1) {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == -1) {
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
        }
    }
}

function createPointsDeduction(pointDeductions){
    deductionDiv.innerHTML = ""
    if (Object.keys(pointDeductions).length === 0){
        return
    }
    for (const deduction in pointDeductions) {
        let deductionPar = document.createElement('p');
        deductionPar.textContent = `${pointDeductions[deduction]["team_name"]} deducted ${pointDeductions[deduction]["points_deducted"]} points - ${pointDeductions[deduction]["reason"]}`
        deductionDiv.appendChild(deductionPar)
    }
}
