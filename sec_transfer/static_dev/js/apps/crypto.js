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

const getPublicKeyStr = () => {
    const re = new RegExp(`${getRSAPublicKeyCookieName()}=([^;]+)`);
    const match = document.cookie.match(re);
    
    if (!match || !match[1]) {
        throw new Error('RSA public key not found in cookie');
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

const bufferToBase64 = (buf) => {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(buf)));
}
