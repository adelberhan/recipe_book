// Global cache for recipes
let allRecipes = [];

async function loadAllRecipes() {
  const container = document.getElementById("recipes-container");
  if (!container) {
    return;
  }
  container.innerHTML = "Loading recipes...";

  try {
    const res = await fetch("/api/recipes");
    if (!res.ok) throw new Error(`An error occurred: ${res.status}`);

    allRecipes = await res.json(); // Store in global cache
    const currentUser = localStorage.getItem("username");

    if (allRecipes.length === 0) {
      container.innerHTML = "No recipes found.";
      return;
    }

    container.innerHTML = "";
    renderRecipes(allRecipes, currentUser);
    setupEventListeners();
  } catch (error) {
    container.innerHTML = "Error loading recipes.";
  }
}

function renderRecipes(recipes, currentUser) {
  const container = document.getElementById("recipes-container");
  container.innerHTML = recipes
    .map(
      (recipe) => `
    <div class="card">
      <div class="image-container">
        <img src="${recipe.image_url}" alt="${recipe.name}" class="recipe-link" data-recipe-id="${recipe.id}">
      </div>
      <div class="content">
        <span class="title recipe-link" data-recipe-id="${recipe.id}">${recipe.name}</span>
        ${
          currentUser === recipe.created_by
            ? `
          <div class="actions">
            <button class="btn btn-delete" data-recipe-id="${recipe.id}">Delete</button>
            <a class="btn btn-edit" href="/recipes/edit/${recipe.id}">Edit</a>
          </div>
        `
            : ""
        }
      </div>
    </div>
  `
    )
    .join("");
}

function setupEventListeners() {
  // Recipe click handler
  document.querySelectorAll(".recipe-link").forEach((link) => {
    link.addEventListener("click", function () {
      window.location.href = `/recipes/${this.dataset.recipeId}`;
    });
  });

  // Delete button handler
  document.querySelectorAll(".btn-delete").forEach((button) => {
    button.addEventListener("click", async function (e) {
      e.stopPropagation();
      const recipeId = this.dataset.recipeId;
      if (confirm("Are you sure you want to delete this recipe?")) {
        try {
          const res = await fetch(`/api/recipes/${recipeId}`, { method: "DELETE" });
          const data = await res.json();
          if (data.success) {
            alert("Recipe deleted successfully.");
            loadAllRecipes(); // Refresh the list
          } else {
            alert("Error deleting recipe: " + (data.message || "Unknown error"));
          }
        } catch (err) {
          alert("Something went wrong while deleting.");
        }
      }
    });
  });
}

function setupSearch() {
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");
  let searchTimeout;

  searchInput?.addEventListener("input", function (e) {
    clearTimeout(searchTimeout);
    const query = e.target.value.trim().toLowerCase();

    if (query.length < 2) {
      searchResults?.classList.remove("show");
      return;
    }

    searchTimeout = setTimeout(() => {
      const filteredRecipes = allRecipes.filter((recipe) => recipe.name.toLowerCase().includes(query));
      displaySearchResults(filteredRecipes);
    }, 300);
  });

  function displaySearchResults(recipes) {
    if (!searchResults) return;

    searchResults.innerHTML =
      recipes.length > 0
        ? recipes
            .map(
              (recipe) => `
          <div class="search-result-item" onclick="window.location.href='/recipes/${recipe.id}'">
            <strong>${recipe.name}</strong>
            <div class="text-sm">${recipe.ingredients.slice(0, 50)}...</div>
          </div>
        `
            )
            .join("")
        : '<div class="search-result-item">No matching recipes found</div>';

    searchResults.classList.toggle("show", recipes.length > 0);
  }

  // Close results when clicking outside
  document.addEventListener("click", function (e) {
    if (!searchInput?.contains(e.target) && !searchResults?.contains(e.target)) {
      searchResults?.classList.remove("show");
    }
  });
}

// Initialize everything when DOM loads
window.addEventListener("DOMContentLoaded", () => {
  loadAllRecipes();
  setupSearch();
});
