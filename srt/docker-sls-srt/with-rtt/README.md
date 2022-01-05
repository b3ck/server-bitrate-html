## Configure the file:
---
##### The following line configures your DOCKER SLS SRT server stats location;

### Line 40:
```javascript
const srtresponse = await fetch('http://127.0.0.1:8181/stats');
```
##### Make sure you have the correct PORT, in the example above it is `8181`.
---
### Line(s) 43 & 44:
```javascript
      if (srtdata.publishers["publish/live/feed1"] != null) {
        const stream = srtdata.publishers["publish/live/feed1"];
```

##### So if your SRT streamid is `publish/live/phone` then replace both instances of the above code `publish/live/feed1` with `publish/live/phone`.
---

##### The following line configures how often you want the bitrate to update (time is in ms), DOCKER SLS SRT server updates it's stats page in real-time, so it's up to you how often you want to update it on your overlay;

### Line 55:
```javascript
setInterval(getBitrate, 1000);
```
---

After everything is configured correctly and edited to your liking, save it and add the `bitrate.html` as a browser source in OBS.

Make sure to add it as a local file:

![image](https://user-images.githubusercontent.com/1740542/148205807-36c35fe7-f004-43cd-ad17-c785df2d9076.png)

#### Enjoy! -b3ck
