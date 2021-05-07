## Configure the file:
---
##### The following line configures your DOCKER SLS SRT server stats location;

### Line 35:
```javascript
const srtresponse = await fetch('http://127.0.0.1:8181/stats');
```
##### Make sure you have the correct PORT, in the example above it is `8181`.
---
### Line(s) 38 & 39:
```javascript
      if (srtdata.publishers["publish/live/feed1"] != null) {
        const stream = srtdata.publishers["publish/live/feed1"];
```

##### So if your SRT streamid is `publish/live/phone` then replace both instances of the above code `publish/live/feed1` with `publish/live/phone`.
---

##### The following line configures how often you want the bitrate to update (time is in ms), DOCKER SLS SRT server updates it's stats page in real-time, so it's up to you how often you want to update it on your overlay;

### Line 48:
```javascript
setInterval(getBitrate, 1000);
```
---

##### After everything is configured correctly, save it and add the `bitrate.html` as a browser source in OBS.

#### Enjoy! -b3ck
