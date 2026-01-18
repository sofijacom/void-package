# Void Linux Software Repository

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
| brave-browser (stable) | https://www.brave.com/                            | :heavy_check_mark: |
| github-desktop         | https://github.com/shiftkey/desktop               | :x: |
| google-chrome (stable) | https://www.google.com/chrome/                    | :x: |
| hardinfo2              | https://github.com/hardinfo2/hardinfo2            | :heavy_check_mark: |
| mullvad VPN            | https://github.com/mullvad/mullvadvpn-app/        | :heavy_check_mark: |
| palemoon ( browser )   | https://www.palemoon.org/                         | :x: |
| Osmo                   | https://sourceforge.net/projects/osmo-pim/files/  | :x: |
| SeaMonkey              | https://www.seamonkey-project.org/                | :x: |
| SmartGit               | https://www.smartgit.dev/                         | :x: |
| waterfox-browser       | https://www.waterfox.net/                         | :heavy_check_mark: |
| yandex-browser (stable)| https://repo.yandex.ru/                           | :x: |
| zen-browser (stable)   | https://www.zen-browser.app/                      | :heavy_check_mark: |
