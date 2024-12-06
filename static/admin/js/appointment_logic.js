document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date'); // Dropdown for available dates
    const timeSlotField = document.getElementById('id_time_slots'); // Dropdown for available time slots

    if (dateField && timeSlotField) {
        fetchAvailableDates();

        // Add event listener for date change to fetch time slots
        dateField.addEventListener('change', function () {
            fetchTimeSlots(dateField.value);
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

    // Fetch time slots for the selected date and populate the time slot dropdown
    function fetchTimeSlots(selectedDateId) {
        if (selectedDateId) {
            fetch(`/get-timeslots/?date=${selectedDateId}`, {
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
                    console.log('Time slots:', data);

                    const timeSlots = data.time_slots;
                    if (!timeSlots || !Array.isArray(timeSlots)) {
                        console.error('Invalid response format for time slots');
                        timeSlotField.innerHTML = '<option value="">No slots available</option>';
                        return;
                    }

                    // Populate time slot dropdown
                    timeSlotField.innerHTML = '<option value="">Select a time slot</option>';
                    timeSlots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.id; // Use the time slot ID as the value
                        option.textContent = slot.display; // Display the slot information
                        timeSlotField.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching time slots:', error);
                    timeSlotField.innerHTML = '<option value="">Error fetching time slots</option>';
                });
        } else {
            timeSlotField.innerHTML = '<option value="">Select a date first</option>';
        }
    }
});