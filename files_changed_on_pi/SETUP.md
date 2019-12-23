# Set up everything

Basically follow this guides
[Wireless Access Point](https://pimylifeup.com/raspberry-pi-wireless-access-point/) & [Captive Portal](https://pimylifeup.com/raspberry-pi-captive-portal/)

# Prepare apt

```
$ sudo apt update
$ sudo apt upgrade
```

# Hostapd & dnsmasq

## Install

```
$ sudo apt install hostapd dnsmasq
```

## Set up

### Stop them before overwriting their config files

```
$ sudo systemctl stop hostapd
$ sudo systemctl stop dnsmasq
```

### dhcpcd

[Use this config here](etc/dhcpcd.conf)

```
$ sudo nano /etc/dhcpcd.conf
```

### hostapd

[Use this config here](etc/hostapd/hostapd.conf)

```
$ sudo nano /etc/hostapd/hostapd.conf
```

[Use this config here](etc/default/hostapd)

```
$ sudo nano /etc/default/hostapd
```

[Use this config here](etc/init.d/hostapd)

```
$ sudo nano /etc/init.d/hostapd
```

### dnsmasq

[Use this config here](etc/dnsmasq.conf)

```
$ sudo nano /etc/dnsmasq.conf
```

### sysctl

[Use this config here](etc/sysctl.conf)

```
$ sudo nano /etc/sysctl.conf
```

### Iptables

Add them

```
$ sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

And save them on disk

```
$ sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

## Enable everything again

```
$ sudo systemctl restart dhcpcd
$ sudo systemctl unmask hostapd
$ sudo systemctl enable hostapd
$ sudo systemctl start hostapd
$ sudo service dnsmasq start
```

# Nodogsplash (captive portal)

## Install

```
$ sudo apt install git libmicrohttpd-dev
$ cd ~
$ git clone https://github.com/nodogsplash/nodogsplash.git
$ cd ~/nodogsplash
$ make
$ sudo make install
```

## Set up

[Use this config](etc/nodogsplash/nodogsplash.conf)

```
$ sudo nano /etc/nodogsplash/nodogsplash.conf
```

# Prepare everything to automatically start on boot

[Use this config](etc/rc.local)

```
$ sudo nano /etc/rc.local
```
