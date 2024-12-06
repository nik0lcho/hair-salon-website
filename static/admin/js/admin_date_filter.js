document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');  // Assuming the field is named 'id_date'

    if (dateField) {
        fetchAvailableDates();
    }

    function fetchAvailableDates() {
        fetch('/get-available-dates/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Available dates:', data);

                // Validate and extract available_dates
                const availableDates = data.available_dates;
                if (!availableDates || !Array.isArray(availableDates)) {
                    console.error('available_dates property missing or invalid in response');
                    return;
                }

                // Populate the dateField
                dateField.innerHTML = '<option value="">Select a date</option>';
                availableDates.forEach(date => {
                    const option = document.createElement('option');
                    option.value = date; // Use the date as the value
                    option.textContent = date; // Display the date
                    dateField.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching available dates:', error);
            });
    }
});