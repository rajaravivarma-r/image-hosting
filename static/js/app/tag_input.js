document.addEventListener('DOMContentLoaded', function () {
  const tagsInput = document.getElementById('tagsInput');
  const addTagButton = document.getElementById('addTagButton');
  const tagsContainer = document.getElementById('tagsContainer');
  const hiddenTagsInput = document.getElementById('hiddenTagsInput');
  let imageTags = [];

  addTagButton.addEventListener('click', function () {
    const tagValue = tagsInput.value.trim();
    if (tagValue !== "") {
      const tagElement = document.createElement('span');
      tagElement.className = 'badge align-middle badge-primary tag-text mr-2';
      tagElement.textContent = tagValue;

      const removeButton = document.createElement('button');
      removeButton.className = 'btn btn-close btn-sm ml-1';
      removeButton.innerHTML = "&times;"; // Using innerHTML to properly escape the "&times;"
      removeButton.addEventListener('click', function () {
        tagsContainer.removeChild(tagElement);
        imageTags = imageTags.filter((tag) => tag !== tagValue);
        updateHiddenTagsInput();
      });

      if (!imageTags.includes(tagValue)) {
        imageTags.push(tagValue);
        tagElement.appendChild(removeButton);
        tagsContainer.appendChild(tagElement);

        // Clear the input field
        tagsInput.value = "";

        // Update hidden input field
        updateHiddenTagsInput();
      }
    }
  });

  function updateHiddenTagsInput() {
    hiddenTagsInput.value = imageTags.join(',');
  }
});
