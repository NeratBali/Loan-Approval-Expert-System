document.addEventListener("DOMContentLoaded", () => {
    const ctaButton = document.getElementById("cta-button");
    const nav = document.querySelector("nav");
    const heroText = document.querySelector(".hero-text");
    const modal = document.querySelector(".modal");
    const loginLink=document.getElementById("login-link");
    const modalContent = document.querySelector(".modal-content");
    const signupForm = document.getElementById("signup-form");


    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("show");
            modal.classList.add("hidden");
            nav.classList.remove("animate-out");
            heroText.classList.remove("animate-out2");
            ctaButton.classList.remove("animate-out");
            nav.classList.add("animate-in");
            heroText.classList.add("animate-in2");
            ctaButton.classList.add("animate-in");

        }
    });

    ctaButton.addEventListener("click", (e) => {
        e.preventDefault();
        nav.classList.remove("animate-in");
        heroText.classList.remove("animate-in2");
        ctaButton.classList.remove("animate-in");
        nav.classList.add("animate-out");
        heroText.classList.add("animate-out2");
        ctaButton.classList.add("animate-out");
        modal.classList.remove("hidden");
        modal.classList.add("show");
    });
    loginLink.addEventListener("click", (e) => {
        e.preventDefault();
        modalContent.classList.add("hidden");
        modalContent.innerHTML = `
            <h2>Login</h2>
            <form id="login-form" style="justify-content: center;align-items: center; display: flex;flex-direction: column;">
                <input id="email" name="email" type="email" placeholder="Email Address" required>
                <input id="password" name="password" type="password" placeholder="Password" required>
                <button type="submit">Login</button>
                <p>Don't have an account? <a href="#" id="signup-link">Sign Up</a></p>
            </form>
        `;
        modalContent.classList.remove("hidden");
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const formData = new FormData(loginForm);
                
                fetch('/login', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    } else {
                        return response.json();
                    }
                })
                .then(data => {
                    if (data && !data.success) {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Login failed. Please try again.');
                });
            });
        }

            // Add event listener for switching back to the sign-up form
            const signupLink = document.getElementById("signup-link");
            signupLink.addEventListener("click", (e) => {
                e.preventDefault();
                // Fade out the current content
                modalContent.classList.add("hidden");

                // Wait for the fade-out transition to complete
                // Replace the login form with the sign-up form
                modalContent.innerHTML = `
                    <h2>Sign Up</h2>
                    <form id="signup-form" style="justify-content: center; align-items: center; display: flex; flex-direction: column;">
                        <input id="firstName" name="firstName" type="text" placeholder="First Name" required>
                        <input id="lastName" name="lastName" type="text" placeholder="Last Name" required>
                        <input id="email" name="email" type="email" placeholder="Email Address" required>
                        <input id="password" name="password" type="password" placeholder="Password" required>
                        <button type="submit">Sign Up</button>
                        <p>Already have an account? <a href="#" id="login-link">Login</a></p>
                    </form>
                `;

                    // Fade in the new content
                modalContent.classList.remove("hidden");
                                        // Reattach the event listener for switching to login
                document.getElementById("login-link").addEventListener("click", (e) => {
                    e.preventDefault();
                    loginLink.click();
                });
                }, 500);
            });
            signupForm.addEventListener("submit", (e) => {
                e.preventDefault();
                const formData = new FormData(signupForm);
            
                fetch("/signup", {
                    method: "POST",
                    body: formData,
                })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        alert(data.message);
                        // Switch to login form after successful signup
                        loginLink.click();
                    } else {
                        alert(`Error: ${data.message}`);
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                });
            });

 
});
