"""Constants."""
import re

CONNECTION_ERROR = "connectionerror"
DATA_ERROR = "dataerror"
MAC_REGEX = re.compile(r"(([0-9A-Fa-f]{1,2}\:){5}[0-9A-Fa-f]{1,2})")


TEST_RESPONSE = (
    "var wanDslLinkConfig = '1_ipoe_0_1_0.101_94.12.54.111_24:a7:dc:4c:7e:a2_255.255.252.0_94.12.52.1_ptm0';\n"
    "var sky_WirelessAllSSIDs = 'SKYA6FD4'; \n"
    "var i, j, k, attach_dev = '"
    "UNKNOWN,68:ff:7b:cc:a9:5c,Wireless<lf>"
    "Test-Name2,70:4f:57:99:a3:f0,Cabled<lf>"
    # "Test-Name3,72:4f:57:99:a3:f0,Unknown<lf>"
    "TC-Private,e4:95:6e:44:cd:7d,Cabled<lf>"
    "SKY+HD,20:47:ed:c5:9a:72,Wireless<lf>"
    # "SKY+HD,20:47:ed:c5:9a:72,UnKnown<lf>"
    "09AA01AC101702WV,18:b4:30:bf:4d:e6,Wireless"
    "'; "
    "more stuff"
)
