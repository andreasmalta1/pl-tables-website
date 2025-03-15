function downloadImage(
  title,
  managerFace = null,
  nationLogo = null,
  teamLogo = null,
  teamName = null
) {
  const table = document.getElementById("plTable")
  const tableData = []
  const headers = []
  const headerCells = table.querySelectorAll("thead tr th")

  toggleSpinner()
  toggleDownloadBtn()

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

  let tableDataObj = {
    tableData: tableData,
    title: title,
  }

  if (
    typeof deductionDiv !== "undefined" &&
    deductionDiv &&
    deductionDiv.hasChildNodes()
  ) {
    const deductionList = []
    const deductions = deductionDiv.querySelectorAll("p")

    deductions.forEach((deduction) => {
      deductionList.push(deduction.textContent)
    })
    tableDataObj.deductions = deductionList
  }

  if (managerFace) {
    tableDataObj.managerFace = managerFace
  }

  if (nationLogo) {
    tableDataObj.nationLogo = nationLogo
  }

  if (teamLogo) {
    tableDataObj.teamLogo = teamLogo
  }

  if (teamName) {
    tableDataObj.teamName = teamName
  }

  tableDataObj = JSON.stringify({ tableDataObj })

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
      toggleSpinner()
      toggleDownloadBtn()
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      )
      toggleSpinner()
      toggleDownloadBtn()
    })
}

function toggleSpinner() {
  if (spinnerVisible) {
    spinner.style.display = "none"
  } else {
    spinner.style.display = "block"
  }
  spinnerVisible = !spinnerVisible
}

function toggleDownloadBtn() {
  if (downloadBtnVisible) {
    downloadBtn.classList.add("hidden")
    downloadBtn.classList.remove("genBtn")
  } else {
    downloadBtn.classList.remove("hidden")
    downloadBtn.classList.add("genBtn")
  }
  downloadBtnVisible = !downloadBtnVisible
}
