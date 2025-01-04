chrome.runtime.onInstalled.addListener(() => {
    console.log("NaviModerator Installed");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "authenticate") {
        const clientId = "YOUR_CLIENT_ID";
        const redirectUri = chrome.identity.getRedirectURL();
        const scope = "https://www.googleapis.com/auth/youtube.force-ssl";
        const authUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${clientId}&response_type=token&redirect_uri=${redirectUri}&scope=${scope}`;

        chrome.identity.launchWebAuthFlow({ url: authUrl, interactive: true }, (redirectUrl) => {
            if (chrome.runtime.lastError || !redirectUrl) {
                console.error(chrome.runtime.lastError);
                sendResponse({ success: false });
                return;
            }

            const token = new URL(redirectUrl).hash.split('&').find(el => el.includes('access_token')).split('=')[1];
            chrome.storage.local.set({ accessToken: token }, () => {
                console.log("Access token saved!");
                sendResponse({ success: true, accessToken: token });
            });
        });

        return true; // Indicates async response
    }
});
