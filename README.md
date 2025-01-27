# easee_hass_combined_energymeter



## Installation

There are 2 different methods of installing the custom component

### HACS installation

1. Add this repository from HACS->Integrations.
2. Restart Home Assistant.
3. Install the component from Settings->Integrations. You may have to clear the browser cache to make the Easee integration appear in the list.

### Git installation

1. Make sure you have git installed on your machine.
2. Navigate to you home assistant configuration folder. maybe cd /homeassistant or cd /config
3. Create a `custom_components` folder of it does not exist, navigate down into it after creation.
4. Execute the following command: `git clone https://github.com/rolfsrolfs/easee_hass_combined_energymeter easee_hass_combined_energymeter`
5. Run `bash links.sh`


## Configuration

Add the following to your configuration.yaml - make sure that the sensors you add are correct

sensor:
  - platform: easee_hass_combined_energy_meter
    total_consumption_entity: sensor.mineasee_home_levetidsforbruk
    session_consumption_entity: sensor.mineasee_home_energi_ladesesjon

