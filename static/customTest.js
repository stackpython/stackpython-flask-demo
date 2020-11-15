 // /static/custom.js


  // Initialize Pusher
  const pusher = new Pusher('91d5569d42fc4b9024ab', {
    cluster: 'ap1',
    encrypted: true
});

// Subscribe to movie_bot channel
const channel = pusher.subscribe('movie_bot');

  // bind new_message event to movie_bot channel
  channel.bind('new_message', function(data) {

   // Append human message
    $('.chat-container').append(`
        <div class="chat-message col-md-5 humans-message">
            ${data.human_message}
        </div>
    `)

    // Append bot message
    $('.chat-container').append(`
        <div class="chat-message col-md-5 offset-md-7 bots-message">
            ${data.bot_message}
        </div>
    `)
});



 function submit_message(message) {
    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {
      // append the bot repsonse to the div
      $('.chat-container').append(`
            <div class="chat-message col-md-5 offset-md-7 bots-message">
                ${data.message}
            </div>
      `)
      // remove the loading indicator
      $( "#loading" ).remove();
    }
}

$.post( "/send_message", {
    message: messages2, 
    socketId: pusher.connection.socket_id
}, handle_response);

$('#target').on('submit', function(e){
    e.preventDefault();
    const input_message = $('#input_message').val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $('.chat-container').append(`
        <div class="chat-message col-md-5 humans-message">
            ${input_message}
        </div>
    `)

    // loading 
    $('.chat-container').append(`
        <div class="chat-message text-center col-md-2 offset-md-10 bots-message" id="loading">
            <b>...</b>
        </div>
    `)

    // clear the text input 
    $('#input_message').val('')

    // send the message
    submit_message(input_message)
});