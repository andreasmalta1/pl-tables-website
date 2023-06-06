const downloadBtn = document.getElementById("convert")
const tables = document.querySelectorAll("table")
let columnIndex



downloadBtn.addEventListener("click", () => {
    tables.forEach(table => {
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
    })
})