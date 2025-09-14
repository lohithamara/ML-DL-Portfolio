window.onload = function() {
    const airlineFilter = document.getElementById('airlineFilter');
    const classFilter = document.getElementById('classFilter');
    const stopsFilter = document.getElementById('stopsFilter');
    const table = document.getElementById('flightsTable');
    const tbody = table.getElementsByTagName('tbody')[0];
    let rows = Array.from(tbody.getElementsByTagName('tr'));

    function filterRows() {
        let airline = airlineFilter.value;
        let cls = classFilter.value;
        let stops = stopsFilter.value;
        let filtered = rows.filter(row => {
            let cells = row.getElementsByTagName('td');
            let airlineMatch = !airline || cells[0].innerText === airline;
            let classMatch = !cls || cells[6].innerText === cls;
            let stopsMatch = !stops || cells[5].innerText === stops;
            return airlineMatch && classMatch && stopsMatch;
        });
        // Hide all
        rows.forEach(r => r.style.display = 'none');
        // Show filtered
        filtered.forEach(r => r.style.display = '');
    }
    airlineFilter.onchange = classFilter.onchange = stopsFilter.onchange = filterRows;
};