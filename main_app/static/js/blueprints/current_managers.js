const stintsUrl = `${SCRIPT_ROOT}/api/stints`
const managerUrl = `${SCRIPT_ROOT}/api/managers`
const downloadTableUrl = `${SCRIPT_ROOT}/api/download-table`

const managersTable = document.getElementById("managersTable")
const managersTableBody = managersTable.getElementsByTagName("tbody")[0]
const managersRows = Array.from(managersTableBody.getElementsByTagName("tr"))
const managerBtns = document.querySelectorAll("#genBtn")
const tableDiv = document.getElementById("standings")
const managerProfileDiv = document.getElementById("managerProfile")
const managersDiv = document.getElementById("managersTableDiv")
const toggleArrowBtn = document.getElementById("toggleArrowBtn")
const toggleArrowCard = document.getElementById("toggleArrowCard")
const downloadBtn = document.getElementById("downBtn")
const spinner = document.getElementById("spinner")

let spinnerVisible = false
let downloadBtnVisible = false

let table

function daysElapsedNow(dateString) {
  const inputDate = new Date(dateString)
  const currentDate = new Date()
  const timeDifference = currentDate - inputDate
  const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24))
  return daysDifference
}

const currentDaysElapsed = managersRows.map((row) => {
  const dateCell = row.cells[4]
  const dateString = dateCell.textContent.trim()
  const daysElapsedValue = daysElapsedNow(dateString)
  const daysElapsedCell = row.cells[5]
  daysElapsedCell.textContent = daysElapsedValue
  return { row, daysElapsedValue }
})

currentDaysElapsed.sort((a, b) => b.daysElapsedValue - a.daysElapsedValue)
managersTableBody.innerHTML = ""
currentDaysElapsed.forEach(({ row }) => {
  managersTableBody.appendChild(row)
})

function hideManagers() {
  if (!managersDiv.classList.contains("hidden")) {
    managersDiv.classList.add("hidden")
  }
  managerProfileDiv.classList.remove("hidden")
}

function createManagerCard(data) {
  managerProfileDiv.innerHTML = ""

  let managerNameDiv = document.createElement("div")
  managerNameDiv.className = "managerNameCard"

  let managerTitle = document.createElement("h1")
  managerTitle.textContent = data.name
  managerTitle.className = "managerTitle"
  managerTitle.id = "managerTitle"

  let managerFace = document.createElement("img")
  managerFace.src = data.face_url
  managerFace.className = "managerFaceCard"
  managerFace.id = "managerFaceCard"

  managerNameDiv.appendChild(managerTitle)
  managerNameDiv.appendChild(managerFace)

  let managerNationDiv = document.createElement("div")
  managerNationDiv.className = "managerNationCard"

  let managerNation = document.createElement("h1")
  managerNation.textContent = data.nation_name
  managerNation.className = "managerNation"

  let nationFlag = document.createElement("img")
  nationFlag.src = data.nation_flag_url
  nationFlag.className = "nationFlag"
  nationFlag.id = "nationFlag"

  managerNationDiv.appendChild(managerNation)
  managerNationDiv.appendChild(nationFlag)

  let managerTeamDiv = document.createElement("div")
  managerTeamDiv.className = "managerTeamCard"

  let managerTeam = document.createElement("h1")
  managerTeam.textContent = data.team_name
  managerTeam.className = "managerTeam"
  managerTeam.id = "managerTeam"

  let teamCrest = document.createElement("img")
  teamCrest.src = data.team_crest_url
  teamCrest.className = "managerTeamImg"
  teamCrest.id = "managerTeamImg"

  managerTeamDiv.appendChild(managerTeam)
  managerTeamDiv.appendChild(teamCrest)

  let managerStart = document.createElement("p")
  managerStart.textContent = `Start Day: ${data.date_start}`
  managerStart.className = "managerStart"
  managerStart.id = "managerStart"

  let daysElapsedValue = daysElapsedNow(data.date_start)
  let managerDays = document.createElement("p")
  managerDays.textContent = `Days in Charge: ${daysElapsedValue}`
  managerDays.className = "managerDays"

  let toggleCard = document.createElement("div")
  toggleCard.id = "toggleArrowCard"
  toggleCard.classList.add("toggleArrow")
  toggleCard.classList.add("toggleCard")
  toggleCard.innerHTML =
    "&#x25B6; <span class='arrowText'> Change Managerial Stint</span>"
  toggleCard.addEventListener("click", () => {
    managersDiv.classList.remove("hidden")
    managerProfileDiv.classList.add("hidden")
  })

  managerProfileDiv.appendChild(managerNameDiv)
  managerProfileDiv.appendChild(managerNationDiv)
  managerProfileDiv.appendChild(managerTeamDiv)
  managerProfileDiv.appendChild(managerStart)
  managerProfileDiv.appendChild(managerDays)
  managerProfileDiv.appendChild(toggleCard)
}

managerBtns.forEach((btn) => {
  btn.addEventListener("click", async function () {
    let stintId = btn.name
    const response = await fetch(`${stintsUrl}/${stintId}`)
      .then((response) => response.json())
      .then((data) => {
        if (Object.keys(data).length === 0 && data.constructor === Object) {
          noMatches(
            "No matches played in these dates. Please choose a different stint"
          )
          return
        }
        table = createTable(data)
        sortTable(table, 0)
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        )
      })

    fetch(`${managerUrl}/${stintId}`)
      .then((response) => response.json())
      .then((data) => {
        hideManagers()
        createManagerCard(data)
        highlightTeam(table, data)
        toggleDownloadBtn()
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        )
      })
  })
})

toggleArrowBtn.addEventListener("click", () => {
  managerProfileDiv.classList.remove("hidden")
  managersDiv.classList.add("hidden")
})

toggleArrowCard.addEventListener("click", () => {
  managersDiv.classList.remove("hidden")
  managerProfileDiv.classList.add("hidden")
})

downloadBtn.addEventListener("click", () => {
  const today = new Date()

  const managerName = document.getElementById("managerTitle").textContent
  const managerFace = document.getElementById("managerFaceCard").src
  const nationLogo = document.getElementById("nationFlag").src
  const teamLogo = document.getElementById("managerTeamImg").src
  const teamName = document.getElementById("managerTeam").textContent
  const managerStartDate = document
    .getElementById("managerStart")
    .textContent.replace("Start Day: ", "")
  const managerEndDate = today.toISOString().split("T")[0]

  downloadImage(
    `${managerName}: ${managerStartDate} - ${managerEndDate}`,
    managerFace,
    nationLogo,
    teamLogo,
    teamName
  )
})
