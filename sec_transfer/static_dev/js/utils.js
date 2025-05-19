const format = (str, ...values) => {
    return str.replace(/{(\d+)}/g, function(match, index) {
        return typeof values[index] !== 'undefined' ? values[index] : match;
    });
}
