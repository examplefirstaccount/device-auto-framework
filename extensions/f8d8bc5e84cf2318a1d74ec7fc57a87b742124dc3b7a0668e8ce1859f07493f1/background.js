
const config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "192.177.61.43",
            port: 64144
        }
    }
}
chrome.proxy.settings.set({
    value: config,
    scope: 'regular'
}, () => {});

chrome.webRequest.onAuthRequired.addListener(
  (details, callback) => {
    const authCredentials = {
      username: "PDdt6CfS",
      password: "1Rv4qxJX",
    };
    setTimeout(() => {
      callback({ authCredentials });
    }, 200);
  },
  { urls: ["<all_urls>"] },
  ["asyncBlocking"]
);

