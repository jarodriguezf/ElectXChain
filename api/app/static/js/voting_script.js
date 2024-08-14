

// ACTIVE THE BUTTON WHEN THE RADIUS ELEMENT ARE CHEKED
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('votingForm');
    const submitBtn = document.getElementById('submitBtn');

    function updateButtonState() {
        const isOptionSelected = form.querySelector('input[name="party"]:checked');
        submitBtn.disabled = !isOptionSelected;
    }

    form.querySelectorAll('input[name="party"]').forEach(function(radio) {
        radio.addEventListener('change', updateButtonState);
    });

    updateButtonState();
});
