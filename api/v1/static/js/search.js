document.addEventListener('DOMContentLoaded', function () {
  let debounceTimer;
  let foundPatientId = null;

  // Ensure these buttons are correctly selected
  const searchInput = document.getElementById('search_patient');
  const patientList = document.querySelector('.patient_list');
  const viewPatient = document.querySelector('#viewPatient')

  searchInput.addEventListener('input', function () {
    viewPatient.textContent = searchInput.value.trim() !== '' ? 'Hide Patient' : 'View All Patients';
    const searchQuery = this.value.trim();
    clearTimeout(debounceTimer);

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
                const dateOfBirth = new Date(patient.date_of_birth);
                const formattedDate = dateOfBirth.toLocaleDateString('en-GB');
                const patientItem = `
                <div class="card p-3 mb-2">
                  <h5 class="card-title">${patient.first_name} ${patient.last_name}</h5>
                  <p class="card-text">Email: ${patient.email}</p>
                  <p class="card-text">ID: ${patient.id}</p>
                  <p class="card-text">Address: ${patient.address}</p>
                  <p class="card-text">Date of Birth: ${formattedDate}</p>
                  <p class="card-text">Gender: ${patient.gender}</p>
                  <p class="card-text">Blood Group: ${patient.blood_group}</p>
                  <div class="row justify-content-between">
                    <div class="col-md-5">
                      <button class="btn btn-success btn-large py-2 mb-3 btn-view" data-id="${patient.id}">View Patient's Records</button>
                    </div>
                    <div class="col-md-5">
                      <button class="btn btn-success btn-large py-2 btn-update" data-id="${patient.id}">Update Patient's Records</button>
                    </div>
                  </div>
                </div>
                `;
                patientList.innerHTML += patientItem;
              });
            } else {
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

  // Event delegation
  patientList.addEventListener('click', function (event) {
    if (event.target.classList.contains('btn-view')) {
      const patientId = event.target.getAttribute('data-id');
      if (patientId) {
        window.location.href = `/api/v1/doctor/patients/${patientId}/view_patient_records`;
      }
    } else if (event.target.classList.contains('btn-update')) {
      const patientId = event.target.getAttribute('data-id');
      if (patientId) {
        window.location.href = `/api/v1/doctor/patients/${patientId}/update_patient_records`
      }
    }
  });
});
