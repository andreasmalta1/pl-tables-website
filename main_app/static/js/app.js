document.getElementById('start_date').max = max = new Date().toISOString().split("T")[0];
document.getElementById('end_date').max = max = new Date().toISOString().split("T")[0];

if (!endDate){
    document.getElementById('end_date').valueAsDate = new Date();
}
