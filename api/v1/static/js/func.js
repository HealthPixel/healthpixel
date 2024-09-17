document.addEventListener('DOMContentLoaded', (e) => {
    // Hide and Show Password
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    const eyeIcon = document.querySelector('#eyeIcon');

    if (togglePassword) {
        togglePassword.addEventListener('click', (e) => {
            // toggle the type attribute
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);

            // toggle the eye icon
            if (type === 'password') {
                eyeIcon.classList.remove('fa-eye-slash');
                eyeIcon.classList.add('fa-eye');
            } else {
                eyeIcon.classList.remove('fa-eye');
                eyeIcon.classList.add('fa-eye-slash');
            }
        });
    }


    // Function to hide the element after a delay
    function hideElementAfterDelay(elementId, delay) {
        setTimeout(function () {
            var element = document.getElementById(elementId);
            if (element) {
                element.style.transition = "opacity 1s ease-out";
                element.style.visibility = "hidden";
                setTimeout(function () {
                    // element.style.display = "none";
                }, 1000);
            }
        }, delay);
    }
    hideElementAfterDelay("msg", 1000);


    // For formatted phone number input
    // Initialize intl-tel-input for the first and emergency contact's phone number
    var phoneInput = document.querySelector("#phone_number");
    var emergencyPhoneInput = document.querySelector("#emg_contact_phone");
    if (phoneInput) {
        var itiPhone = window.intlTelInput(phoneInput, {
            initialCountry: "ng", // Set default country (Nigeria in this example)
            separateDialCode: true,
            utilsScript:
                "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
        });
    }
    if (emergencyPhoneInput) {
        var itiEmergencyPhone = window.intlTelInput(emergencyPhoneInput, {
            initialCountry: "ng", // Set default country (Nigeria in this example)
            separateDialCode: true,
            utilsScript:
                "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
        });
    }

    let docSubmit = document.querySelector("#submit-doc-btn")
    if (docSubmit) {
        docSubmit.addEventListener('submit', () => {
            // Append the full phone number before submitting the form
            var fullPhoneNumber = itiPhone.getNumber();
            var emgFullPhoneNumber = itiEmergencyPhone.getNumber();
            phoneInput.value = fullPhoneNumber;
            emergencyPhoneInput.value = emgFullPhoneNumber;
        })
    }

    let patSubmit = document.querySelector("#submit-pat-btn")
    if (patSubmit) {
        patSubmit.addEventListener('submit', () => {
            // Append the full phone number before submitting the form
            var fullPhoneNumber = itiPhone.getNumber();
            var emgFullPhoneNumber = itiEmergencyPhone.getNumber();
            phoneInput.value = fullPhoneNumber;
            emergencyPhoneInput.value = emgFullPhoneNumber;
        })
    }
});