# Void Linux Software Repository

# How to use
```shell
printf "repository=https://github.com/sofijacom/void-package/releases/latest/download/\n" | sudo tee /etc/xbps.d/sofijacom-void-repository.conf
sudo xbps-install -S
```


# Available packages
| package | source | automatic update |
|:--------|:-------|:-----------------|
| brave-browser (stable) | https://www.brave.com/                            | :white_check_mark: |
| github-desktop         | https://desktop.github.com                        | :x: |
| google-chrome (stable) | https://www.google.com/chrome/                    | :x: |
| palemoon ( browser )   | https://www.palemoon.org/                         | :x: |
| waterfox-browser       | https://www.waterfox.net/                         | :white_check_mark: |
| yandex-browser (stable)| https://repo.yandex.ru/                           | :x: |
| zen-browser (stable)   | https://www.zen-browser.app/                      | :white_check_mark: |


# Archived packages
| package | source | reason |
|:--------|:-------|:-----------------|
| pet                    | https://github.com/knqyf263/pet                   | available in [upstream void-packages](https://github.com/void-linux/void-packages) |
| river-bedload          | https://git.sr.ht/~novakane/river-bedload         | available in [upstream void-packages](https://github.com/void-linux/void-packages) |


# _Yandex-Browser-for-Void-Linux ![void](https://github.com/sofijacom/yandex-browser/assets/107557749/0cb14595-dcea-4f79-84a4-0185b1df379d)_


Install codec:
```
# perform this action if you already had the codec installed

sudo rm "/opt/yandex/browser/libffmpeg.so"
```
```
sudo /opt/yandex/browser/update_codecs /opt/yandex/browser || true
```
