const createFileForm = document.getElementById('create-file-form');

const fileInput = createFileForm.querySelector('input[name="file"]');
const ivInput = createFileForm.querySelector('input[name="iv"]');
const gcmTagInput = createFileForm.querySelector('input[name="gcm_tag"]');
const encryptedKeyInput = createFileForm.querySelector('input[name="encrypted_key"]');

fileInput.onchange = async event => {
    const reader = new FileReader();
    const file = fileInput.files[0];
    reader.onload = async e => {
        const [ data, aesKey, iv, tag ] = await encryptFile(e.target.result);
        const dataTransfer = new DataTransfer()
        dataTransfer.items.add(new File([new Blob([data])], file.name, { type: file.type }));
        fileInput.files = dataTransfer.files;
        ivInput.value = bufferToBase64(iv);
        gcmTagInput.value = bufferToBase64(tag);
        const public_key = await getEncryptPublicKey();
        
        const encrypted_aes_key = await crypto.subtle.encrypt(
            { name: 'RSA-OAEP' },
            public_key,
            await crypto.subtle.exportKey('raw', aesKey),
        )
        console.log(encrypted_aes_key);

        encryptedKeyInput.value = bufferToBase64(encrypted_aes_key);
    }
    reader.readAsArrayBuffer(file);
}
