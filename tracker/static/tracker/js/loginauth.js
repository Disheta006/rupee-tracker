document.getElementById("login-form").addEventListener("submit",function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    fetch(loginURL, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
        })
        .then(res => res.json())
        .then(data => {
            const msg = document.getElementById("login-msg");
            if(data.success) {
               window.location.href = data.redirect_url;
            }
        });
});