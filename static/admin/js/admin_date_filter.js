document.addEventListener('DOMContentLoaded', function() {
    const dateField = document.getElementById('id_date');  // Replace with your actual field ID

    if (dateField) {
        populateAvailableDates();
    }

    function populateAvailableDates() {
        fetch('/get-available-dates/', {  // URL of your view
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.available_dates) {
                dateField.innerHTML = '';  // Clear existing options
                data.available_dates.forEach(date => {
                    const option = document.createElement('option');
                    option.value = date;
                    option.textContent = date;
                    dateField.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error fetching available dates:', error));
    }
});
