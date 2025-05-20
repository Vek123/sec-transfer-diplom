const downloadFile = async (event) => {
    const publicKey = await getVerifyPublicKey();
    const tableRow = event.target.closest('.file');
    const fileId = tableRow.dataset.fileId;
    const fileUrl = tableRow.dataset.fileUrl;
    const filename = fileUrl.split('/').reverse()[0];
    const downloadCryptoDataUrl = format(getFileCryptoDataUrl(), fileId);

    let { encrypted_key, aes_key_sign, gcm_tag, iv } = await (await fetch(downloadCryptoDataUrl)).json();

    const aesKey = base64ToBuffer(encrypted_key);
    const gcmTag = base64ToBuffer(gcm_tag);
    const aesKeySign = base64ToBuffer(aes_key_sign);
    iv = base64ToBuffer(iv);

    if (!await verifyWithPublicKey(aesKeySign, aesKey, publicKey)) {
        addMessageError('AES key was compromitised while delivering from the server. File was not downloaded. Try again later...');
        return;
    }

    const aesCryptoKey = await importAESKey(aesKey, ['decrypt'])

    const fileBlob = await (await fetch(fileUrl)).blob();
    const fileBuffer = await fileBlob.arrayBuffer();
    let data = null;
    try {
        data = await decryptFile(fileBuffer, aesCryptoKey, gcmTag, iv);
    } catch (error) {
        addMessageError('GMC tag found that file was compromitised while delivering from the server. File was not downloaded. Try again later...');
        return;
    }
    const decryptedFile = new Blob([data], {type: fileBlob.type});

    downloadBlob(decryptedFile, filename);
}

document.querySelectorAll('.file__download').forEach((val) => {
    val.onclick = downloadFile;
});
