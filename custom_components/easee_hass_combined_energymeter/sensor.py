from homeassistant.helpers.entity import Entity
from homeassistant.const import ENERGY_KILO_WATT_HOUR
from .const import DOMAIN

#import logging
#from datetime import timedelta
#from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Combined Energy Meter sensor."""
    name = config_entry.data["name"]
    total_consumption_entity = config_entry.data["total_consumption_entity"]
    session_consumption_entity = config_entry.data["session_consumption_entity"]

    async_add_entities([CombinedEnergyMeter(hass, name, total_consumption_entity, session_consumption_entity)], True)

class CombinedEnergyMeter(Entity):
    def __init__(self, hass, name, total_consumption_entity, session_consumption_entity):
        self.hass = hass
        self._name = name
        self._total_consumption_entity = total_consumption_entity
        self._session_consumption_entity = session_consumption_entity
        self._state = None
        self._last_total = None
        self._last_session = None
        self._modified_session = 0

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return ENERGY_KILO_WATT_HOUR

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        async def total_consumption_changed(entity_id, old_state, new_state):
            if new_state is None:
                return
            new_total = float(new_state.state)
            if self._last_total is not None:
                self._modified_session = 0
            self._last_total = new_total
            await self.async_update_ha_state()

        async def session_consumption_changed(entity_id, old_state, new_state):
            if new_state is None:
                return
            new_session = float(new_state.state)
            if self._last_session is not None:
                self._modified_session += new_session - self._last_session
            self._last_session = new_session
            await self.async_update_ha_state()

        self.hass.helpers.event.async_track_state_change(
            self._total_consumption_entity, total_consumption_changed
        )
        self.hass.helpers.event.async_track_state_change(
            self._session_consumption_entity, session_consumption_changed
        )

    async def async_update(self):
        total_state = self.hass.states.get(self._total_consumption_entity)
        session_state = self.hass.states.get(self._session_consumption_entity)

        if total_state is None or session_state is None:
            self._state = None
            return

        total = float(total_state.state)
        session = float(session_state.state)

        if self._last_total is None:
            self._last_total = total
        if self._last_session is None:
            self._last_session = session

        self._state = max(total, self._last_total + self._modified_session)

