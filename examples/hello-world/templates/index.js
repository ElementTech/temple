$(() => {
  marked.setOptions({
    renderer: new marked.Renderer(),
    highlight: (code, lang) => hljs.highlightAuto(code).value,
    langPrefix: 'hljs language-',
  });

  var objectConstructor = ({}).constructor;

  function stringifyIfNeeded(value) {
    if (value.constructor === objectConstructor) {
      return JSON.stringify(value);
    } else {
      return value
    }
  }

  $('#content').html(marked.parse(`{{ markdown | safe | replace('`','\`') }}`));


  const res = () => $.get('/code/res').done(data => $('#log').append("<br />" + stringifyIfNeeded(data))).fail(error => $('#log').append("<br />" + error.responseText));

  const log = () => $.get('/code/log').done(data => ($('#log').append("<br />" + stringifyIfNeeded(data)), res())).fail(error => ($('#log').append("<br />" + error.responseText), setTimeout(log, 500)));

  $('#form').submit(e => {
    e.preventDefault();
    $('#log').empty();
    const result = $('#form').serializeArray().reduce((acc, { name, value }) => ((acc[name] = acc[name] ? `${acc[name]},${value}` : value), acc), {});
    $.post('/code/run', result).done(data => ($('#log').append(stringifyIfNeeded(data)), log())).fail(error => ($('#log').append(error.responseText), null));
  });
});