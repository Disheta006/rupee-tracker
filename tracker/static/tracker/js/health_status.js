function updateHealthStatus(spent,totalBudget) {
    const percentage = totalBudget > 0 ? Math.min((spent/ totalBudget)*100,100) : 0;
    const circle  = document.getElementById('healthCircle');
    const text = document.getElementById('healthMessage');
    const offset = 251.2 - (percentage/100)*251.2;
    circle.style.strokeDashoffset = offset;
    text.innerText = `${Math.round(percentage)}%`;
    if(percentage == 0) {
        circle.setAttribute('class','text-gray-500 stroke-current transition-all duration-700');
        msg.innerText = ".";
        msg.className = "text-red-600 font-bold leading-relaxed";
    }
    if (percentage >= 90) {
        circle.setAttribute('class','text-red-500 stroke-current transition-all duration-700');
        msg.innerText = "Danger! You have exhausted nearly your entire budget.";
        msg.className = "text-red-600 font-bold leading-relaxed";
    }
    else if (percentage >= 70) {
        circle.setAttribute('class','text-orange-500 stroke-current transition-all duration-700');
        msg.innerText = "Warning: Your spending is approching your threshold.";
        msg.className = "text-orange-600 font-bold leading-relaxed";
    }
    else {
        circle.setAttribute('class','text-green-500 stroke-current transition-all duration-700');
        msg.innerText = "Safe! Your financial health is currently in excellent standiing.";
        msg.className = "text-[#5f8724] font-bold leading-relaxed";
    }
}