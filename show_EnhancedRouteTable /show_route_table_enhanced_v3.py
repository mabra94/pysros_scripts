#!/usr/bin/env python3

# show_route_table_enhanced.py
#   Copyright 2022 Nokia


"""
Enhancement of SROS embedded show router [Id] route-table command.
Tested on: SR OS 22.5.R1
"""

import sys
from datetime import timedelta
from pysros.management import connect
from pysros.pprint import Table


def get_connection(host=None, username=None, password=None, port=830):
    """
    Function definition to obtain a Connection object to a specific
    SR OS device and access the model-driven information.

    This function also checks whether the script is being executed
    locally on a pySROS capable SROS device or on a remote machine.

    :parameter host: The hostname or IP address of the SR OS node.
    :type host: str
    :paramater credentials: The username and password to connect
                            to the SR OS node.
    :type credentials: dict
    :parameter port: The TCP port for the connection to the SR OS node.
    :type port: int
    :returns: Connection object for the SR OS node.
    :rtype: :py:class:`pysros.management.Connection`
    """
    try:
        connection_object = connect(
            host=host,
            username=username,
            password=password,
            port=port,
        )
    except RuntimeError as error1:
        print("Failed to connect.  Error:", error1)
        sys.exit(-1)
    return connection_object


def print_route_table_v4(rows):
    """Function Definition to print the SROS style table."""

    # Define the columns that will be used in the table.  Each list item
    # is a tuple of (column width, heading).
    cols = [
        (25, "Dest Prefix"),
        (15, "Protocol"),
        (20, "Age"),
        (15, "Preference"),
        (80, "Next Hop"),
    ]

    # Initalize the Table object with the heading and columns.
    table = Table("Service Route Table", cols)

    # Print the output passing the data for the rows as
    # an argument to the function.
    table.print(rows)


def get_service_name(input_parameter, vprn_services):
    """Function definition to resolve the service name.

    The information collection is based on the service name.
    If the user provides the service ID as the input parameter
    instead, this function resolves the corresponsing
    service name.

    :parameter input_parameter: accessing provided input values
    :type input_parameter: dict
    :parameter vprn_services: Contains all VPRN services of a NE.
    :type vprn_services: dict
    :returns:   The service name of the service.
    :rtype: str
    """

    if input_parameter[1].isdigit():
        service_id = input_parameter[1]

        for service in vprn_services.keys():
            if int(vprn_services[service]["oper-service-id"].data) == int(
                service_id
            ):
                service_name = service

    else:
        service_name = input_parameter[1]
    return service_name


def get_local_itf_name(service_routes, route, interface_list):
    """Function definition to resolve local interface name.

    For local interfaces in the L3VPN/L3EVPN the respective
    interface name is resolved.

    :parameter service_routes: Contains all routes of a given L3 service
    :type service_routes: dict
    :parameter route: A specific route to be checked
    :type route: str
    :parameter interface_list: Contains all interfaces on a given L3 service
    :type interface_list: dict
    :returns:   The interface name.
    :rtype: str
    """

    if_index = service_routes[route]["nexthop"][0]["if-index"].data

    for interface in interface_list.keys():
        if interface_list[interface]["if-index"].data == if_index:
            next_hop_interface = interface

    next_hop = next_hop_interface + " (local interface)"
    return next_hop


