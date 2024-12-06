document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');  // Assuming the field is named 'id_date'
    const timeSlotField = document.getElementById('id_time_slots'); // Ensure the ID matches your actual HTML

    if (dateField && timeSlotField) {
        // Disable time slots until a valid date is selected
        timeSlotField.disabled = true;

        dateField.addEventListener('change', function () {
            const selectedDateId = dateField.value;
            console.log('Selected Date ID for time slots:', selectedDateId); // Log the selected date ID

            // Only fetch time slots if a valid date is selected
            if (selectedDateId) {
                fetchTimeSlots(selectedDateId); // Fetch time slots for the selected date
            } else {
                // Reset time slot dropdown if no date is selected
                timeSlotField.innerHTML = '<option value="">Select a date first</option>';
                timeSlotField.disabled = true;
            }
        });
    }

    // Fetch available time slots based on the selected date ID
    function fetchTimeSlots(selectedDateId) {
        console.log('Fetching available time slots for date ID:', selectedDateId); // Log the selected date ID

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
                console.log('Fetched time slots:', data); // Log the fetched time slots

                const timeSlots = data.time_slots;
                if (!timeSlots || !Array.isArray(timeSlots)) {
                    console.error('Invalid response format for time slots');
                    timeSlotField.innerHTML = '<option value="">No available slots</option>';
                    return;
                }

                // Populate the time slot dropdown with only available slots
                timeSlotField.innerHTML = '<option value="">Select a time slot</option>';
                timeSlots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.id; // Use the slot ID as the value
                    option.textContent = slot.display; // Display the slot information
                    timeSlotField.appendChild(option);
                });

                timeSlotField.disabled = false; // Enable the time slot field once options are populated
            })
            .catch(error => {
                console.error('Error fetching time slots:', error);
                timeSlotField.innerHTML = '<option value="">Error fetching time slots</option>';
            });
    }
});