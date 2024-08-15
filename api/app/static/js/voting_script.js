const submitBtn = document.getElementById('submitBtn');
const modal = document.getElementById('myModal');
const closeModal = document.getElementsByClassName('close')[0];
const confirmVote = document.getElementById('confirmVote');
const cancelVote = document.getElementById('cancelVote');
const votingForm = document.getElementById('votingForm');


// SHOW THE MODAL
submitBtn.onclick = function() {
    const selectedParty = votingForm.querySelector('input[name="party"]:checked');
    if (selectedParty) {
        modalText.textContent = `¿Are you sure about voting for ${selectedParty.value}?`;
    }
    modal.style.display = 'flex';
}

// CLOSE THE MODAL (X)
closeModal.onclick = function() {
    modal.style.display = 'none';
}

// CANCEL THE VOTE AND CLOSE THE MODAL
cancelVote.onclick = function() {
    modal.style.display = 'none';
}

// CLOSE THE MODAL IF THE USER CLICK OUTSIDE THE BOX
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// CONFIRM THE VOTE AND SENT TO KAFKA
confirmVote.onclick = function() {
    modal.style.display = 'none';
    try {
        const selectedParty = votingForm.querySelector('input[name="party"]:checked').value;
        const additionalId = document.getElementById('id').value;

        const data = {
            vote:  selectedParty,
            id: additionalId
        };
        console.log('Data to send:', JSON.stringify(data));

        fetch('/submit_vote', {
            method: 'POST',  
            headers: {
                'Content-Type': 'application/json'  
            },
            body: JSON.stringify(data)  
        })
        .then(response => {
            if (response.ok) {
                alert('Vote successfully registered, the page will be close inmediatly!!');
                location.href="/page_final";
            } else {
                response.json().then(errorData => {
                    handleError(response.status, errorData.detail);
                }).catch(() => {
                    alert('An unknown error occurred while processing the response.');
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again later.');
        });
        
    } catch (error) {
        alert('An unexpected error occurred. Please try again later.');
    }
}

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

// HANDLE THE EXCEPTION
function handleError(status, detail) {
    switch (status) {
        case 400:
            alert(`Error: ${detail}`);
            break;
        case 422:
            alert('Validation error: Please check your input.');
            break;
        default:
            alert('An unexpected error occurred.');
            break;
    }
}
