# Linkline Android QA shell

This branch packages the hosted-Preview-approved Linkline web bundle into a local Android WebView APK.

- package: `com.linkline.game`
- web origin inside WebView: `https://linkline.local/`
- web bundle baseline: public Preview commit `1c17f6ae2899fc2c3c7420ecb81c0ca60e73a0e1`
- no Production Worker dependency at runtime
- first build is debug-signed for physical-device QA only

The build workflow refuses to run if the embedded web bundle differs from the frozen Preview baseline.
