import yaml
import sys
import os
from pysros.management import connect
from pathlib import Path

def get_connection(host=None, username=None, password=None, port=830, hostkey_verify=False):
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
            hostkey_verify=hostkey_verify
        )
    except RuntimeError as error1:
        print("Failed to connect.  Error:", error1)
        sys.exit(-1)
    return connection_object

def getConfig(connection_object, path):
    """
    Dedicated function to retrieve required config.

    :parameter connection_object: The connection object
    :type connection_object: dict
    :paramater path: xpath pointing towards desired config
    :type path: str

    :returns:   A tuple holding the required data.
    :rtype: tuple
    """

    config = connection_object.running.get(path)

    return config

def ConfigToJson(connection_object, path, config):
    """
    Dedicated function to convert config to json.

    :parameter connection_object: The connection object
    :type connection_object: dict
    :paramater config: config retrieved from node
    :type config: dict

    :returns:   
    :rtype: 
    """

    jsonConfig = connection_object.convert(path=path, payload=config, source_format="pysros", destination_format="json", pretty_print=True)

    return jsonConfig

def loadInventory(inventoryFile):
    f = open(inventoryFile)
    inv = yaml.safe_load(f)

    return inv

def main():
    """

    """
    path = '/nokia-conf:configure'

    inventory = loadInventory('inventory.yaml')

    NeUsername = os.getenv('NEUSERNAME')
    NePassword = os.getenv('NEPASSWORD')

    for entry in inventory['hosts']:

        filepath = Path(entry+'/config.json')
      
        print("Establishing Connection to "+ entry +"\n")
        connection_object = get_connection(host=entry, username=NeUsername, password=NePassword)

        print("Fetching config from "+ entry +"\n")
        actualConfig = getConfig(connection_object, path)
        actualJsonConfig = ConfigToJson(connection_object, path, actualConfig)

        if filepath.is_file():
            print("File exist")
            with filepath.open("r", encoding ="utf-8") as f:
                storedConfig = f.read()
                f.close()

                if storedConfig == actualJsonConfig:
                    print("Existing stored config is identical to the running config on the nodes")
                else:
                    with filepath.open("w", encoding ="utf-8") as f:
                        f.write(actualJsonConfig)
                        f.close()
        else:
            print("File not exist")
            with filepath.open("w", encoding ="utf-8") as f:
                f.write(actualJsonConfig)
                f.close()


if __name__ == "__main__":
    main()
