var changeOutput = "";

function StartJsScript() {
	//document.getElementById("startButton").style.display = "none";
	var elems = document.getElementsByClassName("IO_box");
	for (var i = 0; i < elems.length; i++) {
	elems[i].style.display = "block";
	}
	
	GetFRDMk64FIO();
	//setInterval(GetFRDMk64FIO,1000);
}

function GetFRDMk64FIO() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (this.readyState == 4) { //&& this.states == 200) {
			console.log(this.states)
			if (this.responseXML != null) {
				var xmlDoc = xmlhttp.responseXML;
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
	xmlhttp.open("GET", "ajaxInputs_random.xml" + "?t=" + Math.random() + changeOutput, true);
	xmlhttp.send();
	console.log(changeOutput)
	changeOutput = "";
}

function ChangeOutput(name,value) {
	if (changeOutput.search("name") == -1) {
		changeOutput = "&" + name + "=" + value;
	}
	else {
		changeOutput = changeOutput.replace("&" + name + "=" + !value, "&" + name + "=" + value);
	}
	console.log(changeOutput)
}