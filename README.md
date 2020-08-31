[![CodeFactor](https://www.codefactor.io/repository/github/rogerselwyn/skyq_hub/badge)](https://www.codefactor.io/repository/github/rogerselwyn/skyq_hub)

[![maintained](https://img.shields.io/maintenance/yes/2020.svg)](#)
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
   {'mac': '68:xx:7b:cc:xx:5c', 'name': 'UNKNOWN'},
   {'mac': '70:xx:57:a3:xx:f0', 'name': 'UNKNOWN'},
   {'mac': 'e4:xx:6e:44:xx:7d', 'name': 'Private'},
   {'mac': '20:xx:ed:c5:xx:72', 'name': 'SKY+HD'},
   {'mac': '18:xx:30:bf:xx:e6', 'name': '09AA0xxxxxx02WV'},
   ...
]
```
