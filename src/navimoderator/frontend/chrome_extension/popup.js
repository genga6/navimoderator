document.getElementById("authenticate").addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "authenticate" }, (response) => {
        const status = document.getElementById("status");
        if (response.success) {
            status.textContent = "Authenticated successfully!";
            console.log("Access Token:", response.accessToken);
        } else {
            status.textContent = "Authentication failed.";
            console.error("Authentication error");
        }
    });
});
