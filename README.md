# rtmp-bitrate-html
Simple HTML / Javascript webpage that shows current bitrate of desired RTMP server.

---
## Configure the file:
---
The following line configures your RTMP server location;

### Line 33:
```javascript
const response = await fetch("http://localhost/stat");
```
---

The example below is for the stream /live (publish/live) if you have changed this make sure to change it accordingly;

### Line 36:
```javascript
const live = parse.getElementsByTagName("live")[0];
```
---

The following line configures how often you want the bitrate to update, depending on how often the RTMP updates your /stat page;

### Line 48:
```javascript
setInterval(getBitrate, 2000);
```
---

After everything is configured correctly, save it and add the `bitrate.html` as a browser source in OBS.

Enjoy!
-b3ck
