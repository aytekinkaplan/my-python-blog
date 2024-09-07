document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript yüklendi!");

  const header = document.querySelector("header h1");
  if (header) {
    header.style.cursor = "pointer";
    header.addEventListener("click", function () {
      alert("Python Blog'a Hoş Geldiniz!");
    });
  }

  const postTitles = document.querySelectorAll(".post h2 a");
  postTitles.forEach((title) => {
    title.addEventListener("mouseover", function () {
      this.style.color = "#ffd43b";
    });
    title.addEventListener("mouseout", function () {
      this.style.color = "#3776ab";
    });
  });
});
