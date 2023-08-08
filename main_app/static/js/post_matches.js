const datePickerEl = document.getElementById('datePicker');
const today = new Date().toISOString().split('T')[0];

datePickerEl.valueAsDate = new Date();
datePickerEl.setAttribute("max", today);