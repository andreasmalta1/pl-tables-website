const seasonUrl = `${SCRIPT_ROOT}/api/seasons`
const deductionsUrl = `${SCRIPT_ROOT}/api/deductions`

const dropdownElement = document.getElementById('seasons');
const firstSeason = dropdownElement.options[0].text.replace("/", "-")
const tableDiv = document.getElementById('standings')
const genBtn = document.getElementById('genBtn')
const deductionDiv = document.getElementById('deductions')

getCurrentSeasonTable(firstSeason)

function getCurrentSeasonTable(firstSeason){
    fetch(`${seasonUrl}/${firstSeason}`)
        .then(response => response.json())
        .then(data => {
            currentTable = createTable(data)
            sortTable(currentTable, 0)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    fetch(`${deductionsUrl}/${firstSeason}`)
        .then(response => response.json())
        .then(data => {
            createPointsDeduction(data)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

genBtn.addEventListener('click', () => {
    let selectedValue = dropdownElement.value.replace("/", "-")
    fetch(`${seasonUrl}/${selectedValue}`)
        .then(response => response.json())
        .then(data => {
            table = createTable(data)
            sortTable(table, 0)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    
    fetch(`${deductionsUrl}/${selectedValue}`)
        .then(response => response.json())
        .then(data => {
            createPointsDeduction(data)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});