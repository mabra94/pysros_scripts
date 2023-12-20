## General Introduction

This script was written to allow resolution of hex strings provided by SROS for Optical Compliance of optical transceiver modules.
One version is written to be executable directly on an SROS device, the other version is supposed to run standalone.


## Elements and SW Versions tested with

| Element                | Version                                      |
|------------------------|----------------------------------------------|
|   Dev Workstation      |    CentOS Linux release 7.9.2009 (Core)      |
|   Dev Python Version   |    Python 3.6.8                              |
|   SROS Versions        |    22.5R1 to 23.7R2                          |

## Usage Description

This section shows some brief CLI examples of using this script.

#### Using the standalone version

The standalone version takes the optical compliance hex string as input parameter:


```shell
python OpticalComplianceResolution_v2.py 02:11:46:81:01:0d:46:21:55:0d:47:21:15:0d:48:21:05:41:48:41:11:41:49:41:01:11:c4:81:01:0d:c4:21:55:41:c4:41:11:05:c4:11:ff:0f:c4:41:11:0a:c4:11:ff:39:c4:41:11:53:c4:21:55:c0:c3:11:ff:00:00:00
Resolved Module Type
Optical Interfaces: SMF

Resolved Values for the Module Media Type:
['400GAUI-8 C2M (Annex 120E)', 'ZR400-OFEC-16QAM', 8, 1, '0b1']
['100GAUI-2 C2M (Annex 135G)', 'ZR400-OFEC-16QAM', 2, 1, '0b1010101']
['100GAUI-2 C2M (Annex 135G)', 'ZR300-OFEC-8QAM', 2, 1, '0b10101']
['100GAUI-2 C2M (Annex 135G)', 'ZR200-OFEC-QPSK', 2, 1, '0b101']
['CAUI-4 C2M (Annex 83E) without FEC', 'ZR200-OFEC-QPSK', 4, 1, '0b10001']
['CAUI-4 C2M (Annex 83E) without FEC', 'ZR100-OFEC-QPSK', 4, 1, '0b1']
['400GAUI-8 C2M (Annex 120E)', 'Vendor Specific/Custom', 8, 1, '0b1']
['100GAUI-2 C2M (Annex 135G)', 'Vendor Specific/Custom', 2, 1, '0b1010101']
['CAUI-4 C2M (Annex 83E) without FEC', 'Vendor Specific/Custom', 4, 1, '0b10001']
['25GAUI C2M (Annex 109B)', 'Vendor Specific/Custom', 1, 1, '0b11111111']
['200GAUI-4 C2M (Annex 120E)', 'Vendor Specific/Custom', 4, 1, '0b10001']
['50GAUI-1 C2M (Annex 135G)', 'Vendor Specific/Custom', 1, 1, '0b11111111']
['OTL4.4 (ITU-T G.709/Y.1331 G.Sup58) See CEI-28G-VSR', 'Vendor Specific/Custom', 4, 1, '0b10001']
['OTL4.2', 'Vendor Specific/Custom', 2, 1, '0b1010101']
['Vendor Specific/Custom', 'Vendor Specific/Custom', 1, 1, '0b11111111']
```

#### Using the pySROS version

The pySROS version can be executed either on or off-box. If executed from a remote machine you need to provide connection details how to connect to the SROS device. It takes the port ID as an input. 

#### Tested Hex Strings

QSFP-DD | ZR400-OFEC-16QAM ZR300-OFEC-8QAM ZR200-OFEC-QPSK ZR100-O*
02:11:46:81:01:0d:46:21:55:0d:47:21:15:0d:48:21:05:41:48:41:11:41:49:41:01:11:c4:81:01:0d:c4:21:55:41:c4:41:11:05:c4:11:ff:0f:c4:41:11:0a:c4:11:ff:39:c4:41:11:53:c4:21:55:c0:c3:11:ff:00:00:00

QSFP-DD | 400G FR4
02:11:1d:84:01:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00

QSFP-DD | 400G FR4 Undefined
02:50:1d:44:11:52:00:88:01:4f:1d:44:11:51:00:88:01:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00

QSFP-DD | 400GBASE-DR4 100GBASE-DR
02:11:1c:84:01:0d:14:21:55:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00

QSFP-DD | 100GBASE-DR 400GBASE-DR4 Undefined
02:4b:14:11:ff:4c:14:11:ff:4f:1c:44:11:50:1c:44:11:51:00:88:01:52:00:88:01:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00

QSFP-DD | 100G-LR 400GBASE-DR4 Undefined
02:4b:16:11:ff:4c:16:11:ff:4f:1c:44:11:50:1c:44:11:51:00:88:01:52:00:88:01:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00

QSFP-DD | 100G-FR 400GBASE-DR4 Undefined
02:4b:15:11:ff:4c:15:11:ff:4f:1c:44:11:50:1c:44:11:51:00:88:01:52:00:88:01:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00

QSFP-DD | 100G-LR 400GBASE-DR4 Undefined
02:4c:16:11:ff:50:1c:44:11:52:00:88:01:4b:16:11:ff:4f:1c:44:11:51:00:88:01:ff:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00