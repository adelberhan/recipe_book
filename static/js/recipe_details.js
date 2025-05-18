const pathSegments = window.location.pathname.split("/");
const recipeId = pathSegments[2];
const currentUser = localStorage.getItem("username");

if (!recipeId) {
  
  document.body.innerHTML = '<p style="color:red;">No recipe ID provided in the URL</p>';
} else {
  fetch(`/api/recipes/${recipeId}`)
    .then((res) => {
      if (!res.ok) throw new Error("Recipe not found");
      return res.json();
    })
    .then((data) => {
      // Populate recipe details
      document.getElementById("recipe-name").textContent = data.name;
      document.getElementById("recipe-image").src = data.image_url;
      document.getElementById("created-by").textContent = data.created_by;
      document.getElementById("prep-time").textContent = data.prep_time;
      document.getElementById("cook-time").textContent = data.cook_time;
      document.getElementById("created-at").textContent = new Date(data.created_at).toLocaleString();
      document.getElementById("updated-at").textContent = new Date(data.updated_at).toLocaleString();
      document.getElementById("ingredients-list").textContent = data.ingredients;
      document.getElementById("instructions-text").textContent = data.instructions;

      // Add action buttons if current user is the creator
      if (currentUser === data.created_by) {
        const actionsHTML = `
          <div class="recipe-actions">
            <a href="/recipes/edit/${recipeId}" class="btn btn-edit">
              <i class="fa-solid fa-pen-to-square"></i> Edit
            </a>
            <button class="btn btn-delete" data-recipe-id="${recipeId}">
              <i class="fa-solid fa-trash"></i> Delete
            </button>
          </div>
        `;
        
        // Insert buttons - choose where you want them to appear
        // Option 1: After the recipe-info div
        document.querySelector('.recipe-info').insertAdjacentHTML('beforeend', actionsHTML);
        
        // Or Option 2: Before the ingredients-instructions div
        // document.querySelector('.ingredients-instructions').insertAdjacentHTML('beforebegin', actionsHTML);

        // Add delete event listener
        document.querySelector('.btn-delete').addEventListener('click', async (e) => {
          e.preventDefault();
          if (confirm("Are you sure you want to delete this recipe?")) {
            try {
              const deleteRes = await fetch(`/api/recipes/${recipeId}`, {
                method: "DELETE"
              });
              
              if (deleteRes.ok) {
                window.location.href = "/recipes";
              } else {
                throw new Error("Failed to delete recipe");
              }
            } catch (err) {
              console.error("Delete error:", err);
              alert("Failed to delete recipe. Please try again.");
            }
          }
        });
      }
    })
    .catch((err) => {
      document.body.innerHTML = `<p style="color:red; text-align: center;">Error: ${err.message}</p>`;
    });
}