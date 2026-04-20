<div align="center">
	
# Void Linux Software Repository

![Platform](https://img.shields.io/badge/platform-Void%20Linux-478061?logo=linux)
[![x85_64-glibc](https://img.shields.io/badge/x86__64-glibc-478061?style=badge)](#)

[![Build](https://img.shields.io/github/actions/workflow/status/sofijacom/void-package/build.yml?style=badge&label=BUILD&logo=githubactions&logoColor=white)](https://github.com/sofijacom/void-package/actions)
[![Updates](https://img.shields.io/github/actions/workflow/status/sofijacom/void-package/update.yml?style=badge&label=AUTO-UPDATE&logo=github&logoColor=white)](https://github.com/sofijacom/void-package/actions)

![GitHub](https://img.shields.io/github/license/sofijacom/void-package?style=badge&label=License&color=purple&logo=gitbook)
![GitHub contributors](https://img.shields.io/github/contributors/sofijacom/void-package?style=badge&color=purple&logo=github&label=Contributors)
![GitHub release (with filter)](https://img.shields.io/github/v/release/sofijacom/void-package?style=badge&logo=github&label=Release&color=purple)
![GitHub issues](https://img.shields.io/github/issues-raw/sofijacom/void-package?style=badge&label=Open%20Issues&logo=github&color=purple)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/sofijacom/void-package?style=badge&label=Closed%20Issues&logo=github&color=purple)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/sofijacom/void-package/main?style=badge&label=Last%20Commit&logo=github&color=purple)
<!-- style=for-the-badge -->
</div>

> [!NOTE]
>>  _How to use_
>>> _type in the terminal_

```shell
printf "repository=https://github.com/sofijacom/void-package/releases/latest/download/\n" | sudo tee /etc/xbps.d/sofijacom-void-repository.conf
```

> [!IMPORTANT]
> 
> _Then type in the terminal `sudo xbps-install -S` and accept the fingerprint (Y)_

```shell
sudo xbps-install -S
```


# Available packages
| package | source | automatic update |
|:--------|:-------|:-----------------|
| Brave-browser (stable) | https://www.brave.com/                            | :heavy_check_mark: |
| GitHub-desktop         | https://github.com/shiftkey/desktop               | :x: |
| Google-chrome (stable) | https://www.google.com/chrome/                    | :x: |
| Hardinfo2              | https://github.com/hardinfo2/hardinfo2            | :heavy_check_mark: |
| LibreWolf (web browser)| https://librewolf.net/                            | :x: |
| Microsoft-edge (browser)| https://github.com/NDViet/microsoft-edge-stable  | :x: |
| Mullvad VPN            | https://github.com/mullvad/mullvadvpn-app/        | :heavy_check_mark: |
| Palemoon ( browser )   | https://www.palemoon.org/                         | :x: |
| Pup-volume-monitor     | https://github.com/01micko/pup-volume-monitor     | :x: |
| Osmo + dependency ( libgringotts )                   | https://sourceforge.net/projects/osmo-pim/files/  | :x: |
| SeaMonkey (Web-browser)| https://www.seamonkey-project.org/                | :x: |
| SmartGit               | https://www.smartgit.dev/                         | :x: |
| Waterfox-browser       | https://www.waterfox.net/                         | :heavy_check_mark: |
| Yandex-browser (stable)| https://repo.yandex.ru/                           | :x: |
| Zen-browser (stable)   | https://www.zen-browser.app/                      | :heavy_check_mark: |

<details>
<summary><b>repo-key</b></summary>
	
> repo-key
>> repo-key `00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist`
>>>  ```
>>>   cp ./repo-keys/x86_64/00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist /var/db/xbps/keys/00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist
>>>  ```


```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>public-key</key>
	<data>LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF6aFR1SkVjalBFZzZaUnNGbThtLwpaRnY0RWoyNUZVZzRZR3JQZlI3cWdaaGs5MExWd1hnTnVBQVl2TXFrSmpDd1dueEdYZVNzWUgyNFpSaFhiSHNvCm1DOGJFSDBOWkpmWGRYWFl3Rjg1dGl3b0RGRkpxOE0wN3daT0JsVmI4YXhkRm96UElpWXlRUEMxN1BwTjg0UksKS3NzZkJtQmt0dDUwbGptUWpmQW5lV21tZzF5VTRlSWZvR3AvamgrWW9TUGkyTzZTQi9ZVVJpZnNFYmlUK1RoMQpGdmpZTWhCb1VmQ2NGaGlIb3hDWXJOREhNOURSM21lUVI5ZkFuTEhKNEdXclhoMy84TjFhTngwcnZXckdSNDlJCkJrenNJdjErL2hHNzdyVG54Z3VPNGx0QVZ0QnljdVhRa2ZoWlpzMCtNSXphMzZpaVJja1lVRVVzYVFtQkJnUXMKaHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==</data>
	<key>public-key-size</key>
	<integer>2048</integer>
	<key>signature-by</key>
	<string>void-package-github-actions</string>
</dict>
</plist>
```

</details>
