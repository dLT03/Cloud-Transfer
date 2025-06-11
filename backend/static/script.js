const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const folderInput = document.getElementById('folderInput');
const fileSummary = document.getElementById('fileSummary');
const formView = document.getElementById('formView');
const linkView = document.getElementById('linkView');

let uploadMode = "file"; // Default upload mode

// Display selected files with name, extension, and size
function showFiles(input) {
  if (input.files.length > 0) {
    const files = Array.from(input.files);
    const summary = files.map(file => {
      const ext = file.name.split('.').pop();
      const size = (file.size / 1024).toFixed(2);
      return `<div><strong>${file.name}</strong> (${ext}, ${size} KB)</div>`;
    }).join('');

    fileSummary.innerHTML = `<strong>Files selected:</strong><br>${summary}`;
    fileSummary.style.display = 'block';
  }
}

// Set mode to single file and display selected file
fileInput.addEventListener('change', () => {
  uploadMode = "file";
  showFiles(fileInput);
});

// Set mode to folder and display selected files
folderInput.addEventListener('change', () => {
  uploadMode = "folder";
  showFiles(folderInput);
});

// Form submission
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const files = uploadMode === "file" ? fileInput.files : folderInput.files;
  if (!files || files.length === 0) {
    alert("No file selected.");
    return;
  }

  const formData = new FormData();
  const customTitle = document.getElementById("title").value.trim();

  if (uploadMode === "file") {
    formData.append("file", files[0]);
    if (customTitle) {
      formData.append("customName", customTitle);
    }
  } else {
    for (let file of files) {
      formData.append("files", file, file.webkitRelativePath);
    }

    // Extract and send folder name
    const folderName = files[0].webkitRelativePath?.split("/")[0];
    formData.append("folderName", folderName);
    if (customTitle) {
      formData.append("customName", customTitle);
    }
  }

  try {
    // Send files to backend
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("Upload failed");

    const data = await response.json();

    formView.style.display = "none";
    linkView.innerHTML = `
      <div class="link-line">
        <span class="link-text">${data.download_link}</span>
      </div>
      <button class="generate" onclick="navigator.clipboard.writeText('${data.download_link}')">copy</button>
      <p class="text2">link is generated, enjoy :]</p>
    `;
    linkView.style.display = "block";

  } catch (err) {
    alert("Upload failed: " + err.message);
  }
});
