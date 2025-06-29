document.addEventListener('DOMContentLoaded', () => {
  const roleRadios = document.querySelectorAll('input[name="role"]');
  const createBtn = document.getElementById('createAccountBtn');

  let selectedRole = null;

  roleRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      selectedRole = radio.value;
      createBtn.disabled = false;
    });
  });

  createBtn.addEventListener('click', () => {
    if (selectedRole === 'user') {
      window.location.href = 'register_users.html'; // обычный пользователь
    } else if (selectedRole === 'doctor') {
      window.location.href = 'For_Doctors/doctor_register.html'; // врач
    }
  });
});
