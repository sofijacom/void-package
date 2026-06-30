<div align="center" markdown="1">
  <a>
  <!-- <img width="600" height="120" alt="void-linux" src="https://github.com/sofijacom/void-package/blob/main/img/void-linux.gif" /> -->
  <img width="350" height="auto" alt="void-linux" src="https://github.com/sofijacom/void-package/blob/main/img/void-linux-1.png?raw=true" />
  </a>
<!-- # 【 Void Linux Software Repository 】 -->
<!-- # 【 Unofficial package repository for Void Linux 】 -->

##### 【 `Unofficial package repository` 】

[![Platform](https://img.shields.io/badge/platform-Void%20Linux-478061?logo=linux&colorA=363a4f)](#)
[![x85_64-glibc](https://img.shields.io/badge/x86__64-glibc-478061?style=badge&colorA=363a4f)](#)

[![Build](https://img.shields.io/github/actions/workflow/status/sofijacom/void-package/build.yml?style=badge&label=BUILD&logo=githubactions&logoColor=white&colorA=363a4f)](https://github.com/sofijacom/void-package/actions)
[![Build](https://img.shields.io/github/actions/workflow/status/sofijacom/void-package/update-template.yml?style=badge&label=UPDATE-TEMPLATE&logo=githubactions&logoColor=white&colorA=363a4f)](https://github.com/sofijacom/void-package/actions)
[![Updates](https://img.shields.io/github/actions/workflow/status/sofijacom/void-package/update.yml?style=badge&label=AUTO-UPDATE&logo=github&logoColor=white&colorA=363a4f)](https://github.com/sofijacom/void-package/actions)

[![GitHub](https://img.shields.io/github/license/sofijacom/void-package?style=badge&label=License&colorA=363a4f&colorB=purple&logo=gitbook)](#)
[![GitHub contributors](https://img.shields.io/github/contributors/sofijacom/void-package?style=badge&colorA=363a4f&colorB=purple&logo=github&label=Contributors)](#)
[![GitHub release (with filter)](https://img.shields.io/github/v/release/sofijacom/void-package?style=badge&logo=github&label=Release&colorA=363a4f&colorB=purple)](#)
[![GitHub issues](https://img.shields.io/github/issues-raw/sofijacom/void-package?style=badge&label=Open%20Issues&logo=github&colorA=363a4f&colorB=purple)](#)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/sofijacom/void-package?style=badge&label=Closed%20Issues&logo=github&colorA=363a4f&colorB=purple)](#)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/sofijacom/void-package/main?style=badge&label=Last%20Commit&logo=github&colorA=363a4f&colorB=purple)](#)

</div>
<br>

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
| Brave-browser ( stable )            | https://www.brave.com/                            | ✔️ |
| Brave-origin ( stable )             | https://www.brave.com/                            | ✔️ |
| Brave-origin ( beta )               | https://www.brave.com/                            | ✔️ |
| Calamares ( Graphical installer )   | https://calamares.io                              | ✔️ |
| Conky-manager2                      | https://github.com/zcot/conky-manager2            | 🔐 | 
| GitHub-desktop                      | https://github.com/shiftkey/desktop               | ✔️ |
| Google-chrome ( stable )            | https://www.google.com/chrome/                    | ✔️ |
| Gtk3dialog ( GTK+ 3 )               | https://github.com/puppylinux-woof-CE             | ✔️ |
| Hardinfo2                           | https://github.com/hardinfo2/hardinfo2            | ✔️ |
| Helium-browser                      | https://helium.computer/                          | ✔️ |
| LibreWolf ( Web browser )           | https://librewolf.net/                            | ✔️ |
| ly                                  | https://codeberg.org/fairyglade/ly                | ✔️ |
| Microsoft-edge ( Web browser )      | https://github.com/NDViet/microsoft-edge-stable   | ✔️ |
| Mullvad-browser                     | https://github.com/mullvad/mullvad-browser        | ✔️ |
| Mullvad VPN                         | https://github.com/mullvad/mullvadvpn-app/        | ✔️ |
| Palemoon ( browser )                | https://www.palemoon.org/                         | ✔️ |
| Pup-volume-monitor                  | https://github.com/01micko/pup-volume-monitor     | 🔐 |
| Osmo + dependency ( libgringotts )  | https://sourceforge.net/projects/osmo-pim/files/  | 🔐 |
| SeaMonkey ( Web-browser )           | https://www.seamonkey-project.org/                | ✔️ |
| SmartGit                            | https://www.smartgit.dev/                         | ✔️ |
| Waterfox-browser                    | https://www.waterfox.net/                         | ✔️ |
| Yandex-browser ( stable )           | https://repo.yandex.ru/                           | ✔️ |
| Zen-browser ( stable )              | https://www.zen-browser.app/                      | ✔️ |

### TODO

- [x] Build and package void-package once a new version is released via GitHub Actions
- ▷

<br>
 
<details>
<summary><b>repo-key ► Click to expand</b></summary>
	
> repo-key `00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist`
>>  ```txt
>>   cp ./repo-keys/x86_64/00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist /var/db/xbps/keys/00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist
>>  ```


```txt

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

<p align="center">
  <a>
	  <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/footers/gray0_ctp_on_line.svg?sanitize=true" />
  </a>		  
</p>

<p align="center">
	<a href="https://github.com/sofijacom/void-package/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&logo=gitbook&label=License&message=MIT&logoColor=EDE9FE&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
