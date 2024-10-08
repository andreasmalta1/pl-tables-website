const currentSeasonUrl = `${SCRIPT_ROOT}/api/current-season`
const deductionsUrl = `${SCRIPT_ROOT}/api/deductions`
const seasonUrl = `${SCRIPT_ROOT}/api/get-current-season`

const seasonDiv = document.getElementById('standingsTitle')
const tableDiv = document.getElementById('standings')
const deductionDiv = document.getElementById('deductions')

document.addEventListener("DOMContentLoaded", () => {
    fetch(`${currentSeasonUrl}`)
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
    
    fetch(`${seasonUrl}`)
        .then(response => response.json())
        .then(data => {
            seasonDiv.textContent = `Season ${data.season}`
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
})
