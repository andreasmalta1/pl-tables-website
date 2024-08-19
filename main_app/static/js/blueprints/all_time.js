const allTimeTableUrl = `${SCRIPT_ROOT}/api/all-time`


const tableDiv = document.getElementById('standings')

document.addEventListener("DOMContentLoaded", () => {
    fetch(`${allTimeTableUrl}`)
        .then(response => response.json())
        .then(data => {
            table = createTable(data)
            sortTable(table, 0)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
})