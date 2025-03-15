const seasonUrl = `${SCRIPT_ROOT}/api/seasons`
const deductionsUrl = `${SCRIPT_ROOT}/api/deductions`
const downloadTableUrl = `${SCRIPT_ROOT}/api/download-table`

const dropdownElement = document.getElementById("seasons")
const firstSeason = dropdownElement.options[0].text.replace("/", "-")
const seasonInputEl = document.getElementById("seasonInput")
const seasonTitleEl = document.getElementById("seasonTitle")
const seasonTextEl = document.getElementById("seasonText")
const tableDiv = document.getElementById("standings")
const genBtn = document.getElementById("genBtn")
const deductionDiv = document.getElementById("deductions")
const toggleArrowBtn = document.getElementById("toggleArrowBtn")
const toggleArrowTitle = document.getElementById("toggleArrowTitle")
const downloadBtn = document.getElementById("downBtn")
const spinner = document.getElementById("spinner")

let spinnerVisible = false
let downloadBtnVisible = false

getCurrentSeasonTable(firstSeason)

function getCurrentSeasonTable(firstSeason) {
  fetch(`${seasonUrl}/${firstSeason}`)
    .then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).length === 0 && data.constructor === Object) {
        noMatches("Invalid season. Please choose a different season")
        return
      }
      currentTable = createTable(data)
      sortTable(currentTable, 0)
      toggleDownloadBtn()
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })
  fetch(`${deductionsUrl}/${firstSeason}`)
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

  seasonTextEl.innerHTML = `Season ${firstSeason.replace("-", "/")}`
}

genBtn.addEventListener("click", () => {
  let selectedValue = dropdownElement.value.replace("/", "-")
  fetch(`${seasonUrl}/${selectedValue}`)
    .then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).length === 0 && data.constructor === Object) {
        noMatches("Invalid season. Please choose a different season")
        return
      }
      table = createTable(data)
      sortTable(table, 0)
      downloadBtn.classList.remove("hidden")
      downloadBtn.classList.add("genBtn")
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })

  fetch(`${deductionsUrl}/${selectedValue}`)
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

  seasonTextEl.innerHTML = `Season ${selectedValue.replace("-", "/")}`
  seasonTitleEl.classList.remove("hidden")
  seasonInputEl.classList.add("hidden")
})

toggleArrowBtn.addEventListener("click", () => {
  seasonTitleEl.classList.remove("hidden")
  seasonInputEl.classList.add("hidden")
})

toggleArrowTitle.addEventListener("click", () => {
  seasonInputEl.classList.remove("hidden")
  seasonTitleEl.classList.add("hidden")
})

downloadBtn.addEventListener("click", () => {
  downloadImage(seasonTextEl.innerHTML)
})
