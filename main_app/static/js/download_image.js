const downloadBtn = document.getElementById("down-table")
const table = document.getElementById("pl-table")
let columnIndex

deletedCells = []

downloadBtn.addEventListener("click", () => {
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

    html2canvas(table)
    .then(async function (canvas) {
        const img = await canvas.toDataURL("image/jpeg")
        const a = document.createElement('a')
        a.setAttribute("href", img)
        a.setAttribute("download", "table.png")
        a.click()
        a.remove()
    })

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
})