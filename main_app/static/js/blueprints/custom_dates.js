const datesUrl = `${SCRIPT_ROOT}/api/dates`
const downloadTableUrl = `${SCRIPT_ROOT}/api/download-table`

const dateInputEl = document.getElementById("dateInput")
const startDateInput = document.getElementById("startDate")
const endDateInput = document.getElementById("endDate")
const tableDiv = document.getElementById("standings")
const genBtn = document.getElementById("genBtn")
const toggleArrow = document.getElementById("toggleArrow")
const downloadBtn = document.getElementById("downBtn")
const spinner = document.getElementById("spinner")

let spinnerVisible = false
let downloadBtnVisible = false

let today = new Date()
let todayFormatted = today.toISOString().split("T")[0]

startDateInput.setAttribute("max", todayFormatted)
endDateInput.setAttribute("max", todayFormatted)

let lastWeek = new Date()
lastWeek.setDate(today.getDate() - 7)
let lastWeekFormatted = lastWeek.toISOString().split("T")[0]

startDateInput.value = lastWeekFormatted
endDateInput.value = todayFormatted

function dateChecker() {
  if (startDateInput.value > endDateInput.value) {
    return false
  }

  if (startDateInput.value > today || endDateInput.value > today) {
    return false
  }
  return true
}

function incorrectDates() {
  tableDiv.innerHTML = ""
  let errorMsg = document.createElement("h3")
  errorMsg.textContent = "Incorrect Dates. Please choose different dates"
  tableDiv.appendChild(errorMsg)
}

function changeAppearance() {
  toggleArrow.innerHTML =
    '&#x25B6; <span class="arrowText"> Change Dates</span>'
  dateInputEl.classList.add("hidden")
}

fetch(`${datesUrl}/${startDateInput.value}/${endDateInput.value}`)
  .then((response) => response.json())
  .then((data) => {
    if (Object.keys(data).length === 0 && data.constructor === Object) {
      noMatches(
        "No matches played in these dates. Please choose different dates"
      )
      return
    }
    table = createTable(data)
    sortTable(table, 0)
    toggleDownloadBtn()
  })
  .catch((error) => {
    console.error("There has been a problem with your fetch operation:", error)
  })

genBtn.addEventListener("click", () => {
  const dateCheckBool = dateChecker()
  if (!dateCheckBool) {
    incorrectDates()
    return
  }
  fetch(`${datesUrl}/${startDateInput.value}/${endDateInput.value}`)
    .then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).length === 0 && data.constructor === Object) {
        noMatches(
          "No matches played in these dates. Please choose different dates"
        )
        return
      }
      table = createTable(data)
      sortTable(table, 0)
      changeAppearance()
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
    })
})

toggleArrow.addEventListener("click", () => {
  if (dateInputEl.classList.contains("hidden")) {
    dateInputEl.classList.remove("hidden")
    toggleArrow.innerHTML = '&#x25B2; <span class="arrowText"> Collapse</span>'
  } else {
    dateInputEl.classList.add("hidden")
    toggleArrow.innerHTML =
      '&#x25B6; <span class="arrowText"> Change Dates</span>'
  }
})

downloadBtn.addEventListener("click", () => {
  downloadImage(
    `Premier League Table: ${startDateInput.value} - ${endDateInput.value}`
  )
})
