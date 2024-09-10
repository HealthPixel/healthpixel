let debounceTimer;
document.getElementById('search_patient').addEventListener('input', function () {
  const searchQuery = this.value;

  clearTimeout(debounceTimer); // Clear previous timer

  // Clear patient list if the input is empty or too short
  const patientList = document.querySelector('.patient_list');
  if (searchQuery.length < 3) {
    patientList.innerHTML = ''; // Clear the patient list
    return; // Exit the function if the query is less than 3 characters
  }

  debounceTimer = setTimeout(() => {
    if (searchQuery.length > 2) { // Start searching after 3 characters
      fetch(`/api/v1/doctor/patients/search?query=${encodeURIComponent(searchQuery)}`)
        .then(response => response.json())
        .then(data => {
          patientList.innerHTML = '';

          if (data.length > 0) {
            data.forEach(patient => {
              const patientItem = `
              <div class="card p-3 mb-2">
                <h5 class="card-title">${patient.first_name} ${patient.last_name}</h5>
                <p class="card-text">Email: ${patient.email}</p>
                <p class="card-text">ID: ${patient.id}</p>
                <p class="card-text">Address: ${patient.address}</p>
                <p class="card-text">Blood Group: ${patient.blood_group}</p>
                <p class="card-text">Date of Birth: ${patient.date_of_birth}</p>
                <p class="card-text">Gender: ${patient.gender}</p>
                <p class="card-text">Phone Number: ${patient.phone_number}</p>
                <p class="card-text">Emergency Contact: ${patient.emergency_contact_name} - ${patient.emergency_contact_phone}</p>
                <p class="card-text">Zip Code: ${patient.zipcode}</p>
                <p class="card-text">Created At: ${patient.created_at}</p>
                <p class="card-text">Updated At: ${patient.updated_at}</p>
              </div>
              `;
              patientList.innerHTML += patientItem;
            });
          } else {
            patientList.innerHTML = '<p class="text-danger">No patient found</p>';
          }
        })
        .catch(error => {
          console.error('Error fetching patient data:', error);
        });
    }
  }, 300); // Delay by 300ms
});
