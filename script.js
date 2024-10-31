const prodUrl = "https://almaszaurbekov.github.io/itcareer-cvbuilder";

function startTimer(duration, display) {
    let timer = duration;
    const interval = setInterval(() => {
        let seconds = parseInt(timer, 10);

        display.textContent = `${seconds}s`; // Update the display

        if (--timer < 0) {
            clearInterval(interval); // Stop timer when it reaches 0
            document.getElementById('loader').style.display = 'none';
            display.style.display = 'none';
        }
    }, 1000);
}

document.getElementById('inputForm')?.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const textInput = document.getElementById('textInput').value;
    const fileInput = document.getElementById('fileInput').files[0];

    // Check if a file is selected and if it's a PDF
    if (fileInput) {
        const fileType = fileInput.type; // Get the MIME type
        const fileExtension = fileInput.name.split('.').pop().toLowerCase(); // Get the file extension

        // Validate file type
        if (fileType !== 'application/pdf' && fileExtension !== 'pdf') {
            alert('Please upload a valid PDF file.'); // Alert user for invalid file type
            return; // Stop further execution
        }
    }

    const formData = new FormData(); // Create a FormData object
    formData.append('job_vacancy_description', textInput); // Append the text input
    if (fileInput) {
        formData.append('pdf_resume', fileInput); // Append the file input if any
    }

    const timerDisplay = document.getElementById('timer');
    timerDisplay.style.display = 'inline';
    startTimer(25, timerDisplay);
    document.getElementById('resultOutput').innerHTML = '';

    const token = localStorage.getItem('jwtToken');

    // Make the API request
    fetch('http://127.0.0.1:5000/upgrade_bullet_points', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData // Send the FormData as the request body
    })
    .then(response => response.json())
    .then(data => {
        timerDisplay.style.display = 'none';

        // Handle the response data
        const message = data.message;

        // Split the message into an array of bullet points by newline character
        const bulletPoints = message.split('\n').map(item => item.replace(/^-\s*/, '').trim()).filter(item => item !== '');

        // Create a <ul> element
        const ul = document.createElement('ul');

        // Iterate over bullet points and create <li> for each
        bulletPoints.forEach(point => {
            const li = document.createElement('li');
            li.textContent = point; // Set the text content
            ul.appendChild(li);
        });

        const outputDiv = document.getElementById('resultOutput');
        outputDiv.innerHTML = ''; // Clear previous content
        outputDiv.appendChild(ul)
    })
    .catch(error => {
        timerDisplay.style.display = 'none';
        console.error('Error:', error);
        document.getElementById('resultOutput').innerHTML = `<p>Error occurred: ${error.message}</p>`;
    });
});

// Function to handle Login
document.getElementById('loginForm')?.addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('jwtToken', data.access_token); // Save token in localStorage
            window.location.href = prodUrl;
        } else {
            alert('Login failed. Please check your credentials.');
        }
    })
    .catch(error => console.error('Error:', error));
});

// Function to handle Registration
document.getElementById('registerForm')?.addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('jwtToken', data.access_token);
            window.location.href = prodUrl;
        } else {
            alert('Registration failed.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('logout')?.addEventListener('click', function(event) {
    localStorage.removeItem('jwtToken');
    window.location.href = `${prodUrl}/pages/login`;
});

// Check if the current page is "/" and the token is none
if (window.location.href === prodUrl) {
    if(localStorage.getItem('jwtToken') == null) {
        window.location.href = `${prodUrl}/pages/login`;
    }
}

if (window.location.href === `${prodUrl}/pages/login`) {
    if(localStorage.getItem('jwtToken') != null) {
        window.location.href = prodUrl;
    }
}

if (window.location.href === `${prodUrl}/pages/register`) {
    if(localStorage.getItem('jwtToken') != null) {
        window.location.href = window.location.href = prodUrl;
    }
}