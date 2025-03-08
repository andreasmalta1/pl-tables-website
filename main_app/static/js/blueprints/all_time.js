const allTimeTableUrl = `${SCRIPT_ROOT}/api/all-time`
const downloadTableUrl = `${SCRIPT_ROOT}/api/download-table`

const tableDiv = document.getElementById("standings")
const downloadBtn = document.getElementById("downBtn")

document.addEventListener("DOMContentLoaded", () => {
  fetch(`${allTimeTableUrl}`)
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
})

downloadBtn.addEventListener("click", () => {
  downloadImage("All Time Premier Legaue Table")
})
