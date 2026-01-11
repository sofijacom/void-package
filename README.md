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
| mullvad VPN            | https://github.com/mullvad/mullvadvpn-app/        | :x: |
| palemoon ( browser )   | https://www.palemoon.org/                         | :x: |
| SeaMonkey              | https://www.seamonkey-project.org/                | :x: |
| SmartGit               | https://www.smartgit.dev/                         | :x: |
| waterfox-browser       | https://www.waterfox.net/                         | :heavy_check_mark: |
| yandex-browser (stable)| https://repo.yandex.ru/                           | :x: |
| zen-browser (stable)   | https://www.zen-browser.app/                      | :heavy_check_mark: |


# _Yandex-Browser-for-Void-Linux ![void](https://github.com/sofijacom/yandex-browser/assets/107557749/0cb14595-dcea-4f79-84a4-0185b1df379d)_


Install codec:
```
# perform this action if you already had the codec installed

sudo rm "/opt/yandex/browser/libffmpeg.so"
```
```
sudo /opt/yandex/browser/update_codecs /opt/yandex/browser || true
```
> [!NOTE]
> _The assembly template for Yandex-browser has been improved, now the codec "libffmpeg.so" does not need to be installed manually, it will be installed when installing the package_
