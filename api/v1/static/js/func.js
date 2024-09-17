document.addEventListener('DOMContentLoaded', () => {
    // Hide and Show Password
    const togglePassword = document.querySelector('#togglePassword');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password = document.querySelector('#password');
    const conf_password = document.querySelector('#conf_password');
    const eyeIcon = document.querySelector('#eyeIcon');
    const eyeIcon2 = document.querySelector('#eyeIcon2');

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
    if (togglePassword2) {
        togglePassword2.addEventListener('click', (e) => {
            // toggle the type attribute
            const type = conf_password.getAttribute('type') === 'password' ? 'text' : 'password';
            conf_password.setAttribute('type', type);

            // toggle the eye icon
            if (type === 'password') {
                eyeIcon2.classList.remove('fa-eye-slash');
                eyeIcon2.classList.add('fa-eye');
            } else {
                eyeIcon2.classList.remove('fa-eye');
                eyeIcon2.classList.add('fa-eye-slash');
            }
        });
    }


    // Function to hide the element after a delay
    function hideElementAfterDelay(elementId, delay) {
        setTimeout(function () {
            let element = document.getElementById(elementId);
            if (element) {
                element.style.transition = "opacity 1s ease-out";
                element.style.visibility = "hidden";
                setTimeout(function () {
                    // element.style.display = "none";
                }, 1000);
            }
        }, delay);
    }
    hideElementAfterDelay("msg", 4000);


    // For formatted phone number input
    // Initialize intl-tel-input for the first and emergency contact's phone number
    if (typeof window.intlTelInput === 'function') {
        let itiPhone, itiEmergencyPhone;

        let phoneInput = document.querySelector("#phone_number");
        if (phoneInput) {
            itiPhone = window.intlTelInput(phoneInput, {
                initialCountry: "ng",
                separateDialCode: true,
                utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
            });
        }

        let emergencyPhoneInput = document.querySelector("#emg_contact_phone");
        if (emergencyPhoneInput) {
            itiEmergencyPhone = window.intlTelInput(emergencyPhoneInput, {
                initialCountry: "ng",
                separateDialCode: true,
                utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
            });
        }

        let form = document.querySelector("form");
        if (form) {
            form.addEventListener("submit", function (event) {
                // event.preventDefault(); // Prevent form submission for debugging

                if (itiPhone) {
                    let fullPhoneNumber = itiPhone.getNumber();
                    if (phoneInput) phoneInput.value = fullPhoneNumber;
                }

                if (itiEmergencyPhone) {
                    let fullEmergencyPhoneNumber = itiEmergencyPhone.getNumber();
                    if (emergencyPhoneInput) emergencyPhoneInput.value = fullEmergencyPhoneNumber;
                }
            });
        }
    }
});