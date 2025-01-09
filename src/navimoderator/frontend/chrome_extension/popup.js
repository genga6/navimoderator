document.querySelectorAll('.tab-link').forEach(tab => {
    tab.addEventListener('click', (e) => {
        document.querySelectorAll('.tab-link').forEach(link => link.classList.remove('active'));

        e.target.classList.add('active');

        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

        const targetTab = e.target.getAttribute('data-tab');
        document.getElementById(targetTab).classList.add('active');
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const toggleSwitch = document.getElementById("toggleSwitch");
    const switchLabel = document.getElementById("switchLabel");
    const container = document.querySelector(".container");
    const title = document.querySelector(".title");
    const switchContainer = document.querySelector(".switch-container");

    // スイッチの切り替え動作
    toggleSwitch.addEventListener("change", () => {
        const isEnabled = toggleSwitch.checked;
        switchLabel.textContent = isEnabled ? "ON" : "OFF";

        // タイトルとスイッチコンテナを除外して無効化/有効化
        Array.from(container.children).forEach(child => {
            if (child !== title && child !== switchContainer) {
                if (!isEnabled) {
                    child.classList.add("disabled");
                } else {
                    child.classList.remove("disabled");
                }
            }
        });
    });

    // 初期化：スイッチの状態に応じて設定
    if (!toggleSwitch.checked) {
        Array.from(container.children).forEach(child => {
            if (child !== title && child !== switchContainer) {
                child.classList.add("disabled");
            }
        });
    }
});

document.getElementById("google-login-button").addEventListener("click", () => {
    // Google OAuthフローを開始する関数を呼び出し
    gapi.auth2.init({
        client_id: 'YOUR_CLIENT_ID',
        scope: 'https://www.googleapis.com/auth/youtube.readonly'
    }).then(() => {
        const authInstance = gapi.auth2.getAuthInstance();
        authInstance.signIn().then(user => {
            const accessToken = user.getAuthResponse().access_token;
            console.log('Access Token:', accessToken);
            alert("ログインに成功しました！");
            // アプリにログイン情報を送信するロジックを追加
        });
    });
});
