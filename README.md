# Void Linux Software Repository

This repo contains packages not found in any of the [mirrors](https://xmirror.voidlinux.org/).

> *__NOTE__*: Should you really use random binaries of the internet???

> Your warranty is now void.<br>
> I am not responsible for bricked devices, failed installations, thermonuclear war, 
> or you getting fired because the computer failed.<br>
> Please do some research if you have any concerns about the content of this repo <br>
> If you point the finger at me for messing up your installation, I will laugh at you.

# How to use
```shell
printf "repository=https://github.com/grvn/void-packages/releases/latest/download/\n" > /etc/xbps.d/grvn-void-repository.conf
xbps-install -S
```