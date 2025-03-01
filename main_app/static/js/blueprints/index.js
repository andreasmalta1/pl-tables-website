const currentSeasonUrl = `${SCRIPT_ROOT}/api/current-season`
const deductionsUrl = `${SCRIPT_ROOT}/api/deductions`
const seasonUrl = `${SCRIPT_ROOT}/api/get-current-season`
const downloadTableUrl = `${SCRIPT_ROOT}/api/download-table`

const seasonDiv = document.getElementById("standingsTitle")
const tableDiv = document.getElementById("standings")
const deductionDiv = document.getElementById("deductions")
const downloadBtn = document.getElementById("downBtn")

document.addEventListener("DOMContentLoaded", () => {
  fetch(`${currentSeasonUrl}`)
    .then((response) => response.json())
    .then((data) => {
      table = createTable(data)
      sortTable(table, 0)
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })

  fetch(`${deductionsUrl}/current`)
    .then((response) => response.json())
    .then((data) => {
      createPointsDeduction(data)
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })

  fetch(`${seasonUrl}`)
    .then((response) => response.json())
    .then((data) => {
      seasonDiv.textContent = `Season ${data.season}`
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })
})

downloadBtn.addEventListener("click", () => {
  const table = document.getElementById("plTable")
  const tableData = []
  const headers = []
  const headerCells = table.querySelectorAll("thead tr th")

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

  fetch(downloadTableUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tableData: tableData }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      const imageData = data.image
      const link = document.createElement("a")
      link.href = "data:image/png;base64," + imageData
      link.download = "table_image.png"
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      console.log("done")
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })
})
