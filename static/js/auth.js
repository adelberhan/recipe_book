async function handleAuth({ formId, url, fields, successRedirect }) {
  document.getElementById(formId).addEventListener("submit", async function (e) {
    e.preventDefault();

    const errorBox = document.querySelector(`#${formId} #error-message`);
    const values = {};

    // Gather input values and trim
    for (const field of fields) {
      const input = document.getElementById(field);
      if (!input) continue;
      values[field] = input.value.trim();
    }

    // Extra check for register (password match)
    if (formId === "register-form" && values["password"] !== values["re-password"]) {
      errorBox.textContent = "Passwords do not match.";
      return;
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: values["username"] || values["email"], // unify username/email
          password: values["password"],
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Store username in localStorage
        localStorage.setItem("username", values["username"] || values["email"]);

      }

      if (data.success) {
        window.location.href = successRedirect;
      } else {
        errorBox.textContent = data.message || "Authentication failed.";
      }
    } catch (err) {
      console.error(err);
      errorBox.textContent = "An error occurred. Please try again.";
    }
  });
}

// handles the logout button click
async function setupLogout() {
  const logoutButton = document.getElementById("logout-button");
  const userName = document.getElementById("user-name-active");
  const storedUsername = localStorage.getItem("username");

  // Update UI based on login state
  if (storedUsername && userName) {
    userName.textContent = `HI ${storedUsername.toUpperCase().match(/^([^@]+)/)[0]} 😃`;
  }

  if (!logoutButton) return; // Exit if no logout button found

  if (storedUsername) {
    // User is logged in - setup logout functionality
    logoutButton.addEventListener("click", async function (e) {
      e.preventDefault();

      try {
        const response = await fetch("/logout", { method: "GET" });
        const data = await response.json();

        if (data.success) {
          localStorage.removeItem("username");
          window.location.reload();
          setTimeout(() => {
          }, 500);  
        } else {
          console.error("Logout failed:", data.message);
          alert("Logout failed. Please try again.");
        }
      } catch (err) {
        console.error("Network error:", err);
        alert("Network error during logout.");
      }
    });
  } else {
    // User is not logged in - change to login button
    logoutButton.className = "btn-login";
    logoutButton.textContent = "Login";
    logoutButton.addEventListener("click", function () {
      window.location.href = "/login";
    });
  }
}

// Handles the authentication logic for login and registration forms
document.addEventListener("DOMContentLoaded", function () {
  // Only run register logic if on the register page  
  if (document.getElementById("register-form")) {
    handleAuth({
      formId: "register-form",
      url: "/api/register",
      fields: ["username", "password", "re-password"],
      successRedirect: "/recipes",
    });
  }

  // Only run login logic if on the login page
  if (document.getElementById("login-form")) {
    handleAuth({
      formId: "login-form",
      url: "/login",
      fields: ["email", "password"],
      successRedirect: "/recipes",
    });
  }
});

// This script handles the logout button click
// Run when DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  setupLogout();
});
