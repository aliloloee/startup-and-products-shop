function EasyHTTP(){
    this.http = new XMLHttpRequest();
}

EasyHTTP.prototype.get = function (url, callback) {
    this.http.open('GET', url, true);
    this.http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    let self = this;
    this.http.onload = function (){
        if (self.http.status === 200){
            callback(null, self.http.responseText);
        }else {
            callback('Error: ' + self.http.status);
        }
    }

    this.http.send();
}

EasyHTTP.prototype.post = function (url, csrfToken, data, callback) {
    this.http.open('POST', url, true);
    this.http.setRequestHeader('Content-type', 'application/json');
    this.http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    this.http.setRequestHeader('X-CSRFToken', `${csrfToken}`);

    let self = this;
    this.http.onload = function (){
        if (self.http.status === 201) {
            callback(null, self.http.responseText);
        } else {
            callback('Error: ' + self.http.status);
        }
    }

    this.http.send(JSON.stringify(data));
}

EasyHTTP.prototype.put = function (url, csrfToken, data, callback) {
    this.http.open('PUT', url, true);
    this.http.setRequestHeader('Content-type', 'application/json');
    this.http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    this.http.setRequestHeader('X-CSRFToken', `${csrfToken}`);

    let self = this;
    this.http.onload = function (){
        if (self.http.status === 200) {
            callback(null, self.http.responseText);
        } else {
            callback('Error: ' + self.http.status);
        }
    }

    this.http.send(JSON.stringify(data));
}


EasyHTTP.prototype.delete = function (url, csrfToken, data, callback) {
    this.http.open('DELETE', url, true);
    this.http.setRequestHeader('Content-type', 'application/json');
    this.http.setRequestHeader('X-Requested-With', 'XMLHttpRequest'); 
    this.http.setRequestHeader('X-CSRFToken', `${csrfToken}`);

    let self = this;
    this.http.onload = function (){
        if (self.http.status === 200){
            callback(null, self.http.responseText);
        }else {
            callback('Error: ' + self.http.status);
        }
    }

    this.http.send(JSON.stringify(data));
}

// Only for accounts

EasyHTTP.prototype.post_account = function (url, csrfToken, data, callback) {
    this.http.open('POST', url, true);
    this.http.setRequestHeader('Content-type', 'application/json');
    this.http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    this.http.setRequestHeader('X-CSRFToken', `${csrfToken}`);

    let self = this;
    this.http.onload = function (){
        if (self.http.status === 201 || self.http.status === 208) {
            callback(null, self.http.responseText, self.http.status);
        } else {
            callback('Error: ' + self.http.status);
        }
    }

    this.http.send(JSON.stringify(data));
}
