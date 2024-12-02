document.addEventListener('DOMContentLoaded', function() {
    const dateField = document.getElementById('id_date');  // Assuming the field is named 'id_date'
    const timeSlotField = document.getElementById('id_time_slots'); // Ensure the ID matches your actual HTML
    timeSlotField.innerHTML = ''

    if (dateField) {
        dateField.addEventListener('change', function() {
            fetchTimeSlots();
        });
    }

    function fetchTimeSlots() {
        const selectedDate = dateField.value;

        if (selectedDate) {
            fetch(`/get-timeslots/?date=${selectedDate}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Received data:", data);
                const timeSlots = data.time_slots;
                timeSlotField.innerHTML = ''// Adjust to match the response structure
                timeSlots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.id;
                    option.textContent = slot.display;
                    timeSlotField.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching time slots:', error));
        } else {
            timeSlotField.innerHTML = '';  // Clear if no date selected
        }
    }
});