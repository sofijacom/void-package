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
| Osmo + dependency ( libgringotts )                   | https://sourceforge.net/projects/osmo-pim/files/  | :x: |
| SeaMonkey              | https://www.seamonkey-project.org/                | :x: |
| SmartGit               | https://www.smartgit.dev/                         | :x: |
| waterfox-browser       | https://www.waterfox.net/                         | :heavy_check_mark: |
| yandex-browser (stable)| https://repo.yandex.ru/                           | :x: |
| zen-browser (stable)   | https://www.zen-browser.app/                      | :heavy_check_mark: |

> repo-key
>> repo-key `00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist`
>>>  ```
>>>   cp ./repo-keys/x86_64/00_ca_42_57_c9_c0_9a_ec_94_b4_7d_97_e5_a9_aa_1e.plist /var/db/xbps/keys/00:ca:42:57:c9:c0:9a:ec:94:b4:7d:97:e5:a9:aa:1e.plist
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
