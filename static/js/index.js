document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.emit('join');

        document.querySelector('#message').addEventListener('keydown', event => {
            if (event.key == 'Enter') {
                document.getElementById("send-button").click();
            }
        });

        document.querySelector('#send').onclick = () => {
            let timestamp = new Date();
            timestamp = timestamp.toLocaleString('en-US');

            let msg = document.getElementById('message').value;

            socket.emit('send message', msg, timestamp);

            document.getElementById('message').value = '';
        };
    });

    socket.on('announce message', data => {
        let message = '[ ' + `${data.user}` + ']:  ' + `${data.timestamp}` + '\n' + `${data.msg}`
        
        document.querySelector('#msg').value += message + '\n'
    })
});
