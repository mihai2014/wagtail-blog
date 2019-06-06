function getXHR(){
    var xhr = false;
    if (window.XMLHttpRequest) {
        xhr = new XMLHttpRequest();
    } else { //code for IE6, IE5
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhr;
}

function GetData() {
    var milisec1 = Date.now();

    // Instantiate XHR
    xhr = getXHR();
    if(!xhr) {
        alert("Ajax is not supported by your browser!");
        return;
    }

    // Handle Response from Server
    xhr.onreadystatechange = function () {
        if (xhr.readyState < 4)
            document.getElementById('div1').innerHTML = "Sending...";
        else if (xhr.readyState === 4) {
            if (xhr.status == 200 && xhr.status < 300){
                var milisec2 = Date.now();
                var dt = (milisec2 - milisec1).toString();
                document.getElementById('div1').innerHTML = xhr.responseText + " (" + dt + " milisec delay)";
            }
            else
                document.getElementById('div1').innerHTML = "Error: " + xhr.status;
        }
    }
    xhr.onerror = function() {
        document.getElementById('div1').innerHTML = "Error: No response from server.";
    }

    // Send data to server
    var timeout = document.getElementById('timeout').value;
    xhr.open('GET', 'reply/?timeout='+timeout);
    xhr.send(null);
}

function GET(req,successHandler,responseFormat,errorHandler){

    // Instantiate XHR
    xhr = getXHR();
    if(!xhr) {
        alert("Ajax is not supported by your browser!");
        return;
    }

    //process response
    xhr.onload = function() {
        if (xhr.status === 200) {
                response = xhr.responseText;
                if(responseFormat == "txt") response = xhr.responseText;
                if(responseFormat == "json") response = JSON.parse(xhr.responseText);
                if (successHandler) successHandler(response);
        }
        else{
                var err_name = err_codes[xhr.status][0];
                var err_state = err_codes[xhr.status][1];
                var fullDescription = err_codes[xhr.status][2];
                if(errorHandler)
                    errorHandler(xhr.status);
                else
                    alert("Error " + xhr.status + " : " + err_name + "\n[" + err_state + " - " + fullDescription+"]");
        }
    }

    xhr.onerror = function() {
        alert("Error: No response from server.");
    }

    // Send data to server
    xhr.open('GET', req);
    xhr.send(null);
}


