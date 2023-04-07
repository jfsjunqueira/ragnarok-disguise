document.addEventListener('DOMContentLoaded', () => {
    const monsterNameInput = document.getElementById('monster-name');
    
    // Clear the input field and set focus on page load
    monsterNameInput.value = '';
    monsterNameInput.focus();
  
    // Clear the input field and set focus after submitting the form
    const form = document.querySelector('form');
    form.addEventListener('submit', () => {
      setTimeout(() => {
        monsterNameInput.value = '';
        monsterNameInput.focus();
      }, 100);
    });
  });
  