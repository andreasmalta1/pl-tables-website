const managersTable = document.getElementById("currentManagers")
const managersTableBody = managersTable.getElementsByTagName('tbody')[0];
const managersRows = Array.from(managersTableBody.getElementsByTagName('tr'));

function daysElapsedNow(dateString) {
    const inputDate = new Date(dateString);
    const currentDate = new Date();
    const timeDifference = currentDate - inputDate;
    const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    return daysDifference;
}

const currentDaysElapsed = managersRows.map(row => {
    const dateCell = row.cells[4];
    const dateString = dateCell.textContent.trim();
    const daysElapsedValue = daysElapsedNow(dateString);
    const daysElapsedCell = row.cells[5];
    daysElapsedCell.textContent = daysElapsedValue;
    return { row, daysElapsedValue };
});

currentDaysElapsed.sort((a, b) => b.daysElapsedValue - a.daysElapsedValue);

managersTableBody.innerHTML = '';

currentDaysElapsed.forEach(({ row }) => {
    managersTableBody.appendChild(row);
})
