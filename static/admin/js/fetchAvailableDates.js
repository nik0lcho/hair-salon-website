document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');

    if (dateField) {
        fetchAvailableDates();

        dateField.addEventListener('change', function () {
            const selectedDateId = dateField.value;
            console.log('Selected Date ID:', selectedDateId);

            if (selectedDateId) {
                fetchTimeSlots(selectedDateId);
            } else {
                const timeSlotField = document.getElementById('id_time_slots');
                timeSlotField.innerHTML = '<option value="">Select a date first</option>';
                timeSlotField.disabled = true;
            }
        });
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

                const availableDates = data.available_dates;
                if (!availableDates || !Array.isArray(availableDates)) {
                    console.error('Invalid response format for available dates');
                    return;
                }

                // Populate date dropdown
                dateField.innerHTML = '<option value="">Select a date</option>';
                availableDates.forEach(dateObj => {
                    const option = document.createElement('option');
                    option.value = dateObj.id;
                    option.textContent = dateObj.display;
                    dateField.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching available dates:', error);
            });
    }
});