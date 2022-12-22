from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
app = FastAPI()

html = """
<!DOCTYPE html>

    <html>
    <head>
        <title>Message list</title>
        <script src="https://code.jquery.com/jquery-3.1.1.min.js" integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=" crossorigin="anonymous"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
        <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container">
            <h2>Сервис вывод списка сообщений на страницу без перезагрузки</h2>
            <form action="" onsubmit="sendMessage(event)" class="ui form">
                <div class="field">
                    <h4>Введите сообщение:</h4>
                    <input type="text" id="messageText" autocomplete="off">
                </div>
                <button>Отправить</button>
                </form>
                <div class="ui divider"></div>
                <div id="messages"></div>
                <script>
                    var ws = new WebSocket("ws://localhost:8000/ws");
                    ws.onmessage = function(event) {
                        var messages = document.getElementById("messages")
                        var message = document.createElement('label')
                        var br = document.createElement('br')
                        var msg_obj = JSON.parse(event.data)
                        var keys = Object.values(msg_obj)
                        result = keys[0]+ ". " + keys[1]
                        var content = document.createTextNode(result)
                        message.appendChild(content)
                        messages.appendChild(message)
                        messages.appendChild(br)
                    };
                    function sendMessage(event) {
                        var input = document.getElementById("messageText")
                        if (input.value.length == 0) {
                            alert("Введено пустое сообщение страница будет перезагружена")
                            location.reload()
                        } else {
                            var json = JSON.stringify(input.value)
                            ws.send(json)
                            input.value = ''
                            event.preventDefault()
                        }
                    }
                </script>
        </div>
    </body>

</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        response_data = {
            'number': 0,
            'message': ''}
        count = 1
        while True:
            data = await websocket.receive_json()
            response_data['number'] = count
            response_data['message'] = data
            await websocket.send_json(response_data)
            count += 1
    except WebSocketDisconnect:
        print("close the page")