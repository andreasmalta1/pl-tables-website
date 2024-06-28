const datesUrl = `${SCRIPT_ROOT}/api/dates`

const startDateInput = document.getElementById("start_date")
const endDateInput = document.getElementById("end_date")
const tableDiv = document.getElementById('standings')
const genBtn = document.getElementById('genBtn')

let today = new Date();
let todayFormatted = today.toISOString().split('T')[0];

let lastWeek = new Date();
lastWeek.setDate(today.getDate() - 7);
let lastWeekFormatted = lastWeek.toISOString().split('T')[0];

startDateInput.value = lastWeekFormatted;
endDateInput.value = todayFormatted;

fetch(`${datesUrl}/${startDateInput.value}/${endDateInput.value}`)
    .then(response => response.json())
    .then(data => {
        table = createTable(data)
        sortTable(table, 0)
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });

genBtn.addEventListener('click', () => {
    fetch(`${datesUrl}/${startDateInput.value}/${endDateInput.value}`)
    .then(response => response.json())
    .then(data => {
        table = createTable(data)
        sortTable(table, 0)
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
});