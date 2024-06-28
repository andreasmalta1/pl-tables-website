const yearUrl = `${SCRIPT_ROOT}/api/years`

const dropdownElement = document.getElementById('years');
const firstYear = dropdownElement.options[0].text.replace("/", "-")
const tableDiv = document.getElementById('standings')
const titleDiv = document.getElementById('standings-title')
const genBtn = document.getElementById('genBtn')
getCurrentYearTable(firstYear)

function yearTitle(year){
    titleDiv.textContent = year
}

function getCurrentYearTable(firstYear){
    fetch(`${yearUrl}/${firstYear}`)
        .then(response => response.json())
        .then(data => {
            currentTable = createTable(data)
            sortTable(currentTable, 0)
            yearTitle(firstYear.replace("-", "/"))
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

genBtn.addEventListener('click', () => {
    let selectedValue = dropdownElement.value
    fetch(`${yearUrl}/${selectedValue}`)
    .then(response => response.json())
    .then(data => {
        table = createTable(data)
        sortTable(table, 0)
        yearTitle(selectedValue)
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
});