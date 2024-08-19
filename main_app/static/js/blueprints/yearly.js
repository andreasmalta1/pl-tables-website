const yearUrl = `${SCRIPT_ROOT}/api/years`

const dropdownElement = document.getElementById('years');
const firstYear = dropdownElement.options[0].text.replace("/", "-")
const yearInputEl = document.getElementById('yearInput')
const yearTitleEl = document.getElementById('yearTitle')
const yearTextEl = document.getElementById('yearText')
const tableDiv = document.getElementById('standings')
const genBtn = document.getElementById('genBtn')
const toggleArrowBtn = document.getElementById('toggleArrowBtn')
const toggleArrowTitle = document.getElementById('toggleArrowTitle')

getCurrentYearTable(firstYear)

function getCurrentYearTable(firstYear){
    fetch(`${yearUrl}/${firstYear}`)
        .then(response => response.json())
        .then(data => {
            currentTable = createTable(data)
            sortTable(currentTable, 0)
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    yearTextEl.innerHTML = `Calendar year: ${firstYear}`
}

genBtn.addEventListener('click', () => {
    let selectedValue = dropdownElement.value
    fetch(`${yearUrl}/${selectedValue}`)
    .then(response => response.json())
    .then(data => {
        table = createTable(data)
        sortTable(table, 0)
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
    yearTextEl.innerHTML = `Calendar year: ${selectedValue}`
    yearTitleEl.classList.remove('hidden');
    yearInputEl.classList.add('hidden')
});


toggleArrowBtn.addEventListener('click', () => {
    yearTitleEl.classList.remove('hidden');
    yearInputEl.classList.add('hidden')
})


toggleArrowTitle.addEventListener('click', () => {
    yearInputEl.classList.remove('hidden');
    yearTitleEl.classList.add('hidden')
})