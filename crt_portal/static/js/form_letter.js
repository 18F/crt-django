(function(root) {
  var modal = document.getElementById('intake_template');

  var contact = document.getElementById('contact_complainant');
  var showModal = function(event) {
    event.preventDefault();
    if (modal.getAttribute('hidden') !== null) {
      root.CRT.openModal(modal);
    } else {
      root.CRT.closeModal(modal);
    }
  };
  contact.addEventListener('click', showModal);

  var cancel_modal = document.getElementById('intake_template_cancel');
  root.CRT.cancelModal(modal, cancel_modal);

  var copy = document.getElementById('intake_copy');
  var print = document.getElementById('intake_print');
  var letter = document.getElementById('intake_letter');
  var send_email = document.getElementById('intake_send');

  var email_enabled = document.getElementById('intake_send').dataset.emailEnabled === 'True';
  var has_contact_email = Boolean(document.getElementById('contact_email').dataset.email);

  var reset = function() {
    description.innerHTML = '(select a response template)';
    letter.innerHTML = '';
    copy.setAttribute('disabled', 'disabled');
    print.setAttribute('disabled', 'disabled');
    send_email.setAttribute('disabled', 'disabled');
  };

  var description = document.getElementById('intake_description');
  var options = document.getElementById('intake_select');
  options.onchange = function(event) {
    event.preventDefault();
    var index = event.target.selectedIndex;
    var option = event.target.options[index];
    description.innerHTML = option.dataset['description'] || '(select a response template)';
    letter.innerHTML = option.dataset['content'] || '';
    if (index >= 1) {
      copy.removeAttribute('disabled');
      print.removeAttribute('disabled');
      if (email_enabled && has_contact_email) {
        send_email.removeAttribute('disabled');
      }
    } else {
      reset();
    }
  };

  var setLanguageCookie = function(lang) {
    document.cookie = 'form-letter-language' + '=' + lang;
  };

  var getLanguageCookie = function() {
    var nameEQ = 'form-letter-language=';
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  };

  var applyTemplateLanguageFilter = function() {
    var language_select = document.getElementById('template-language-select');
    var selected_language = language_select.value;

    // form letters for languages other than the one selected
    var toHide = document.querySelectorAll(
      `#intake_select > option.usa-select:not([data-language=${selected_language}])`
    );
    // form letters for the language that is selected
    var toShow = document.querySelectorAll(
      `#intake_select > option.usa-select[data-language=${selected_language}]`
    );

    for (var el of toHide) {
      el.setAttribute('hidden', 'true');
    }

    for (var el of toShow) {
      el.removeAttribute('hidden');
    }

    // the selected language changed, clear the currently selected form letter
    var intake_select = document.getElementById('intake_select');
    intake_select.selectedIndex = 0;
    reset();
  };

  var language_select = document.getElementById('template-language-select');
  language_select.onchange = function(event) {
    event.preventDefault();
    applyTemplateLanguageFilter();
    setLanguageCookie(language_select.value);
  };

  // try to grab the most recently used language setting
  if (getLanguageCookie()) {
    // if there is one, set the dropdown back to that value
    language_select.value = getLanguageCookie();
  }
  // refresh the template dropdown to reflect the current language selection
  applyTemplateLanguageFilter();

  var copyContents = function(event) {
    const el = document.createElement('textarea');
    el.value = description.innerText + '\n\n' + letter.value;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    el.setSelectionRange(0, 99999); // mobile
    document.execCommand('copy');
    document.body.removeChild(el);
  };
  copy.addEventListener('click', copyContents);

  var printContents = function(event) {
    const letterhead = document.getElementById('form-letterhead');
    const letter_placeholder = document.getElementById('form-letter--placeholder');
    const el = document.createElement('p');
    el.append(letter.value);
    letter_placeholder.appendChild(el);
    letterhead.removeAttribute('hidden');
    document.body.appendChild(letterhead);
    window.print();
    letterhead.removeChild(el);
    document.body.removeChild(letterhead);
    root.CRT.closeModal(modal);
  };
  print.addEventListener('click', printContents);
})(window);
