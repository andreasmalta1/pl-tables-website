const currentSeasonsUrl = `${SCRIPT_ROOT}/api/current-season`
const deductionsUrl = `${SCRIPT_ROOT}/api/deductions`

const tableDiv = document.getElementById('standings')
const deductionDiv = document.getElementById('deductions')

document.addEventListener("DOMContentLoaded", () => {
    fetch(`${currentSeasonsUrl}`)
        .then(response => response.json())
        .then(data => {
            table = createTable(data)
            sortTable(table, 0)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });

    fetch(`${deductionsUrl}/current`)
        .then(response => response.json())
        .then(data => {
            createPointsDeduction(data)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
})