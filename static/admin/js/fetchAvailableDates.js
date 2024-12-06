document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');  // Assuming the field is named 'id_date'

    if (dateField) {
        fetchAvailableDates();

        // Add event listener for date change
        dateField.addEventListener('change', function () {
            const selectedDateId = dateField.value;
            console.log('Selected Date ID:', selectedDateId); // Log the selected date ID

            if (selectedDateId) {
                // Trigger fetch for time slots when a valid date is selected
                fetchTimeSlots(selectedDateId);
            } else {
                // Reset time slot dropdown and disable if no date is selected
                const timeSlotField = document.getElementById('id_time_slots');
                timeSlotField.innerHTML = '<option value="">Select a date first</option>';
                timeSlotField.disabled = true;
            }
        });
    }

    // Fetch available dates and populate the date dropdown
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

                const availableDates = data.available_dates;
                if (!availableDates || !Array.isArray(availableDates)) {
                    console.error('Invalid response format for available dates');
                    return;
                }

                // Populate date dropdown
                dateField.innerHTML = '<option value="">Select a date</option>';
                availableDates.forEach(dateObj => {
                    const option = document.createElement('option');
                    option.value = dateObj.id; // Use the ID as the value
                    option.textContent = dateObj.display; // Display the formatted date
                    dateField.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching available dates:', error);
            });
    }
});