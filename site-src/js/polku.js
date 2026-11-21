/*
 * Itseopiskelupolun edistyminen ja muistiinpanot.
 * Tiedot tallentuvat vain tämän selaimen localStorageen avaimella 'loo:v1', ja vain silloin,
 * kun käyttäjä painaa painiketta. Sivun avaaminen vain lukee tiedot. Mitään ei lähetetä.
 */
(function () {
  'use strict';

  var KEY = 'loo:v1';
  var root = document.documentElement;
  root.classList.add('js');

  function emptyState() {
    return { v: 1, done: {}, notes: {} };
  }

  function readState() {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) { return emptyState(); }
      var parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== 'object') { return emptyState(); }
      parsed.done = parsed.done && typeof parsed.done === 'object' ? parsed.done : {};
      parsed.notes = parsed.notes && typeof parsed.notes === 'object' ? parsed.notes : {};
      parsed.v = 1;
      return parsed;
    } catch (error) {
      return emptyState();
    }
  }

  function writeState(state) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(state));
      return true;
    } catch (error) {
      return false;
    }
  }

  function each(selector, callback) {
    Array.prototype.forEach.call(document.querySelectorAll(selector), callback);
  }

  function say(message) {
    each('[data-storage-status]', function (element) { element.textContent = message; });
  }

  function showControls() {
    each('[data-js-only]', function (element) { element.removeAttribute('hidden'); });
  }

  function render(state) {
    var total = 0;
    var done = 0;
    each('[data-step-toggle]', function (button) {
      var id = button.getAttribute('data-step-toggle');
      var isDone = state.done[id] === true;
      button.setAttribute('aria-pressed', isDone ? 'true' : 'false');
      button.textContent = isDone ? 'Tehty. Poista merkintä' : 'Merkitse tehdyksi';
    });
    each('[data-step]', function (step) {
      total += 1;
      if (state.done[step.getAttribute('data-step')] === true) { done += 1; }
    });
    each('[data-progress]', function (element) {
      var count = parseInt(element.getAttribute('data-total'), 10) || total;
      element.textContent = 'Tehty ' + done + ' / ' + count;
    });
    each('textarea[data-note-for]', function (area) {
      var id = area.getAttribute('data-note-for');
      if (document.activeElement !== area) { area.value = state.notes[id] || ''; }
    });
  }

  function toggleStep(id) {
    var state = readState();
    if (state.done[id] === true) { delete state.done[id]; } else { state.done[id] = true; }
    say(writeState(state) ? '' : 'Selain ei sallinut tallennusta. Merkintä näkyy vain tällä sivulla.');
    render(state);
  }

  function saveNote(id) {
    var area = document.querySelector('textarea[data-note-for="' + id + '"]');
    if (!area) { return; }
    var state = readState();
    if (area.value.trim() === '') { delete state.notes[id]; } else { state.notes[id] = area.value; }
    say(writeState(state) ? 'Muistiinpano tallennettu tähän selaimeen.' : 'Selain ei sallinut tallennusta.');
  }

  function clearAll() {
    if (!window.confirm('Poistetaanko kaikki tämän selaimen merkinnät ja muistiinpanot?')) { return; }
    try { window.localStorage.removeItem(KEY); } catch (error) { /* nothing to remove */ }
    each('textarea[data-note-for]', function (area) { area.value = ''; });
    render(emptyState());
    say('Tiedot on poistettu.');
  }

  function printNotes() {
    var state = readState();
    var wrapper = document.createElement('div');
    wrapper.className = 'notes-print';
    var heading = document.createElement('h2');
    heading.textContent = 'Omat muistiinpanot';
    wrapper.appendChild(heading);
    var count = 0;
    each('[data-step]', function (step) {
      var id = step.getAttribute('data-step');
      if (!state.notes[id]) { return; }
      count += 1;
      var title = step.querySelector('h3');
      var sub = document.createElement('h3');
      sub.textContent = title ? title.textContent : id;
      var text = document.createElement('p');
      text.style.whiteSpace = 'pre-wrap';
      text.textContent = state.notes[id];
      wrapper.appendChild(sub);
      wrapper.appendChild(text);
    });
    if (count === 0) {
      var none = document.createElement('p');
      none.textContent = 'Ei tallennettuja muistiinpanoja.';
      wrapper.appendChild(none);
    }
    var main = document.querySelector('main') || document.body;
    main.appendChild(wrapper);
    document.body.classList.add('printing-notes');
    window.print();
    document.body.classList.remove('printing-notes');
    main.removeChild(wrapper);
  }

  document.addEventListener('click', function (event) {
    var target = event.target.closest ? event.target.closest('button') : null;
    if (!target) { return; }
    if (target.hasAttribute('data-step-toggle')) { toggleStep(target.getAttribute('data-step-toggle')); }
    else if (target.hasAttribute('data-note-save')) { saveNote(target.getAttribute('data-note-save')); }
    else if (target.hasAttribute('data-clear-data')) { clearAll(); }
    else if (target.hasAttribute('data-print-notes')) { printNotes(); }
  });

  showControls();
  render(readState());
})();
