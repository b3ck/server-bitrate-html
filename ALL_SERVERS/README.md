# Configure the way it looks:

## Modify line 107 to change how it looks when there is NO incoming bitrate:

Default for line 107 will show nothing.
```javascript
document.getElementById('bitrate').innerHTML = null;
```

### Here are some examples:
Example #1; this will show: `0`
```javascript
document.getElementById('bitrate').innerHTML = "0";
```

Example #2; this will show: `NO SIGNAL`
```javascript
document.getElementById('bitrate').innerHTML = "NO SIGNAL";
```

Example #3; this will show: `WHATEVER`
```javascript
document.getElementById('bitrate').innerHTML = "WHATEVER";
```
---
## Modify line 110 to change how it looks when there IS incoming bitrate:

Default for line 110 will show: `XXXX kb/s`.
```javascript
document.getElementById('bitrate').innerHTML = bitrate + " kb/s";
```

### Here are some examples:
Example #1; this will show: `bitrate: XXXX kb/s`
```javascript
document.getElementById('bitrate').innerHTML = "bitrate: " + bitrate + " kb/s";
```

Example #2; this will show: `blah blah XXXX kb/s`
```javascript
document.getElementById('bitrate').innerHTML = "blah blah " + bitrate + " kb/s";
```

---

# Configure the way the script fetches the bitrate:

## Line 115; 
The following line configures the interval the script fetches all of the bitrates from the server stats pages in the array, this is in milliseconds, so 2000 would equal 2 seconds.
```javascript
    let interval = 2000;
```


## Lines 117-119;
## Modify the following lines to match your server(s) setup, make your changes accordingly;

Line 117; if you're using SRT this would be your `streamid`, in the example below 'publish/live/feed1'
```javascript
{ server: "SRT", page: "http://127.0.0.1:8181/stats", key: "publish/live/feed1" },
```

Line 118; if you're using NMS this would be your `application` + `key`, in the example below 'live' is the application and 'feed1' is the key.
```javascript
{ server: "NMS", page: "http://localhost:8000/api/streams/live/feed1" },
```

Line 119; if you're using NGINX this would be just your `key`, so if you go with the default, it would be 'live'
```javascript
{ server: "NGINX", page: "http://localhost/stat", key: "live" }
```
---


After everything is configured correctly, save it and add the `bitrate.html` as a browser source in OBS.

Enjoy!
-b3ck
