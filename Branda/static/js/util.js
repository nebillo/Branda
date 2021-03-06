/**
* Returns an XMLHttp instance to use for asynchronous
* downloading. This method will never throw an exception, but will
* return NULL if the browser does not support XmlHttp for any reason.
* @return {XMLHttpRequest|Null}
*/
function createXmlHttpRequest() {
 try {
   if (typeof ActiveXObject != 'undefined') {
     return new ActiveXObject('Microsoft.XMLHTTP');
   } else if (window["XMLHttpRequest"]) {
     return new XMLHttpRequest();
   }
 } catch (e) {
   changeStatus(e);
 }
 return null;
};

/**
* This functions wraps XMLHttpRequest open/send function.
* It lets you specify a URL and will call the callback if
* it gets a status code of 200.
* @param {String} url The URL to retrieve
* @param {Function} callback The function to call once retrieved.
*/
function downloadUrl(url, type, data, callback) {
 var status = -1;
 var request = createXmlHttpRequest();
 if (!request) {
   return false;
 }

 request.onreadystatechange = function() {
   if (request.readyState == 4) {
     try {
       status = request.status;
     } catch (e) {
       // Usually indicates request timed out in FF.
     }
     if (status == 200) {
       callback(request.responseText);
       request.onreadystatechange = function() {};
     }
   }
 }
 request.open(type, url, true);
 if (type == "POST") {
  request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  request.setRequestHeader("Content-length", data.length);
  request.setRequestHeader("Connection", "close"); 
 }

 try {
   request.send(data);
 } catch (e) {
   changeStatus(e);
 }
};


function downloadScript(url) {
  var script = document.createElement('script');
  script.src = url;
  document.body.appendChild(script);
}


function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}


function buildQueryString(dictionary) {
  var string = "";
  // For each key-value pair
  var count = 0;
  for (var key in dictionary) {
    if (count == 0) {
      string += "?";
    } else {
      string += "&";
    }
    var value = dictionary[key];
    string += encodeURIComponent(key) + "=" + encodeURIComponent(value);
    count ++;
  }
  return string;
}

