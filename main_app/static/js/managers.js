const currentTitleEl = document.getElementById("current-manager")
const currentFormEl = document.getElementById("current-form")

const memorableTitleEl = document.getElementById("memorable-manager")
const memorableFormEl = document.getElementById("memorable-form")

const currentManagersTable = document.getElementById("currentManagers")
const currentManagersTableBody = currentManagersTable.getElementsByTagName('tbody')[0];
const currentManagersRows = Array.from(currentManagersTableBody.getElementsByTagName('tr'));


const memorableManagersTable = document.getElementById("memorableManagers")
const memorableManagersTableBody = memorableManagersTable.getElementsByTagName('tbody')[0];
const memorableManagersRows = Array.from(memorableManagersTableBody.getElementsByTagName('tr'));

currentTitleEl.addEventListener('click', () => {
    currentFormEl.classList.toggle("form-hidden")
})

memorableTitleEl.addEventListener('click', () => {
    memorableFormEl.classList.toggle("form-hidden")
})

function daysElapsedNow(dateString) {
    const inputDate = new Date(dateString);
    const currentDate = new Date();
    const timeDifference = currentDate - inputDate;
    const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    return daysDifference;
}

function daysDifference(startDateString, endDateString) {
    const startDate = new Date(startDateString);
    const endDate = new Date(endDateString);
    const timeDifference = endDate - startDate;
    const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    return daysDifference;
}

const currentDaysElapsed = currentManagersRows.map(row => {
    const dateCell = row.cells[4];
    const dateString = dateCell.textContent.trim();
    const daysElapsedValue = daysElapsedNow(dateString);
    const daysElapsedCell = row.cells[5];
    daysElapsedCell.textContent = daysElapsedValue;
    return { row, daysElapsedValue };
});

currentDaysElapsed.sort((a, b) => b.daysElapsedValue - a.daysElapsedValue);

currentManagersTableBody.innerHTML = '';


currentDaysElapsed.forEach(({ row }) => {
    currentManagersTableBody.appendChild(row);
})


const memorableDaysElapsed = memorableManagersRows.map(row => {
    const startDateCell = row.cells[4];
    const startDateString = startDateCell.textContent.trim();
    const endDateCell = row.cells[5];
    const endDateString = endDateCell.textContent.trim();
    const daysElapsedValue = daysDifference(startDateString, endDateString);
    const daysElapsedCell = row.cells[6];
    daysElapsedCell.textContent = daysElapsedValue;
    return { row, daysElapsedValue };
});


memorableDaysElapsed.sort((a, b) => b.daysElapsedValue - a.daysElapsedValue);

memorableManagersTableBody.innerHTML = '';


memorableDaysElapsed.forEach(({ row }) => {
    memorableManagersTableBody.appendChild(row);
})
