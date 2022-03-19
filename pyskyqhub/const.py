"""Constants."""
import re

CONNECTION_ERROR = "connectionerror"
DATA_ERROR = "dataerror"
MAC_REGEX = re.compile(r"(([0-9A-Fa-f]{1,2}\:){5}[0-9A-Fa-f]{1,2})")


TEST_RESPONSE = "attach_dev = 'UNKNOWN,68:ff:7b:cc:a9:5c,Cabled<lf>UNKNOWN,70:4f:57:99:a3:f0,Cabled<lf>TC-Private,e4:95:6e:44:cd:7d,Cabled<lf>SKY+HD,20:47:ed:c5:9a:72,UnKnown<lf>09AA01AC101702WV,18:b4:30:bf:4d:e6,Wireless'; "
