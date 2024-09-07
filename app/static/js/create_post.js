document.addEventListener("DOMContentLoaded", function () {
  const sectionsContainer = document.getElementById("sections-container");
  const addSectionButton = document.getElementById("add-section");
  const form = document.getElementById("blog-post-form");

  function createSection() {
    const section = document.createElement("div");
    section.className = "section";
    section.innerHTML = `
          <input type="text" placeholder="Section Title" class="section-title">
          <textarea placeholder="Content" class="section-content"></textarea>
          <textarea placeholder="Python Code" class="section-code"></textarea>
          <textarea placeholder="Output" class="section-output"></textarea>
      `;
    sectionsContainer.appendChild(section);
  }

  addSectionButton.addEventListener("click", createSection);

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const sections = document.querySelectorAll(".section");
    const data = {
      title: document.querySelector('input[name="title"]').value,
      content: document.querySelector('textarea[name="content"]').value,
      sections: Array.from(sections).map((section) => ({
        title: section.querySelector(".section-title").value,
        content: section.querySelector(".section-content").value,
        code: section.querySelector(".section-code").value,
        output: section.querySelector(".section-output").value,
      })),
    };

    fetch("/create_post", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Post created successfully!");
        window.location.href = "/";
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while creating the post.");
      });
  });

  // Initial section
  createSection();
});
