const initChangeLanguageHandler = () => {
    const lang_form = document.getElementById("lang-change");
    const lang_select = lang_form.querySelector(".form-select");
    lang_select.addEventListener("change", (event) => lang_form.submit());
}

document.addEventListener('DOMContentLoaded', initChangeLanguageHandler);
