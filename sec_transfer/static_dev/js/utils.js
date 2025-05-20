const format = (str, ...values) => {
    return str.replace(/{(\d+)}/g, function(match, index) {
        return typeof values[index] !== 'undefined' ? values[index] : match;
    });
}

const _createMessage = (messageText) => {
    const message = document.createElement('p');
    message.classList.add('alert');
    message.textContent = messageText;
    return message;
}

const _showMessage = (message) => {
    const container = document.querySelector('.messages');
    container.appendChild(message);
}

const addMessageSuccess = (messageText) => {
    const message = _createMessage(messageText);
    message.classList.add('alert-success');
    _showMessage(message);
}

const addMessageError = (messageText) => {
    const message = _createMessage(messageText);
    message.classList.add('alert-danger');
    _showMessage(message);
}

const downloadBlob = (blob, filename) => {
    let tUrl = URL.createObjectURL(blob);
    const tmp1 = document.createElement('a');
    tmp1.style.visibility = 'hidden';
    tmp1.href = tUrl;
    tmp1.download = filename;
    document.body.appendChild(tmp1);
    tmp1.click();
    URL.revokeObjectURL(tUrl);
    tmp1.remove();
}

const concatenate = (...arrays) => {
  let size = arrays.reduce((a,b) => a + b.byteLength, 0)
  let result = new Uint8Array(size)
  let offset = 0
  for (let arr of arrays) {
    result.set(arr, offset)
    offset += arr.byteLength
  }
  return result
}

const arrayBufferToDataTransfer = (data, filename, filetype) => {
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(new File([new Blob([data])], filename, { type: filetype }));
    return dataTransfer;
}
