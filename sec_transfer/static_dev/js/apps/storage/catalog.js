const downloadFile = async (event) => {
    const publicKey = await getVerifyPublicKey();
    const tableRow = event.target.closest('.file');
    const fileId = tableRow.dataset.fileId;
    const fileUrl = tableRow.dataset.fileUrl;
    const downloadCryptoDataUrl = format(getFileCryptoDataUrl(), fileId);
    let { encrypted_key, aes_key_sign, gcm_tag, iv } = await (await fetch(downloadCryptoDataUrl)).json();
    const file = await (await fetch(fileUrl)).blob();
    const arrayBufferEncoder = new TextEncoder();
    const aesKey = Uint8Array.from(atob(encrypted_key), c => c.charCodeAt(0));
    const gcmTag = arrayBufferEncoder.encode(atob(gcm_tag));
    const aesKeySign = Uint8Array.from(atob(aes_key_sign), c => c.charCodeAt(0));
    
    iv = Uint8Array.from(atob(iv), c => c.charCodeAt(0));
    console.log(await crypto.subtle.verify({ name: 'RSA-PSS', saltLength: 222 }, publicKey, aesKeySign, aesKey));
}

document.querySelectorAll('.file__download').forEach((val) => {
    val.onclick = downloadFile;
});
