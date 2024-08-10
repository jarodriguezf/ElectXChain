document.getElementById('autenticationForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const data = {};

    formData.forEach((value, key) => {
        switch (key) {
            case 'dni':
                data['dni'] = value;
                break;
            
            case 'telephone':
                data['number_tel'] = parseInt(value, 10);
                break;
        }
    });
    console.log('Data to send:', JSON.stringify(data));

    // CALL API TO VALIDATE THE DATA
    try {
        const response = await fetch('/autentication', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (response.redirected) {
            console.log('Success in the redirected');
            alert('User exists in the system!');
            window.location.href = response.url;

        }else {
            const errorData = await response.text();
            handleError(response.status, errorData);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again later.');
    }
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