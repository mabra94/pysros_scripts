## General Introduction

This script was written to allow simple SROS route-table tunnel resolution to a name instead of an internal tunnel table id. Using default SROS show commands we would need to execute at least 2 commands to get the name of the tunnel being used to reach a tunneled destination prefix. Using this custom script a single command is sufficient as the script handles the lookup.

## Elements and SW Versions tested with

| Element                | Version                                      |
|------------------------|----------------------------------------------|
|   Dev Workstation      |    CentOS Linux release 7.9.2009 (Core)      |
|   Dev Python Version   |    Python 3.6.8                              |
|   SROS Versions        |    22.5R1 to 23.7R2                          |

## Usage Description

This section shows some brief CLI examples of using this script.

#### Built-in SR OS L3VPN route-table view

The following CLI output shows the built-in SR OS L3VPN route-table view, including a tunneled route:

```shell
A:admin@sros1# show router 320 route-table

===============================================================================
Route Table (Service: 320)
===============================================================================
Dest Prefix[Flags]                            Type    Proto     Age        Pref
      Next Hop[Interface Name]                                    Metric
-------------------------------------------------------------------------------
20.0.0.1/32                                   Local   Local     05d19h04m  0
       sros1-vpn320                                                 0
20.0.0.2/32                                   Remote  EVPN-IFL  03d12h49m  170
       200.0.0.2 (tunneled:SR-TE:655365)                            10
-------------------------------------------------------------------------------
No. of Routes: 2
Flags: n = Number of times nexthop is repeated
       B = BGP backup route available
       L = LFA nexthop available
       S = Sticky ECMP requested
===============================================================================
```

#### Enhanced L3VPN route-table view

The following output shows the enhanced pySROS script-based L3VPN route-table view, demonstrating that the script expects either the service-id or the service-name as an input variable. It works in both cases:

```shell
######
# Using service-id as input variable
######

[/]
A:admin@sros1# pyexec cf3:/show_RouteTable_enhanced.py 320
===============================================================================
Service Route Table
===============================================================================
Dest Prefix               Protocol        Age                  Preference
Next Hop
-------------------------------------------------------------------------------
20.0.0.1/32               local           68 days, 18:54:53    0
sros1-vpn320 (local interface)
20.0.0.2/32               evpn-ifl        0:39:28              170
200.0.0.2 (tunneled:sr-te | lsp:l_sros2-srte_pcc)
===============================================================================

[/]

######
# Using service-name as input variable
######

[/]
A:admin@sros1# pyexec cf3:/show_RouteTable_enhanced.py L3-EVPN-Test
===============================================================================
Service Route Table
===============================================================================
Dest Prefix               Protocol        Age                  Preference
Next Hop
-------------------------------------------------------------------------------
20.0.0.1/32               local           68 days, 19:23:52    0
sros1-vpn320 (local interface)
20.0.0.2/32               evpn-ifl        0:07:10              170
200.0.0.2 (tunneled:sr-te | lsp:l_sros2-srte_pcc)
===============================================================================

[/]
```

## Tested Scenarios

This script has been tested for the following types of tunneled L3VPN routes:
- LSP
- SR-ISIS
- SR-TE
- RSVP-TE