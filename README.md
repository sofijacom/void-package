# Void Linux Software Repository

This repo contains packages that I want but have not found in any of the [mirrors](https://xmirror.voidlinux.org/).

> *__NOTE__*: Should you really use random binaries of the internet???

> Your warranty is now void.<br>
> I am not responsible for bricked devices, failed installations, thermonuclear war,
> or you getting fired because the computer failed.<br>
> Please do some research if you have any concerns about the content of this repo. <br>
> If you point the finger at me for messing up your installation, I will laugh at you.

# How to use
```shell
printf "repository=https://github.com/sofijacom/void-package/releases/latest/download/\n" > /etc/xbps.d/sofijacom-void-repository.conf
xbps-install -S
```


# Available packages
| package | source | automatic update |
|:--------|:-------|:-----------------|
| brave-browser (stable) | https://www.brave.com/                            | :white_check_mark: |
| destilled-fonts        | <opinionized list of fonts I want>                | :x: |
| ly (TUI dm)            | https://github.com/fairyglade/ly                  | :white_check_mark: |
| obsidian.md            | https://obsidian.md/                              | :white_check_mark: |
| openshift-oc (oc cli)  | https://github.com/openshift/oc                   | :white_check_mark: |
| pet                    | https://github.com/knqyf263/pet                   | :white_check_mark: |
| pexip-infinity-connect | https://www.pexip.com/                            | :x: |
| rebos                  | https://gitlab.com/Oglo12/rebos                   | :white_check_mark: |
| river-bedload          | https://git.sr.ht/~novakane/river-bedload         | :x: |
| river-status           | https://github.com/grvn/river-status              | :white_check_mark: |
| vesktop                | https://vesktop.vencord.dev/                      | :white_check_mark: |
| wideriver              | https://github.com/alex-courtis/wideriver         | :white_check_mark: |
| zen-browser (stable)   | https://www.zen-browser.app/                      | :white_check_mark: |
