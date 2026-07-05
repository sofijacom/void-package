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
| _Brave-browser ( stable )_            | https://www.brave.com/                            | ✔️ |
| _Brave-origin ( stable )_             | https://www.brave.com/                            | ✔️ |
| _Brave-origin ( beta )_               | https://www.brave.com/                            | ✔️ |
| _Calamares ( Graphical installer )_   | https://calamares.io                              | ✔️ |
| _Conky-manager2_                      | https://github.com/zcot/conky-manager2            | 🔐 | 
| _GitHub-desktop_                      | https://github.com/shiftkey/desktop               | ✔️ |
| _Google-chrome ( stable )_            | https://www.google.com/chrome/                    | ✔️ |
| _Gtk3dialog ( GTK+ 3, VTE )_          | https://github.com/puppylinux-woof-CE/gtkdialog   | ✔️ |
| _Hardinfo2_                           | https://github.com/hardinfo2/hardinfo2            | ✔️ |
| _Helium-browser_                      | https://helium.computer/                          | ✔️ |
| _LibreWolf ( Web browser )_           | https://librewolf.net/                            | ✔️ |
| _ly_                                  | https://codeberg.org/fairyglade/ly                | ✔️ |
| _Microsoft-edge ( Web browser )_      | https://github.com/NDViet/microsoft-edge-stable   | ✔️ |
| _Mullvad-browser_                     | https://github.com/mullvad/mullvad-browser        | ✔️ |
| _Mullvad VPN_                         | https://github.com/mullvad/mullvadvpn-app/        | ✔️ |
| _Palemoon ( browser )_                | https://www.palemoon.org/                         | ✔️ |
| _Pup-volume-monitor_                  | https://github.com/01micko/pup-volume-monitor     | 🔐 |
| _Osmo + dependency (libgringotts)_    | https://sourceforge.net/projects/osmo-pim/files/  | 🔐 |
| _SeaMonkey ( Web-browser )_           | https://www.seamonkey-project.org/                | ✔️ |
| _SmartGit_                            | https://www.smartgit.dev/                         | ✔️ |
| _Waterfox-browser_                    | https://www.waterfox.net/                         | ✔️ |
| _Yandex-browser ( stable )_           | https://repo.yandex.ru/                           | ✔️ |
| _Zen-browser ( stable )_              | https://www.zen-browser.app/                      | ✔️ |

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
