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
                <input id="form-input" type="email" placeholder="Email Address" required>
                <input id="form-input" type="password" placeholder="Password" required>
                <button type="submit">Login</button>
                <p>Don't have an account? <a href="#" id="signup-link">Sign Up</a></p>
            </form>
        `;
        modalContent.classList.remove("hidden");

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
                    <form style="justify-content: center; align-items: center; display: flex; flex-direction: column;">
                        <input id="form-input" type="text" placeholder="First Name" required>
                        <input id="form-input" type="text" placeholder="Last Name" required>
                        <input id="form-input" type="email" placeholder="Email Address" required>
                        <input id="form-input" type="password" placeholder="Password" required>
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
            if (signupForm) {
                signupForm.addEventListener("submit", (e) => {
                    e.preventDefault(); // Prevent the default form submission
        
                    // Collect form data
                    const formData = new FormData(signupForm);
        
                    // Send the data via AJAX
                    fetch("/signup", {
                        method: "POST",
                        body: formData,
                    })
                        .then((response) => response.json())
                        .then((data) => {
                            if (data.success) {
                                // Show success message
                                alert(data.message);
                        // Optionally clear the form
                        signupForm.reset();
                    } else {
                        // Show error message
                        alert(`Error: ${data.message}`);
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                });
            });
        }
            
    });
