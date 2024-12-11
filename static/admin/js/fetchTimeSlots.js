document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');  // Assuming the field is named 'id_date'
    const timeSlotField = document.getElementById('id_time_slots'); // Ensure the ID matches your actual HTML

    if (dateField && timeSlotField) {
        timeSlotField.disabled = true;

        dateField.addEventListener('change', function () {
            const selectedDateId = dateField.value;
            console.log('Selected Date ID for time slots:', selectedDateId);

            if (selectedDateId) {
                fetchTimeSlots(selectedDateId);
            } else {
                timeSlotField.innerHTML = '<option value="">Select a date first</option>';
                timeSlotField.disabled = true;
            }
        });
    }

    function fetchTimeSlots(selectedDateId) {
        console.log('Fetching available time slots for date ID:', selectedDateId);

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
                console.log('Fetched time slots:', data);

                const timeSlots = data.time_slots;
                if (!timeSlots || !Array.isArray(timeSlots)) {
                    console.error('Invalid response format for time slots');
                    timeSlotField.innerHTML = '<option value="">No available slots</option>';
                    return;
                }

                timeSlotField.innerHTML = '<option value="">Select a time slot</option>';
                timeSlots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.id;
                    option.textContent = slot.display;
                    timeSlotField.appendChild(option);
                });

                timeSlotField.disabled = false;
            })
            .catch(error => {
                console.error('Error fetching time slots:', error);
                timeSlotField.innerHTML = '<option value="">Error fetching time slots</option>';
            });
    }
});