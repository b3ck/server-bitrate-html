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

After everything is configured correctly and edited to your liking, save it and add the `bitrate.html` as a browser source in OBS.

Make sure to add it as a local file:

![image](https://user-images.githubusercontent.com/1740542/148205807-36c35fe7-f004-43cd-ad17-c785df2d9076.png)

Enjoy!
-b3ck
