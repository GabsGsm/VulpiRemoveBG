function uploadImage() {
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');

    if (fileInput.files.length > 0) {
        if (fileInput.files.length > 0) {
            const allowedExtensions = [".jpg", ".jpeg", ".png"];
            const fileName = fileInput.files[0].name;
            const fileExtension = fileName.slice(((fileName.lastIndexOf(".") - 1) >>> 0) + 2);
    
            if (allowedExtensions.includes("." + fileExtension.toLowerCase())) {
                document.getElementById('overlay').classList.remove('hidden');
                uploadForm.submit();
            } else {
                alert("Somente arquivos .jpg, .jpeg e .png são permitidos.");
                fileInput.value = ''; 
            }
        }
    }
}