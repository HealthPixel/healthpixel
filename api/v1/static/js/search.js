document.addEventListener('DOMContentLoaded', function () {
  let debounceTimer;
  let foundPatientId = null;

  // Ensure these buttons are correctly selected
  const viewButton = document.getElementById('btn_view_patient_records');
  const updateButton = document.getElementById('btn_update_patient_records');
  const searchInput = document.getElementById('search_patient');

  searchInput.addEventListener('input', function () {
    const searchQuery = this.value.trim();

    clearTimeout(debounceTimer);

    const patientList = document.querySelector('.patient_list');
    if (searchQuery.length < 3) {
      patientList.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(() => {
      if (searchQuery.length > 2) {
        fetch(`/api/v1/doctor/patients/search?query=${encodeURIComponent(searchQuery)}`)
          .then((response) => response.json())
          .then((data) => {
            patientList.innerHTML = '';
            foundPatientId = null; // Reset found Patient ID

            if (data.length > 0) {
              data.forEach((patient) => {
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
                foundPatientId = patient.id; // Make sure patient ID is set
              });
            } else {
              foundPatientId = null;
              patientList.innerHTML = '<p class="text-danger">No patient found</p>';
            }
          })
          .catch((error) => {
            console.error('Error fetching patient data:', error);
            patientList.innerHTML = '<p class="text-danger">An error occurred while fetching patient data.</p>';
          });
      }
    }, 300); // Delay by 300ms
  });

  // Handle the "View Patient's Record" button
  viewButton.addEventListener('click', function () {
    if (foundPatientId) {
      // Redirect to the view patient record page with the patient's ID
      window.location.href = `/api/v1/doctor/patients/${foundPatientId}/view_patient_records`;
    } else {
      // If no patient was searched, show an alert
      alert('Please search for a patient to view their records.');
    }
  });

  // Handle the "Update Patient's Record" button
  updateButton.addEventListener('click', function () {
    if (foundPatientId) {
      // Redirect to the update page with the patient's ID
      window.location.href = `/api/v1/doctor/patients/${foundPatientId}/update_patient_records`;
    } else {
      // If no patient was searched, show an alert
      alert('Please search for a patient before updating their records.');
    }
  });
});
