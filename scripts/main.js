document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

    window.compileCode = function() {
        var code = document.getElementById('code').value;
        document.getElementById('output').innerText = ''; // Очистити попередній вивід
        socket.emit('compile_code', { code: code });
    };

    window.stopExecution = function() {
        socket.emit('stop_execution');
    };

    socket.on('compilation_result', function(data) {
        var outputElement = document.getElementById('output');
        outputElement.innerText += data.output + '\n';
    });
});
