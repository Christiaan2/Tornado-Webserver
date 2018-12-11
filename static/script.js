var ws = null;

function StartWebsocket() {
	if ("WebSocket" in window) {
		if (ws === null) {
			ConnectWebsocket();
		} else {
			if (ws.readyState == 3) {
				ConnectWebsocket();
			} else {
				ws.close();
			}
		}
	} else {
		document.getElementById("WebsocketStatus").innerHTML = "WebSocket NOT supported by your Browser";
		document.getElementById("WebsocketStatus").style.color = "rgb(200, 0, 0)";
	}
}

function ConnectWebsocket() {
	if (window.location.protocol === "http:") {
		ws = new WebSocket("ws://" + window.location.host + "/ws");
	} else {
		ws = new WebSocket("wss://" + window.location.host + "/ws");
	}

	ws.onopen = function(evt) {
		document.getElementById("WebsocketStatus").innerHTML = "Connected";
		document.getElementById("WebsocketStatus").style.color = "rgb(0, 200, 0)";
		document.getElementById("startWebsocket").textContent = "Disconnect websocket";
	}

	ws.onmessage = function(evt) {
		if (typeof evt.data === 'string') {
			var m_json = JSON.parse(evt.data);
			if (m_json != null) {
				var json_AIn = m_json.AIn;
				for (var i = 0; i < json_AIn.length; i++) {
					document.getElementsByClassName("analogIn")[i].innerHTML = json_AIn[i];
				}
				var json_DIn = m_json.DIn;
				for (var i = 0; i < json_DIn.length; i++) {
					if (json_DIn[i]) {
						document.getElementsByClassName("digitalIn")[i].innerHTML = "High";
					} else {
						document.getElementsByClassName("digitalIn")[i].innerHTML = "Low";
					}
				}
				var json_DOut = m_json.DOut;
				for (var i = 0; i < json_DOut.length; i++) {
					document.getElementsByClassName("digitalOut")[i].checked = json_DOut[i];
				}
			}
		}
	}

	ws.onclose = function() {
		document.getElementById("WebsocketStatus").innerHTML = "Not connected";
		document.getElementById("WebsocketStatus").style.color = "rgb(200, 0, 0)";
		document.getElementById("startWebsocket").textContent = "Connect websocket";
	}
}

function ChangeOutput(name,value) {
	ws.send(JSON.stringify({"Name": name, "Value": value}));
}