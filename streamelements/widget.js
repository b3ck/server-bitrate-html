let interval = 2000;
let stats = [];

window.addEventListener('onWidgetLoad', function(obj) {
  const fieldData = obj.detail.fieldData;
  interval = fieldData.interval;
  stats = [
    { server: fieldData.serverType1, page: fieldData.statsURL1, key: fieldData.key1, rtt: fieldData.rtt1 === "yes" },
    { server: fieldData.serverType2, page: fieldData.statsURL2, key: fieldData.key2, rtt: fieldData.rtt2 === "yes" },
    { server: fieldData.serverType3, page: fieldData.statsURL3, key: fieldData.key3, rtt: fieldData.rtt3 === "yes" },
    { server: fieldData.serverType4, page: fieldData.statsURL4, key: fieldData.key4, rtt: fieldData.rtt4 === "yes" }
  ];

  // Apply custom styles
  const customCSS = `
    body {
      font-family: '${fieldData.fontName}', sans-serif;
      color: ${fieldData.fontColor};
      font-size: ${fieldData.fontSize}px;
      font-weight: ${fieldData.fontWeight};
      text-align: ${fieldData.textAlign};
      text-shadow: ${fieldData.textShadow};
      padding: ${fieldData.textPadding}px;
    }
  `;
  document.getElementById('custom-css').innerHTML = customCSS;

  run(stats, interval);
});

const tryFetch = async (page) => {
  try {
    return await fetch(page);
  } catch (error) {
    console.log(page, error);
  }
  return null;
}

const getSrtBitrate = async (page, publisher) => {
  const response = await tryFetch(page);
  if (!response) return null;

  const srtdata = await response.json();
  if (srtdata.publishers[publisher] == null) return null;

  const { bitrate, rtt } = srtdata.publishers[publisher];
  return { bitrate, rtt };
};

const getNmsBitrate = async (page) => {
  const response = await tryFetch(page);
  if (!response) return null

  const { bitrate } = await response.json();

  if (!bitrate) return null;

  return { bitrate };
};

const getNginxBitrate = async (page, key) => {
  const response = await tryFetch(page);
  if (!response) return null

  const data = await response.text();
  const parse = new window.DOMParser().parseFromString(data, "text/xml");
  const live = parse.getElementsByTagName(key)[0];

  const node = live.childNodes[1].childNodes[14];

  if (!node) return null;

  const bitrate = Math.round(node.childNodes[0].nodeValue / 1024);
  return { bitrate };
};

const run = async (stats, interval) => {
  setText(await getBitrate(stats))

  setInterval(async () => {
    setText(await getBitrate(stats));
  }, interval);
}

const getBitrate = async (stats) => {
  const get = {
    "SRT": getSrtBitrate,
    "NMS": getNmsBitrate,
    "NGINX": getNginxBitrate,
  }

  const values = await Promise.all(stats.map(s => get[s.server](s.page, s.key)));
  const index = values.findIndex(el => el);

  return [values[index], stats[index]];
}

const setText = (stats) => {
  [stats, origin] = stats;
  const { bitrate, rtt } = stats || {};
  const el = document.getElementById('bitrate');

  if (!bitrate) {
    el.innerHTML = null;
    return;
  }

  if (origin.rtt && rtt !== undefined) {
    el.innerHTML = `${bitrate} kb/s • ${Math.round(rtt)} RTT`;
  } else {
    el.innerHTML = `${bitrate} kb/s`;
  }
}

