function downloadImage() {
  const table = document.getElementById("plTable")
  const tableData = []
  const headers = []
  const headerCells = table.querySelectorAll("thead tr th")

  downloadBtn.textContent = "Processing"

  headerCells.forEach((cell) => {
    headers.push(cell.textContent)
  })

  const rows = table.querySelectorAll("tbody tr")
  rows.forEach((row) => {
    const rowData = {}
    const cells = row.querySelectorAll("td")
    cells.forEach((cell, index) => {
      if (cell.textContent) {
        rowData[headers[index]] = cell.textContent
      } else {
        const image = cell.querySelectorAll("img")
        rowData[headers[index]] = image[0].src
      }
    })
    tableData.push(rowData)
  })

  let tableDataObj = JSON.stringify({
    tableData: tableData,
    title: seasonDiv.textContent,
  })

  fetch(downloadTableUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: tableDataObj,
  })
    .then((response) => response.json())
    .then((data) => {
      const imageData = data.image
      const link = document.createElement("a")
      link.href = "data:image/png;base64," + imageData
      link.download = "table_image.png"
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      downloadBtn.textContent = "Download Table"
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })
}
