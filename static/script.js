document.addEventListener("DOMContentLoaded", function () {
  const label = document.querySelector(".file-label");
  label.addEventListener("mouseover", () => {
      label.style.backgroundColor = "#fb8c00";
  });
  label.addEventListener("mouseout", () => {
      label.style.backgroundColor = "#ff9800";
  });
});
