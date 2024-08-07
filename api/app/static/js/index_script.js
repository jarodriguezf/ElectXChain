
// EXTRACT REGISTER FORM AND SEND IT TO THE API
document.getElementById('registrationForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const data = {};

    // CONVERT FIELD NAMES TO MATCH UserSchema
    formData.forEach((value, key) => {
        switch (key) {
            case 'fullName':
                data['name'] = value;
                break;
            case 'dni':
                data['dni'] = value;
                break;
            case 'dob':
                // Ensure date is in YYYY-MM-DD format
                data['birth'] = new Date(value).toISOString().split('T')[0];
                break;
            case 'gender':
                data['genre'] = value;
                break;
            case 'telephone':
                data['number_tel'] = parseInt(value, 10);
                break;
            default:
                data[key] = value;
                break;
        }
    });
    console.log('Data to send:', JSON.stringify(data));

    // CALL API TO SEND THE DATA
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            handleError(response.status, errorData.detail);
        } else {
            const data = await response.json();
            console.log('Success:', data);
            alert('User registered successfully!');
            location.href = '/page_autentication';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again later.');
    }
});


// HANDLE THE INVALIDATED FIELDS IN THE PROCESS OF REGISTER
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


// FETCH AND LOAD PROVINCES ON PAGE LOAD
fetch('/app/static/js/provinces.json')
.then(response => response.json())
.then(provinces => {
    const selectElement = document.getElementById('province');

    provinces.forEach(province => {
        const option = document.createElement('option');
        option.value = province;
        option.textContent = province;
        selectElement.appendChild(option);
    });
})
.catch(error => console.error('Error loading provinces:', error));