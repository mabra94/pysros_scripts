#!/usr/bin/env python3

"""
Resolution of optical compliance hex string
provided by SROS according to optical
standards documents.
"""

import sys
from pysros.management import connect

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


def main():
    """
    It takes the input port Id, fetches the corresponding optical compliance
    hex string from the system and resolves it according to optical
    compliance mapping tables
    """

    connection_object = get_connection()

    port_id = sys.argv[1]

    hex_string = connection_object.running.get(
        "/state/port[port-id='" + port_id + "']/transceiver/optical-compliance"
        )


    # Data mapping
    # Module Type Mapping based on Table 8-12 in
    # QSFP-DD-CMIS-rev4p0.pdf
    module_type_mapping = {
        0x00: "Unknown",
        0x01: "Optical Interfaces: MMF",
        0x02: "Optical Interfaces: SMF",
        0x03: "Passive Cu",
        0x04: "Active Cable",
        0x05: "BASE-T"
    }

    host_electrical_mapping = {
        0x00: "Undefined",
        0x01: "1000BASE-CX (Clause 39)",
        0x02: "XAUI (Clause 47)",
        0x03: "XFI (SFF INF-8071i)",
        0x04: "SFI (SFF-8431)",
        0x05: "25GAUI C2M (Annex 109B)",
        0x06: "XLAUI C2M (Annex 83B)",
        0x07: "XLPPI (Annex 86A)",
        0x08: "LAUI-2 C2M (Annex 135C)",
        0x09: "50GAUI-2 C2M (Annex 135E)",
        0x0A: "50GAUI-1 C2M (Annex 135G)",
        0x0B: "CAUI-4 C2M (Annex 83E)1",
        0x41: "CAUI-4 C2M (Annex 83E) without FEC",
        0x42: "CAUI-4 C2M (Annex 83E) with RS(528,514) FEC",
        0x0C: "100GAUI-4 C2M (Annex 135E)",
        0x0D: "100GAUI-2 C2M (Annex 135G)",
        0x4B: "100GAUI-1-S C2M (Annex 120G)",
        0x4C: "100GAUI-1-L C2M (Annex 120G)",
        0x0E: "200GAUI-8 C2M (Annex 120C)",
        0x0F: "200GAUI-4 C2M (Annex 120E)",
        0x4D: "200GAUI-2-S C2M (Annex 120G)",
        0x4E: "200GAUI-2-L C2M (Annex 120G)",
        0x10: "400GAUI-16 C2M (Annex 120C)",
        0x11: "400GAUI-8 C2M (Annex 120E)",
        0x4F: "400GAUI-4-S C2M (Annex 120G)",
        0x50: "400GAUI-4-L C2M (Annex 120G)",
        0x51: "800G S C2M (placeholder)",
        0x52: "800G L C2M (placeholder)",
        0x12: "Reserved",
        0x13: "10GBASE-CX4 (Clause 54)",
        0x14: "25GBASE-CR CA-25G-L (Clause 110)",
        0x15: "25GBASE-CR or 25GBASE-CR-S CA-25G-S (Clause 110)",
        0x16: "25GBASE-CR or 25GBASE-CR-S CA-25G-N (Clause 110)",
        0x17: "40GBASE-CR4 (Clause 85)",
        0x43: "50GBASE-CR2 (Ethernet Technology Consortium) with RS(528,514) (Clause 91) FEC",
        0x44: "50GBASE-CR2 (Ethernet Technology Consortium) with BASE-R (Clause 74), Fire code FEC",
        0x45: "50GBASE-CR2 (Ethernet Technology Consortium) with no FEC",
        0x18: "50GBASE-CR (Clause 136)",
        0x19: "100GBASE-CR10 (Clause 85)",
        0x1A: "100GBASE-CR4 (Clause 92)",
        0x1B: "100GBASE-CR2 (Clause 136)",
        0x46: "100GBASE-CR1 (Clause 162)",
        0x1C: "200GBASE-CR4 (Clause 136)",
        0x47: "200GBASE-CR2 (Clause 162)",
        0x1D: "400G CR8 (Ethernet Technology Consortium)",
        0x48: "400GBASE-CR4 (Clause 162)",
        0x49: "800G-ETC-CR8",
        0x25: "8GFC (FC-PI-4)",
        0x26: "10GFC (10GFC)",
        0x27: "16GFC (FC-PI-5)",
        0x28: "32GFC (FC-PI-6)",
        0x29: "64GFC (FC-PI-7)",
        0x4A: "128GFC (FC-PI-8)",
        0x2A: "128GFC (FC-PI-6P)",
        0x2B: "256GFC (FC-PI-7P)",
        0x2C: "IB SDR (Arch.Spec.Vol.2)",
        0x2D: "IB DDR (Arch.Spec.Vol.2)",
        0x2E: "IB QDR (Arch.Spec.Vol.2)",
        0x2F: "IB FDR (Arch.Spec.Vol.2)",
        0x30: "IB EDR (Arch.Spec.Vol.2)",
        0x31: "IB HDR (Arch.Spec.Vol.2)",
        0x32: "IB NDR",
        0x33: "E.96 (CPRI Specification V7.0)",
        0x34: "E.99 (CPRI Specification V7.0)",
        0x35: "E.119 (CPRI Specification V7.0)",
        0x36: "E.238 (CPRI Specification V7.0)",
        0x37: "OTL3.4 (ITU-T G.709/Y.1331 G.Sup58) See XLAUI (overclocked)",
        0x38: "OTL4.10 (ITU-T G.709/Y.1331 G.Sup58) See CAUI-10 (overclocked)",
        0x53: "OTL4.2",
        0x39: "OTL4.4 (ITU-T G.709/Y.1331 G.Sup58) See CEI-28G-VSR",
        0x3A: "OTLC.4 (ITU-T G.709.1/Y.1331 G.Sup58) See CEI-28G-VSR",
        0x3B: "FOIC1.4 (ITU-T G.709.1/Y.1331 G.Sup58) See CEI-28G-VSR",
        0x3C: "FOIC1.2 (ITU-T G.709.1/Y.1331 G.Sup58) See CEI-56G-VSR-PAM4",
        0x3D: "FOIC2.8 (ITU-T G.709.1/Y.1331 G.Sup58) See CEI-28G-VSR",
        0x3E: "FOIC2.4 (ITU-T G.709.1/Y.1331 G.Sup58) See CEI-56G-VSR-PAM4",
        0x3F: "FOIC4.16 (ITU-T G.709.1 G.Sup58) See CEI-28G-VSR",
        0x40: "FOIC4.8 (ITU-T G.709.1 G.Sup58) See CEI-56G-VSR-PAM4",
        0xC0: "Vendor Specific/Custom",
        0xFF: "End of list"
    }

    # Second byte data mapping
    smf_module_media_mapping = {
        0x01: "10GBASE-LW (Clause 52)",
        0x02: "10GBASE-EW (Clause 52)",
        0x03: "10G-ZW",
        0x04: "10GBASE-LR (Clause 52)",
        0x05: "10GBASE-ER (Clause 52)",
        0x4E: "10GBASE-BR (Clause 158)1",
        0x06: "10G-ZR",
        0x07: "25GBASE-LR (Clause 114)",
        0x08: "25GBASE-ER (Clause 114)",
        0x4F: "25GBASE-BR (Clause 159)1",
        0x09: "40GBASE-LR4 (Clause 87)",
        0x0A: "40GBASE-FR (Clause 89)",
        0x0B: "50GBASE-FR (Clause 139)",
        0x0C: "50GBASE-LR (Clause 139)",
        0x40: "50GBASE-ER (Clause 139)",
        0x50: "50GBASE-BR (Clause 160)1",
        0x0D: "100GBASE-LR4 (Clause 88)",
        0x0E: "100GBASE-ER4 (Clause 88)",
        0x0F: "100G PSM4 MSA Spec",
        0x34: "100G CWDM4-OCP",
        0x10: "100G CWDM4 MSA Spec",
        0x11: "100G 4WDM-10 MSA Spec",
        0x12: "100G 4WDM-20 MSA Spec",
        0x13: "100G 4WDM-40 MSA Spec",
        0x14: "100GBASE-DR (Clause 140)",
        0x15: "100G-FR MSA spec2/100GBASE-FR1 (Clause 140)",
        0x16: "100G-LR MSA spec2/100GBASE-LR1 (Clause 140)",
        0x4A: "100G-LR1-20 MSA Spec2",
        0x4B: "100G-ER1-30 MSA Spec2",
        0x4C: "100G-ER1-40 MSA Spec2",
        0x44: "100GBASE-ZR (Clause 154)",
        0x17: "200GBASE-DR4 (Clause 121)",
        0x18: "200GBASE-FR4 (Clause 122)",
        0x19: "200GBASE-LR4 (Clause 122)",
        0x41: "200GBASE-ER4 (Clause 122)",
        0x1A: "400GBASE-FR8 (Clause 122)",
        0x1B: "400GBASE-LR8 (Clause 122)",
        0x42: "400GBASE-ER8 (Clause 122)",
        0x1C: "400GBASE-DR4 (Clause 124)",
        0x55: "400GBASE-DR4-2 (placeholder)",
        0x1D: "400G-FR4 MSA spec2/400GBASE-FR4 (Clause 151)",
        0x43: "400GBASE-LR4-6 (Clause 151)",
        0x1E: "400G-LR4-10 MSA Spec2",
        0x4D: "400GBASE-ZR (Clause 156)",
        0x56: "800GBASE-DR8 (placeholder)",
        0x57: "800GBASE-DR8-2 (placeholder)",
        0x1F: "8GFC-SM (FC-PI-4)",
        0x20: "10GFC-SM (10GFC)",
        0x21: "16GFC-SM (FC-PI-5)",
        0x22: "32GFC-SM (FC-PI-6)",
        0x23: "64GFC-SM (FC-PI-7)",
        0x45: "128GFC-SM (FC-PI-8)",
        0x24: "128GFC-PSM4 (FC-PI-6P)",
        0x26: "128GFC-CWDM4 (FC-PI-6P)",
        0x2C: "4I1-9D1F (G.959.1)",
        0x2D: "4L1-9C1F (G.959.1)",
        0x2E: "4L1-9D1F (G.959.1)",
        0x2F: "C4S1-9D1F (G.695)",
        0x30: "C4S1-4D1F (G.695)",
        0x31: "4I1-4D1F (G.959.1)",
        0x32: "8R1-4D1F (G.959.1)",
        0x33: "8I1-4D1F (G.959.1)",
        0x51: "FOIC1.4-DO (G.709.3/Y.1331.3)3",
        0x52: "FOIC2.8-DO (G.709.3/Y.1331.3)3",
        0x53: "FOIC4.8-DO (G.709.3/Y.1331.3)3",
        0x54: "FOIC2.4-DO (G.709.3/Y.1331.3)3",
        0x38: "10G-SR",
        0x39: "10G-LR",
        0x3A: "25G-SR",
        0x3B: "25G-LR",
        0x3C: "10G-LR-BiDi",
        0x3D: "25G-LR-BiDi",
        0x3E: "400ZR, DWDM, amplified",
        0x3F: "400ZR, Single Wavelength, Unamplified",
        0x46: "ZR400-OFEC-16QAM",
        0x47: "ZR300-OFEC-8QAM",
        0x48: "ZR200-OFEC-QPSK",
        0x49: "ZR100-OFEC-QPSK"
    }

    mmf_module_media_mapping = {
        0x00: "Undefined",
        0x01: "10GBASE-SW (Clause 52)",
        0x02: "10GBASE-SR (Clause 52)",
        0x03: "25GBASE-SR (Clause 112)",
        0x04: "40GBASE-SR4 (Clause 86)",
        0x05: "40GE SWDM4 MSA Spec",
        0x06: "40GE BiDi",
        0x07: "50GBASE-SR (Clause 138)",
        0x08: "100GBASE-SR10 (Clause 86)",
        0x09: "100GBASE-SR4 (Clause 95)",
        0x0A: "100GE SWDM4 MSA Spec",
        0x0B: "100GE BiDi",
        0x0C: "100GBASE-SR2 (Clause 138)",
        0x0D: "100GBASE-SR1 (Clause 167)",
        0x1D: "100GBASE-VR1 (Clause 167)",
        0x0E: "200GBASE-SR4 (Clause 138)",
        0x1B: "200GBASE-SR2 (Clause 167)",
        0x1E: "200GBASE-VR2 (Clause 167)",
        0x0F: "400GBASE-SR16 (Clause 123)",
        0x10: "400GBASE-SR8 (Clause 138)",
        0x11: "400GBASE-SR4 (Clause 167)",
        0x1F: "400GBASE-VR4 (Clause 167)",
        0x12: "800GBASE-SR8 (Placeholder)",
        0x20: "800GBASE-VR8 (Placeholder)",
        0x1A: "400GBASE-SR4.2 (Clause 150)",
        0x13: "8GFC-MM (FC-PI-4)",
        0x14: "10GFC-MM (10GFC)",
        0x15: "16GFC-MM (FC-PI-5)",
        0x16: "32GFC-MM (FC-PI-6)",
        0x17: "64GFC-MM (FC-PI-7)",
        0x1C: "128GFC-MM (FC-PI-8)",
        0x18: "128GFC-MM4 (FC-PI-6P)",
        0x19: "256GFC-MM4 (FC-PI-7P)"
    }

    # Remove ':' and split the hex string into substrings of 4 bytes each
    hex_bytes = hex_string.replace(":", "")

    # Extracting the first 2 bytes to identify the module type
    mod_type = int(hex_bytes[0:2], 16)

    # Grouping the remaining bytes into chunks of 4 byte each
    substrings = [hex_bytes[i:i+8] for i in range(2, len(hex_bytes), 8)]
    print(substrings)

    # Use a set to store unique resolved values for the first byte
    resolved_module_type = ""

    if mod_type in module_type_mapping:
        resolved_module_type = module_type_mapping[mod_type]
    elif mod_type in range(0x06, 0x90):
        resolved_module_type = "Custom"
    elif mod_type in range(0x90, 0x100):
        resolved_module_type = "Reserved"
    else:
        resolved_module_type = "Could not resolve Module Type"

    # Use a set to store unique resolved values for the second byte
    selected_module_media_mapping = {}
    smf_bool = False
    if "SMF" in resolved_module_type:
        selected_module_media_mapping = smf_module_media_mapping
        smf_bool = True
    elif "MMF" in resolved_module_type:
        selected_module_media_mapping = mmf_module_media_mapping
    else:
        print("Could not find a data mapping to resolve the Module Media Type")

    resolved_data_set = []

    # Extract and resolve the second byte
    for substring in substrings:

        if len(substring) % 8 != 0:
            break

        resolved_bytes = []

        first_byte = int(substring[0:2], 16)
        second_byte = int(substring[2:4], 16)
        third_half_byte_a = int(substring[4:5], 16)
        third_half_byte_b = int(substring[5:6], 16)
        fourth_byte = int(substring[6:8], 16)

        if first_byte in host_electrical_mapping:
            resolved_bytes.append(host_electrical_mapping[first_byte])
        else:
            resolved_bytes.append("Unknown Host Electrial Byte")

        if second_byte in selected_module_media_mapping:
            resolved_bytes.append(selected_module_media_mapping[second_byte])
        elif smf_bool is True and second_byte in range(0x35, 0x37):
            resolved_bytes.append("Reserved")
        elif smf_bool is True and second_byte in range(0x58, 0xBF):
            resolved_bytes.append("Reserved")
        elif smf_bool is True and second_byte in range(0xC0, 0xFF):
            resolved_bytes.append("Vendor Specific/Custom")
        elif smf_bool is False and second_byte in range(0x21, 0xBF):
            resolved_bytes.append("Reserved")
        elif smf_bool is False and second_byte in range(0xC0, 0xFF):
            resolved_bytes.append("Vendor Specific/Custom")
        else:
            resolved_bytes.append("Unknown Module Media Byte")

        if 0 <= third_half_byte_a <= 8:
            resolved_bytes.append(third_half_byte_a)
        else:
            resolved_bytes.append("Invalid Host Lane Count")

        if 0 <= third_half_byte_b <= 8:
            resolved_bytes.append(third_half_byte_b)
        else:
            resolved_bytes.append("Invalid Media Lane Count")

        resolved_bytes.append(bin(fourth_byte))

        resolved_data_set.append(resolved_bytes)

    # Print the unique resolved values for the first byte
    print("Resolved Module Type")
    print(resolved_module_type)

    # Print the unique resolved values for the second byte
    print("\nResolved Values for the Module Media Type:")
    for value in resolved_data_set:
        print(value)

if __name__ == "__main__":
    main()
