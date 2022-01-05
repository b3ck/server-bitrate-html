## Configure the file:
---
##### The following line configures your NMS RTMP server stats location;

### Line 48:
```javascript
const response = await fetch("http://localhost/api/streams/live/cam1");
```
##### So if you stream to `rtmp://XX.XX.XX.XX:1935/publish/live` then replace the above code `/live/cam1/` with `/publish/live`.
---

##### The following line configures how often you want the bitrate to update (time is in ms), NMS updates it's stats page in real-time, so it's up to you;

### Line 59:
```javascript
setInterval(getBitrate, 2000);
```
---

After everything is configured correctly and edited to your liking, save it and add the `bitrate.html` as a browser source in OBS.

Make sure to add it as a local file:

![image](https://user-images.githubusercontent.com/1740542/148205807-36c35fe7-f004-43cd-ad17-c785df2d9076.png)

#### Enjoy! -b3ck
