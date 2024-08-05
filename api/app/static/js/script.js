
// EXTRACT REGISTER FORM AND SEND IT TO THE API
document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const data = {};

    formData.forEach((value, key) => {
        // Convert field names to match UserSchema
        switch (key) {
            case 'fullName':
                data['name'] = value;
                break;
            case 'dni':
                data['nie'] = value;
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

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.detail || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});