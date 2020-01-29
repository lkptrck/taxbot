var loadingMsgIndex,
    botui = new BotUI('tax-bot');

function sendXHR(question, printer) {
  var xhr = new XMLHttpRequest();
  var self = this;
  xhr.open('POST', 'http://localhost:8000');
  xhr.send(question);
  xhr.onload = function () {
    printer(xhr.responseText);
  }
  xhr.send();
}

function init() {
  botui.message
  .bot({
    delay: 1000,
    content: 'Want to know more about tax? Please enter your question below:'
  })
  .then(function () {
    return botui.action.text({
      delay: 1000,
      action: {
        value: '',
        placeholder: ''
      }
    })
  }).then(function (res) {
    loadingMsgIndex = botui.message.bot({
      delay: 200,
      loading: true
    }).then(function (index) {
      loadingMsgIndex = index;
      sendXHR(res.value, printAnswer)
    });
  });
}

function printAnswer(answer) {
  botui.message
  .update(loadingMsgIndex, {
    content: answer
  })
  .then(init);
}

init();