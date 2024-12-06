document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');  // Assuming the field is named 'id_date'
    const timeSlotField = document.getElementById('id_time_slots'); // Ensure the ID matches your actual HTML

    if (dateField && timeSlotField) {
        timeSlotField.innerHTML = '<option value="">Select a time slot</option>';

        dateField.addEventListener('change', function () {
            fetchTimeSlots(dateField.value);
        });
    }

    function fetchTimeSlots(selectedDate) {
        if (selectedDate) {
            fetch(`/get-timeslots/?date=${selectedDate}`, {
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
                    console.log('Full response:', data);

                    // Validate and extract time_slots
                    const timeSlots = data.time_slots;
                    if (!timeSlots || !Array.isArray(timeSlots)) {
                        console.error('time_slots property missing or invalid in response');
                        timeSlotField.innerHTML = '<option value="">No slots available</option>';
                        return;
                    }

                    // Populate dropdown
                    timeSlotField.innerHTML = '<option value="">Select an appointment</option>';
                    timeSlots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.display;
                        option.textContent = slot.display;
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