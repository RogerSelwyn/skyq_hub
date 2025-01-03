[![CodeFactor](https://www.codefactor.io/repository/github/rogerselwyn/skyq_hub/badge)](https://www.codefactor.io/repository/github/rogerselwyn/skyq_hub)

![GitHub release](https://img.shields.io/github/v/release/RogerSelwyn/skyq_hub) [![maintained](https://img.shields.io/maintenance/yes/2025.svg)](#)
[![maintainer](https://img.shields.io/badge/maintainer-%20%40RogerSelwyn-blue.svg)](https://github.com/RogerSelwyn)

# pyskyqhub
Python module for accessing Sky Q hub and retrieving connected devices

## Introduction

This library enables access to SkyQ hub to pull back a list of devices connected to the hub, and their names/

## Installing

To install:

```
pip install pyskyqhub
```

## Usage

### Base
```
from pyskyqremote import SkyQhub

hub = SkyQHub('192.168.1.254')
await hub.async_connect()
```
hub.success_init will indicate for connection was succesful or not

### Get connected devices

```
devices = await skyhub.async_get_skyhub_data()
```

Will return an object such as below:

```
[
   {'mac': '68:xx:7b:cc:xx:5c', 'name': 'UNKNOWN', 'connection': 'Wireless'},
   {'mac': '70:xx:57:a3:xx:f0', 'name': 'UNKNOWN', 'connection': 'Cabled'},
   {'mac': 'e4:xx:6e:44:xx:7d', 'name': 'Laptop', 'connection': 'Wireless'},
   {'mac': '20:xx:ed:c5:xx:72', 'name': 'SKY+HD', 'connection': 'UnKnown'},
   {'mac': '18:xx:30:bf:xx:e6', 'name': '09AA0xxxxxx02WV', 'connection': 'Wireless'},
   ...
]
```

### Properties

The following properties are provided from the component:
* available - Whether the router was accessible and providing valid data.
* ssid - The Wifi SSID provided by the router.
* wan_ip - The external IP address of the router.
* wan_mac - The external mac of the router.
