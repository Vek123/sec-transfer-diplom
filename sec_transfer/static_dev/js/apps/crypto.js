const encryptFile = async (fileData) => {
    const aesKey = await crypto.subtle.generateKey(
        {
            name: 'AES-GCM',
            length: 256,
        },
        true,
        ['encrypt', 'decrypt'],
    );
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const cipherData = await crypto.subtle.encrypt(
        { name: 'AES-GCM', iv: iv, tagLength: 128 },
        aesKey,
        fileData,
    )
    const tagPosition = cipherData.byteLength - 16;
    const encryptedData = cipherData.slice(0, tagPosition);
    const tag = cipherData.slice(tagPosition);

    return [ encryptedData, aesKey, iv, tag ]
}

const encryptFormFile = async (fileInput, ivInput, gcmTagInput, encryptedKeyInput) => {
    const reader = new FileReader();
    const file = fileInput.files[0];
    reader.onload = async e => {
        const [ data, aesKey, iv, tag ] = await encryptFile(e.target.result);
        fileInput.files = arrayBufferToDataTransfer(data, file.name, file.type).files;
        ivInput.value = bufferToBase64(iv);
        gcmTagInput.value = bufferToBase64(tag);
        const encrypted_aes_key = await encryptAESKey(aesKey)
        encryptedKeyInput.value = bufferToBase64(encrypted_aes_key);
    }
    reader.readAsArrayBuffer(file);
}

const decryptFile = async (fileData, aesKey, gcmTag, iv) => {
    const encryptedData = concatenate(new Uint8Array(fileData), new Uint8Array(gcmTag))
    
    const decryptedData = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv: iv, tagLength: 128 },
        aesKey,
        encryptedData.buffer,
    )
    return decryptedData;
}

const encryptAESKey = async (aesKey, publicKey=null) => {
    if (!publicKey) {
        publicKey = await getEncryptPublicKey();
    }
    return await crypto.subtle.encrypt(
        { name: 'RSA-OAEP' },
        publicKey,
        await crypto.subtle.exportKey('raw', aesKey),
    )
}

const verifyWithPublicKey = async (signature, signedData, publicKey=null) => {
    if (!publicKey) {
        publicKey = await getVerifyPublicKey();
    }
    return await crypto.subtle.verify(
        { name: 'RSA-PSS', saltLength: 222 },
        publicKey,
        signature,
        signedData,
    )
}

const getPublicKeyStr = () => {
    const re = new RegExp(`${getRSAPublicKeyCookieName()}=([^;]+)`);
    const match = document.cookie.match(re);
    
    if (!match || !match[1]) {
        const errorMsg = 'RSA public key not found in cookie';
        addMessageError(errorMsg);
        throw new Error(errorMsg);
    }
    
    return Uint8Array.from(atob(match[1].replace(/^b?'|'$/g, '')), c => c.charCodeAt(0));
}

const getEncryptPublicKey = async () => {
    const key_str = getPublicKeyStr()
    const key = await crypto.subtle.importKey(
        'spki',
        key_str,
        { name: 'RSA-OAEP', hash: 'SHA-256' },
        true,
        ['encrypt'],
    );
    return key;
}

const getVerifyPublicKey = async () => {
    const key_str = getPublicKeyStr()
    const key = await crypto.subtle.importKey(
        'spki',
        key_str,
        { name: 'RSA-PSS', hash: 'SHA-256' },
        true,
        ['verify'],
    );
    return key;
}

const importAESKey = async (aesKey, keyUsages) => {
    return await crypto.subtle.importKey(
        'raw',
        aesKey,
        { name: 'AES-GCM' },
        true,
        keyUsages,
    )
}

const bufferToBase64 = (buf) => {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(buf)));
}

const base64ToBuffer = (data) => {
    return Uint8Array.from(atob(data), c => c.charCodeAt(0))
}
