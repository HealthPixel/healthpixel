// View all Paatients

document.addEventListener('DOMContentLoaded', () => {
    const viewPatient = document.querySelector('#viewPatient')
    const patientList = document.querySelector('.patient_list');
    const searchInput = document.getElementById('search_patient');

    viewPatient.addEventListener('click', async (ev) => {
        ev.preventDefault();
        if (patientList.innerHTML !== '') {
            patientList.innerHTML = '';
            viewPatient.textContent = 'View All Patient';
            searchInput.value = '';
        }
        else {
            const response = await fetch(`/api/v1/doctor/patients`)
            if (response.ok) {
                const data = await response.json();
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
                            </div>`;
                        patientList.innerHTML += patientItem;
                        viewPatient.textContent = 'Hide All Patients';
                    });
                } else {
                    patientList.innerHTML = '<p class="text-danger">No patient found</p>';
                } // Data Lenght IF
            } // Response IF
        }
    });
});