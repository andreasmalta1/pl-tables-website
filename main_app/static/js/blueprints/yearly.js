const yearUrl = `${SCRIPT_ROOT}/api/years`
const downloadTableUrl = `${SCRIPT_ROOT}/api/download-table`

const dropdownElement = document.getElementById("years")
const firstYear = dropdownElement.options[0].text.replace("/", "-")
const yearInputEl = document.getElementById("yearInput")
const yearTitleEl = document.getElementById("yearTitle")
const yearTextEl = document.getElementById("yearText")
const tableDiv = document.getElementById("standings")
const genBtn = document.getElementById("genBtn")
const toggleArrowBtn = document.getElementById("toggleArrowBtn")
const toggleArrowTitle = document.getElementById("toggleArrowTitle")
const downloadBtn = document.getElementById("downBtn")
const spinner = document.getElementById("spinner")

let spinnerVisible = false
let downloadBtnVisible = false

getCurrentYearTable(firstYear)

function getCurrentYearTable(firstYear) {
  fetch(`${yearUrl}/${firstYear}`)
    .then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).length === 0 && data.constructor === Object) {
        noMatches("Invalid year. Please choose a different calendar year")
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
  yearTextEl.innerHTML = `Calendar year ${firstYear}`
}

genBtn.addEventListener("click", () => {
  let selectedValue = dropdownElement.value
  fetch(`${yearUrl}/${selectedValue}`)
    .then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).length === 0 && data.constructor === Object) {
        noMatches("Invalid year. Please choose a different calendar year")
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
  yearTextEl.innerHTML = `Calendar Year ${selectedValue}`
  yearTitleEl.classList.remove("hidden")
  yearInputEl.classList.add("hidden")
})

toggleArrowBtn.addEventListener("click", () => {
  yearTitleEl.classList.remove("hidden")
  yearInputEl.classList.add("hidden")
})

toggleArrowTitle.addEventListener("click", () => {
  yearInputEl.classList.remove("hidden")
  yearTitleEl.classList.add("hidden")
})

downloadBtn.addEventListener("click", () => {
  downloadImage(yearTextEl.innerHTML)
})
