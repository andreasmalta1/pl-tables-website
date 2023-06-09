const currentBtn = document.getElementById("down-current")
const allBtn = document.getElementById("down-all")
const currentTable = document.getElementById("current-table")
const allTable = document.getElementById("all-time-table")

let columnIndex

deletedCells = []

downloadImage = (table) => {
    let headerRow = table.getElementsByTagName('tr')[0];
    let headers = headerRow.getElementsByTagName('th');

    for (let i = 0; i < headers.length; i++) {
        if (headers[i].innerHTML === "") {
            columnIndex = i;
            break;
        }
    }
    
    if (columnIndex !== undefined) {
        let rowCount = table.rows.length;
        for (let i = 0; i < rowCount; i++) {
            deletedCells.push(table.rows[i].cells[columnIndex].innerHTML)
            table.rows[i].deleteCell(columnIndex);
        }
    }

    let row = table.insertRow(-1);
    let cell = row.insertCell(0);

    cell.innerHTML = "Downloaded from www.pltables.com. Developed by @andreascalleja"
    cell.colSpan = "10";
    cell.style.fontSize = "0.75rem"

    html2canvas(table)
    .then(async function (canvas) {
        const img = await canvas.toDataURL("image/png")
        const a = document.createElement('a')
        a.setAttribute("href", img)
        a.setAttribute("download", "table.png")
        a.click()
        a.remove()
    })

    rowCount = table.rows.length;
    table.deleteRow(rowCount - 1);

    if (columnIndex !== undefined) {
        let rowCount = table.rows.length;
        for (let i = 0; i < rowCount; i++) {
            let newCell = table.rows[i].insertCell(columnIndex);
            if (i == 0){
                newCell.outerHTML = "<th></th>"
            } else {
                newCell.innerHTML = deletedCells[i]
            }
        }
    }
}

currentBtn.addEventListener("click",
    function() {
        downloadImage(currentTable)
    }) 

allBtn.addEventListener("click",
    function() {
        downloadImage(allTable)
    }) 