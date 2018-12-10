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
			parser = new DOMParser();
			xmlDoc = parser.parseFromString(evt.data,"text/xml");
			if (xmlDoc != null) {
				var xmlAIn = xmlDoc.getElementsByTagName('AIn');
				for (var i = 0; i < xmlAIn.length; i++) {
					document.getElementsByClassName("analogIn")[i].innerHTML = xmlAIn[i].childNodes[0].nodeValue;
				}
				var xmlDIn = xmlDoc.getElementsByTagName('DIn');
				for (var i = 0; i < xmlDIn.length; i++) {
					document.getElementsByClassName("digitalIn")[i].innerHTML = xmlDIn[i].childNodes[0].nodeValue;
				}
				var xmlDOut = xmlDoc.getElementsByTagName('DOut');
				for (var i = 0; i < xmlDOut.length; i++) {
					if (xmlDOut[i].childNodes[0].nodeValue == "High") {
						document.getElementsByClassName("digitalOut")[i].checked = true;
					}
					else {
						document.getElementsByClassName("digitalOut")[i].checked = false;
					}
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