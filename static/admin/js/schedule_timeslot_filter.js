document.addEventListener('DOMContentLoaded', function() {
    const scheduleField = document.getElementById('id_schedule');
    const timeSlotField = document.getElementById('id_time_slots'); // Ensure the ID matches your actual HTML

    if (scheduleField) {
        scheduleField.addEventListener('change', function() {
            fetchTimeSlots();
        });
    }

    function fetchTimeSlots() {
        const scheduleId = scheduleField.value;

        if (scheduleId) {
            fetch(`/get-timeslots/?schedule_id=${scheduleId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Clear and populate the timeSlotField
                timeSlotField.innerHTML = '';
                data.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.id;
                    option.textContent = slot.label;
                    timeSlotField.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching time slots:', error));
        } else {
            timeSlotField.innerHTML = '';  // Clear if no schedule selected
        }
    }
});