def get_next_hop_tunnel(service_routes, route, lsp_list, tun_table):
    """Function definition to resolve tunnel names.

    For tunneled routes in the L3VPN/L3EVPN the respective
    tunnel name is resolved.

    :parameter service_routes: Contains all routes of a given L3 service
    :type service_routes: dict
    :parameter route: A specific route to be checked
    :type route: str
    :parameter lsp_list: Contains all LSPs of the NE
    :type lsp_list: dict
    :parameter tun_table: Contains all tunnels of the NE
    :type tun_table: dict
    :returns:   The tunnel name.
    :rtype: str
    """

    next_hop_path = service_routes[route]["nexthop"][0]["resolving-nexthop"][0]
    if "nexthop-tunnel-id" in next_hop_path.keys():
        tun_id = next_hop_path["nexthop-tunnel-id"].data
    # if "nexthop-tunnel-id" key does not exist,
    # tun_id is set to empty string to avoid errors
    else:
        tun_id = ""
    tun_type = next_hop_path["nexthop-tunnel-type"].data
    for tunnel in tun_table.keys():
        if tun_table[tunnel]["id"].data == tun_id:
            next_hop_ip = tunnel[0]
            next_hop_tun_proto = tun_table[tunnel]["protocol"].data
        else:
            next_hop_ip = next_hop_path["nexthop-ip"].data
            next_hop_tun_proto = tun_type
    for lsp in lsp_list.keys():
        if lsp_list[lsp]["ttm-tunnel-id"].data == tun_id:
            next_hop_lsp = " | lsp:" + lsp
            break
            # if an LSP with given Tunnel ID is found we break
            # the for loop
            # otherwise it would loop through all LSPs and the else
            # condition at the end would most likely be met
        # handling case in which Tunnel ID does not exist
        if tun_id == "":
            next_hop_lsp = ""
        # handling case in which LSP Name is not resolvable
        # in that case TTM Tunnel ID is displayed
        else:
            next_hop_lsp = " | ttmId:" + str(tun_id)
    next_hop = (
        next_hop_ip
        + " "
        + "(tunneled:"
        + next_hop_tun_proto
        + next_hop_lsp
        + ")"
    )
    return next_hop


def get_data():
    """
    Dedicated function to retrieve required data.

    :returns:   A tuple holding the required data.
    :rtype: tuple
    """

    # Calling the get_connection() function to establish
    # the connection to the NE.
    connection_object = get_connection()

    # List of VPRN services is needed to resolve service Id
    # to service name
    vprn_services = connection_object.running.get("/state/service/vprn")
    service_name = get_service_name(sys.argv, vprn_services)

    # All routes for a given service are retrieved
    path_service_routes = (
        "/state/service/vprn[service-name="
        + service_name
        + "]/route-table/unicast/ipv4/route"
    )
    service_routes = connection_object.running.get(path_service_routes)

    # All interfaces for a given are retrieved
    # Needed to resolve the interface name
    path_interface_list = (
        "/state/service/vprn[service-name=" + service_name + "]/interface"
    )
    interface_list = connection_object.running.get(path_interface_list)

    # Tunnel Table and LSP List are retrieved
    # Together they allow tunneled route resolution from TTM Id to tunnel name
    tun_table = connection_object.running.get(
        "/state/router[router-name=Base]/tunnel-table/ipv4/tunnel"
    )
    lsp_list = connection_object.running.get(
        "/state/router[router-name=Base]/mpls/lsp"
    )

    # Returning all needed data back to the main() function
    return service_routes, interface_list, tun_table, lsp_list


def main():
    """
    Main procedure to get all L3VPN/L3EVPN routes for a given service.

    It takes the input service ID or service name and collects required
    information from the SROS device to list all L3VPN/L3EVPN routes and
    resolve tunneled routes in an SROS style table
    """

    (
        service_routes,
        interface_list,
        tun_table,
        lsp_list,
    ) = get_data()

    svc_route_table_v4 = []

    for route in service_routes.keys():

        protocol = service_routes[route]["protocol"].data
        # converting Age into human readable format
        # consisting of "x day, hh:mm:ss"
        age = timedelta(seconds=service_routes[route]["age"].data)
        preference = service_routes[route]["preference"].data

        # This block does interface name resolution based
        # on if-index from route output
        if protocol == "local":
            next_hop = get_local_itf_name(
                service_routes, route, interface_list
            )
        # The function call below handles tunnel name resolution
        else:
            next_hop = get_next_hop_tunnel(
                service_routes, route, lsp_list, tun_table
            )

        svc_route_table_v4.append([route, protocol, age, preference, next_hop])

    print_route_table_v4(svc_route_table_v4)


if __name__ == "__main__":
    main()
