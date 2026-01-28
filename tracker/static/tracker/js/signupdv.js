const passwordInput = document.querySelector('input[name="password"]');
const strengthText = document.getElementById('password-strength');
passwordInput.addEventListener('blur',()=> {
    const value = passwordInput.value;
    if (!value) {
        strengthText.textContent = "";
        return;
    }
    if (value.length < 8) {
        strengthText.textContent = "Weak (min 8 characters)";
        strengthText.className = "text-red-500 text-sm";
    }
    else if(!/[A-Z]/.text(value) || !/[0-9]/.test(value)) {
        strengthText.textContent = "Medium (add uppercase & numbers)";
        strengthText.className = "text-orange-500 text-sm";
    }
    else {
        strengthText.textContent = "Strong password";
        strengthText.className = "text-green-500";
    }
});

passwordInput.addEventListener("input",() => {
    strengthText.textContent = "";
});