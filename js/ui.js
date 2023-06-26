function gradioApp() {
    const elems = document.getElementsByTagName('gadio-app')
    const elem = elems.length == 0 ? document : elems[0]

    if (elem !== document) elem.getElementById = function(id) { return document.getElementById(id) }
    return elem.shadowRoot ? elem.shadowRoot : elem
}

function get_uiCurrentTab() {
    return gradioApp().querySelector('#tabs button:not(.border-transparent)')
}

function get_uiCurrentTabContent() {
    return gradioApp().querySelector('')
}

/**
 * check that a UI element is not in another hidden element or tab content
 * @param el
 */
function uiElementIsVisible(el){
    let isVisible = !el.closest('.\\!hidden');
    if (! isVisible) {
        return false;
    }

    while( isVisible = el.closest('.tabitem')?.style.display !== 'none') {
        if ( !isVisible) {
            return false;
        }
        else if (el.parentElement){
            el = el.parentElement
        }
        else {
            break;
        }
    }
    return isVisible;
}

function updateInput(target){
	let e = new Event("input", { bubbles: true })
	Object.defineProperty(e, "target", {value: target})
	target.dispatchEvent(e);
}

function del_sensitive_word(button, word){
    textarea = gradioApp().querySelector('#extension_to_install textarea')
    textarea.value = word
    updateInput(textarea)
    gradioApp().querySelector("#del_sensitive_word_btn").click()
}