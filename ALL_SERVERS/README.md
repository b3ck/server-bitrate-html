# How to edit and use `bitate.html`:
Open up the `bitrate.html` in your favorite code editor, once open follow the instructions below.

---
# Configure the way the script fetches the bitrate:

## Line 127; 
The following line configures the interval the script fetches all of the bitrates from the server stats pages in the array, this is in milliseconds, so 2000 would equal 2 seconds.
```javascript
const interval = 2000;
```


## Lines 129-131;
## Modify the following lines to match your server(s) setup, make your changes accordingly;

Line 129; if you're using SRT this would be your `streamid`, in the example below 'publish/live/feed1', if you do not want to show RTT then change 'rtt: true' to 'rtt: false'
```javascript
{ server: "SRT", page: "http://127.0.0.1:8181/stats", key: "publish/live/test", rtt: true },
```

Line 130; if you're using NMS this would be your `application` + `key`, in the example below 'live' is the application and 'feed1' is the key.
```javascript
{ server: "NMS", page: "http://localhost:8000/api/streams/live/feed1" },
```

Line 131; if you're using NGINX this would be just your `key`, so if you go with the default, it would be 'live'
```javascript
{ server: "NGINX", page: "http://localhost/stat", key: "live" }
```
---

# Configure the way it looks:

## Modify line 114 to change how it looks when there is NO incoming bitrate:

Default for line 114 will show nothing.
```javascript
el.innerHTML = null;
```

### Here are some examples:
Example #1; this will show: `0`
```javascript
el.innerHTML = `0`;
```

Example #2; this will show: `NO SIGNAL`
```javascript
el.innerHTML = `NO SIGNAL`;
```

Example #3; this will show: `WHATEVER`
```javascript
el.innerHTML = `WHATEVER`;
```
---
## Modify line 119 to change how it looks when there IS incoming bitrate:

Default for line 119 will show: `XXXX kb/s`.
```javascript
el.innerHTML = `${bitrate} kb/s`;
```

### Here are some examples:
Example #1; this will show: `bitrate: XXXX kb/s`
```javascript
el.innerHTML = `bitrate: ${bitrate} kb/s`;
```

Example #2; this will show: `blah blah XXXX kb/s`
```javascript
el.innerHTML = `blah blah ${bitrate} kb/s`;
```

---


After everything is configured correctly and edited to your liking, save it and add the `bitrate.html` as a browser source in OBS.

Enjoy!
-b3ck
