import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.responses import HTMLResponse

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


executor = ThreadPoolExecutor(max_workers=10)


def run_playbook():
    process = subprocess.Popen(['ansible-playbook', '/opt/project/autox/ansible/site.yml'], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    output = []
    for line in iter(process.stdout.readline, ''):
        output.append(line)
    process.stdout.close()
    process.wait()
    return output


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "run_playbook":
                loop = asyncio.get_event_loop()
                output = await loop.run_in_executor(executor, run_playbook)
                for line in output:
                    await websocket.send_text(line)
                await websocket.send_text("Playbook execution finished.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()


if __name__ == '__main__':
    uvicorn.run(app, port=9999, host='0.0.0.0')
