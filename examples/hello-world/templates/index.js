$(() => {
  const appendToLog = (data) => $('#log').append(`${typeof data === 'object' ? JSON.stringify(data) : data}<br />`);
  const handleAjaxError = (error) => appendToLog(error.responseText);
  const runAjax = (url) => $.get(url).done(appendToLog).fail(handleAjaxError);
  const runLogAjax = () => runAjax('/code/log').fail(() => setTimeout(runLogAjax, 500)).done(runResAjax);
  const runResAjax = () => runAjax('/code/res');
  marked.setOptions({renderer: new marked.Renderer(),highlight: (code) => hljs.highlightAuto(code).value,langPrefix: 'hljs language-'});
  $('#content').html(marked.parse(`{{ markdown | safe | replace('`','\`') }}`));
  $('#form').submit((e) => {
    e.preventDefault();
    $('#log').empty();
    const result = $('#form').serializeArray().reduce((acc, { name, value }) => ({ ...acc, [name]: acc[name] ? `${acc[name]},${value}` : value }), {});
    $.post('/code/run', result).done((data) => {appendToLog(data);runLogAjax()}).fail(handleAjaxError);
  });
});
