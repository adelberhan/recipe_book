// This script handles the logout button click
const logoutButton = document.getElementById("logout-button");
const userName = document.getElementById("user-name-active");
const localStorageUsername = localStorage.getItem("username") || null;
document.getElementById("logout-button").addEventListener("click", async function (e) {
  e.preventDefault();

  try {
    const response = await fetch("/logout", {
      method: "GET",
    });

    const data = await response.json();

    if (data.success) {
      localStorage.removeItem("username");
    //   localStorage.removeItem("userData");
      window.location.href = "/recipes"; // redirect to login page
      userName.className = "user-name-active"; // Change class name
    //   userName.innerText = userName.innerText = localStorage.getItem("username"); // Change button text
    } else {
      console.error(data.message || "Logout failed.");
    }
  } catch (err) {
    console.error(err);
  }
});

if (localStorage.getItem("username") === null && logoutButton) {
  logoutButton.className = "btn-login"; // Change class name
  logoutButton.innerText = "Login"; // Change button text
  logoutButton.addEventListener("click", function () {
    window.location.href = "/login";
  });
}

if ( localStorage.getItem("username") && userName) {
  userName.innerText = 'HI ' + localStorage.getItem("username").toLocaleUpperCase()+' 😃';
}