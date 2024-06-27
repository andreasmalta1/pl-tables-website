const startDateInput = document.getElementById("start_date")
const endDateInput = document.getElementById("end_date")

let today = new Date();
let todayFormatted = today.toISOString().split('T')[0];

let lastWeek = new Date();
lastWeek.setDate(today.getDate() - 7);
let lastWeekFormatted = lastWeek.toISOString().split('T')[0];

startDateInput.value = lastWeekFormatted;
endDateInput.value = todayFormatted;