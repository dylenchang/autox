import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI WebSocket</title>
</head>
<body>
    <h1>Ansible Playbook Logs</h1>
    <button onclick="runPlaybook()">Run Playbook</button>
    <pre id="logs"></pre>
    <script>
        var ws = new WebSocket("ws://" + location.host + "/ws");
        ws.onmessage = function(event) {
            var logs = document.getElementById('logs');
            logs.innerHTML += event.data + '\\n';
            logs.scrollTop = logs.scrollHeight;
        };

        function runPlaybook() {
            ws.send('run_playbook');
        }
    </script>
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
        while True:
            data = await websocket.receive_text()
            if data == "run_playbook":
                process = subprocess.Popen(['ansible-playbook', '/opt/project/autox/ansible/site.yml'], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, text=True)
                for line in iter(process.stdout.readline, ''):
                    await websocket.send_text(line)
                process.stdout.close()
                process.wait()
                await websocket.send_text("Playbook execution finished.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, port=9999, host='0.0.0.0')