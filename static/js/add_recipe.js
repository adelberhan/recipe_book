// document.getElementById("recipe-form").addEventListener("submit", function (event) {
//   event.preventDefault();

//   const recipeId = document.getElementById("recipe-id").value;
//   const recipeData = {
//     name: document.getElementById("recipe-name").value,
//     image_url: document.getElementById("recipe-image").value,
//     prep_time: document.getElementById("prep-time").value,
//     cook_time: document.getElementById("cook-time").value,
//     ingredients: document.getElementById("ingredients-list").value,
//     instructions: document.getElementById("instructions-text").value,
//   };

//   const method = recipeId ? "PUT" : "POST";
//   const url = recipeId ? `/recipes/edit/${recipeId}` : `/api/recipes`;
// console.log(method)
//   fetch(url, {
//     method: method,
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(recipeData),
//   })
//     .then((res) => {
//       if (!res.ok) throw new Error("Failed to save recipe");
//       return res.json();
//     })
//     .then((data) => {
//       alert(recipeId ? "Recipe updated!" : "Recipe added!");
//       console.log(data.recipe);
//       // Optionally: reset form or redirect
//     })
//     .catch((err) => {
//       console.error(err);
//       alert("Error saving recipe.");
//     });
// });
function loadRecipeToForm(recipeId) {
  fetch(`/api/recipes/${recipeId}`)
    .then((res) => res.json())
    .then((data) => {
      const recipe = data;
      document.getElementById("recipe-id").value = recipe.id;
      document.getElementById("recipe-name").value = recipe.name;
      document.getElementById("recipe-image").value = recipe.image_url;
      document.getElementById("prep-time").value = parseInt(recipe.prep_time);
      document.getElementById("cook-time").value = parseInt(recipe.cook_time);
      document.getElementById("ingredients-list").value = recipe.ingredients;
      document.getElementById("instructions-text").value = recipe.instructions;
    });
}

// //   event.preventDefault(); // يمنع إرسال الفورم تلقائيًا
// // document.getElementById("recipe-form").addEventListener("submit", function (event) {

// //   const recipe_data = {
// //     name: document.getElementById("recipe-name").value,
// //     image_url: document.getElementById("recipe-image").value,
// //     prep_time: document.getElementById("prep-time").value,
// //     cook_time: document.getElementById("cook-time").value,
// //     ingredients: document.getElementById("ingredients-list").value,
// //     instructions: document.getElementById("instructions-text").value,
// //     // created_by: document.getElementById("created-by").value,
// //     // created_at: new Date().toISOString(),
// //     // updated_at: new Date().toISOString(),
// //     created_by: "Adel", // أو خذها من input مخفي أو من المستخدم
// //   };

// //   fetch(`/api/recipes`, {
// //     method: "POST",
// //     headers: {
// //       "Content-Type": "application/json",
// //     },
// //     body: JSON.stringify(recipe_data),
// //   })
// //     .then((res) => {
// //       if (!res.ok) throw new Error("Failed to create recipe");
// //       return res.json();
// //     })
// //     .then((data) => {
// //       alert("Recipe created successfully!");
// //       console.log(data.recipe);
// //     })
// //     .catch((error) => {
// //       console.error("Error:", error);
// //       alert("Error creating recipe");
// //     });
// //   window.location.href = "/home";
// // });

document.getElementById("recipe-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const userName = localStorage.getItem("username");
  const recipeId = document.getElementById("recipe-id").value;
  const method = recipeId ? "PUT" : "POST";
  const url = recipeId ? `/api/recipes/${recipeId}` : "/api/recipes";
  const recipeData = {
    
    name: document.getElementById("recipe-name").value,
    image_url: document.getElementById("recipe-image").value,
    prep_time: document.getElementById("prep-time").value,
    cook_time: document.getElementById("cook-time").value,
    ingredients: document.getElementById("ingredients-list").value,
    instructions: document.getElementById("instructions-text").value,
    created_by: userName, // required only for POST
  };

  if (method === "PUT") delete recipeData.created_by;

  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(recipeData),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to save recipe");
      return res.json();
    })
    .then((data) => {
      alert(recipeId ? "Recipe updated!" : "Recipe added!");
      window.location.href = "/recipes"; // redirect to the recipes page
      // redirect if needed
    })
    .catch((err) => {
        
        alert("Something went wrong.");
    });
    
});

window.addEventListener("DOMContentLoaded", () => {
  const match = window.location.pathname.match(/\/recipes\/edit\/(.+)/);
  if (match) {
    const recipeId = match[1];
    loadRecipeToForm(recipeId);
  }
});