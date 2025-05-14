// const recipeId = new URLSearchParams(window.location.search).get("id");
const pathSegments = window.location.pathname.split("/");
const recipeId = pathSegments[2];
if (!recipeId) {
  document.body.innerHTML = '<p style="color:red;">No recipe ID provided in the URL</p>';
  console.log(recipeId);
} else {
  fetch(`/api/recipes/${recipeId}`)
  .then((res) => {
      if (!res.ok) throw new Error("Recipe not found");
      return res.json();
    })
    .then((data) => {
        console.log(data)
      document.getElementById("recipe-name").textContent = data.name;
      document.getElementById("recipe-image").src = data.image_url;
      document.getElementById("created-by").textContent = data.created_by;
      document.getElementById("prep-time").textContent = data.prep_time;
      document.getElementById("cook-time").textContent = data.cook_time;
      document.getElementById("created-at").textContent = new Date(data.created_at).toLocaleString();
      document.getElementById("updated-at").textContent = new Date(data.updated_at).toLocaleString();
      document.getElementById("ingredients-list").textContent = data.ingredients;
      document.getElementById("instructions-text").textContent = data.instructions;
    })
    .catch((err) => {
      document.body.innerHTML = `<p style="color:red; text-align: center;">Error: ${err.message}</p>`;
    });
}

// if (!recipeId) {
//   document.body.innerHTML = '<p style="color:red;">No recipe ID provided in the URL</p>';
// } else {
//   fetch(`/api/recipes/${recipeId}`)
//     .then((res) => {
//       if (!res.ok) throw new Error("Recipe not found");
//       return res.json();
//     })
//     .then((data) => {
//       document.getElementById("recipe-name").textContent = data.name;
//       document.getElementById("recipe-image").src = data.image_url;
//       document.getElementById("created-by").textContent = data.created_by;
//       document.getElementById("prep-time").textContent = data.prep_time;
//       document.getElementById("cook-time").textContent = data.cook_time;
//       document.getElementById("created-at").textContent = new Date(data.created_at).toLocaleString();
//       document.getElementById("updated-at").textContent = new Date(data.updated_at).toLocaleString();
//       document.getElementById("ingredients-list").textContent = data.ingredients;
//       document.getElementById("instructions-text").textContent = data.instructions;
//     })
//     .catch((err) => {
//       document.body.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
//     });
// }
