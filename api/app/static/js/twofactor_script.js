document.getElementById('twofactorForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const data = {
        token: formData.get('token')
    };
    console.log('Data to send:', JSON.stringify(data));

    // CALL API TO VALIDATE THE TOKEN
    try {
        const response = await fetch('/validation_token_2fa', {
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
            alert('Token activated!');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again later.');
    }
});

document.getElementById('resendCode').addEventListener('click', async function(event) {
    event.preventDefault(); 
    const number_tel = new URLSearchParams(window.location.search).get('number_tel');
    
    if (!number_tel) {
        alert('Phone number is missing.');
        return;
    }

    const data = {
        number_tel: parseInt(number_tel)
    };
    
    try {
        const response = await fetch('/recive_sms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            handleError(response.status, errorData);
        } else {
            const responseData = await response.json();
            console.log('Success:', responseData);
            alert('Code has been resent!');
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