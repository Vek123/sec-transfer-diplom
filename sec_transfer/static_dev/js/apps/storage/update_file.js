const createFileForm = document.getElementById('update-file-form');

const fileInput = createFileForm.querySelector('input[name="file"]');
const ivInput = createFileForm.querySelector('input[name="iv"]');
const gcmTagInput = createFileForm.querySelector('input[name="gcm_tag"]');
const encryptedKeyInput = createFileForm.querySelector('input[name="encrypted_key"]');

fileInput.onchange = async event => {
    encryptFormFile(fileInput, ivInput, gcmTagInput, encryptedKeyInput);
}
