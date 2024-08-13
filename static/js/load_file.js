    const fileInput = document.getElementById('file');
    const formContainer = document.getElementById('form-container');
    const previewContainer = document.getElementById('preview');
    const previewImage = document.getElementById('preview-image');
    const modal = document.getElementById('modal');
    const modalImage = document.getElementById('modal-image');
    const closeModal = document.getElementById('close-modal');

    // Inicializace zobrazení formuláře
    function updateFormPosition() {
        if (fileInput.files.length > 0) {
            formContainer.classList.add('form-moved');
        } else {
            formContainer.classList.remove('form-moved');
        }
    }

    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
                updateFormPosition();
            }
            reader.readAsDataURL(file);
        } else {
            previewContainer.style.display = 'none';
            updateFormPosition();
        }
    });

    previewImage.addEventListener('click', function() {
        modalImage.src = this.src;
        modal.style.display = 'flex';
    });

    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });