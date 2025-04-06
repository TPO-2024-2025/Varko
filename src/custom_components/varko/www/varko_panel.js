class VarkoPanel extends HTMLElement {
    connectedCallback() {
        this.hass = document.querySelector("home-assistant")?.hass;
        if (!this.hass) return;

        this.innerHTML = `
            <div style="padding: 20px;">
                <h1>Varko</h1>

                <form id="addDeviceForm">
                    <h2>Add device</h2>
                    <label for="selectDeviceType">Select device type:</label>
                    <select name="device_type" id="selectDeviceType">
                        <option value="light">light</option>
                    </select>
                    <label for="addDeviceName">Device name:</label>
                    <input type="text" name="device_name" id="addDeviceName">
                    <label for="addDeviceId">Device Id:</label>
                    <input type="text" name="device_id" id="addDeviceId">
                    <button type="submit">Add</button>
                </form>

                <form id="removeDeviceForm">
                    <h2>Remove device</h2>
                    <label for="selectRemoveDevice">Select device:</label>
                    <select name="device_id" id="selectRemoveDevice" class="entitySelect"></select>
                    <button type="submit">Remove</button>
                </form>

                <form id="activateIntruderForm">
                    <h2>Activate intruder detection</h2>
                    <label for="intruderDetectionDuration">Duration:</label>
                    <input type="number" name="timeout" id="intruderDetectionDuration" value="0" min="0">
                    <button type="submit">Activate</button>
                </form>

                <form id="activatePresenceForm">
                    <h2>Activate presence simulation</h2>
                    <label for="presenceSimulationDuration">Duration:</label>
                    <input type="number" name="timeout" id="presenceSimulationDuration" value="0" min="0">
                    <button type="submit">Activate</button>
                </form>

                <form id="deactivateIntruderForm">
                    <h2>Deactivate intruder detection</h2>
                    <button type="submit">Deactivate</button>
                </form>

                <form id="deactivatePresenceForm">
                    <h2>Deactivate presence simulation</h2>
                    <button type="submit">Deactivate</button>
                </form>

                <form id="addZoneForm">
                    <h2>Add activation zone</h2>
                    <label for="addActivationZone">Select zone:</label>
                    <select name="zone_id" id="addActivationZone" class="selectZone"></select>
                    <button type="submit">Add</button>
                </form>

                <form id="removeZoneForm">
                    <h2>Remove activation zone</h2>
                    <label for="removeActivationZone">Select zone:</label>
                    <select name="zone_id" id="removeActivationZone" class="selectZone"></select>
                    <button type="submit">Remove</button>
                </form>

                <form id="enableDeviceForm">
                    <h2>Enable device</h2>
                    <label for="enableDevice">Select device:</label>
                    <select name="device_id" id="enableDevice" class="entitySelect"></select>
                    <button type="submit">Enable</button>
                </form>

                <form id="disableDeviceForm">
                    <h2>Disable device</h2>
                    <label for="disableDevice">Select device:</label>
                    <select name="device_id" id="disableDevice" class="entitySelect"></select>
                    <button type="submit">Disable</button>
                </form>
            </div>
        `;

        this._loadEntities();
        this._loadZones();

        // Register form event listeners
        this._addFormListener("addDeviceForm", "varko.add_device");
        this._addFormListener("removeDeviceForm", "varko.remove_device");
        this._addFormListener("activateIntruderForm", "varko.activate_intruder_detection");
        this._addFormListener("activatePresenceForm", "varko.activate_presence_simulation");
        this._addFormListener("deactivateIntruderForm", "varko.deactivate_intruder_detection");
        this._addFormListener("deactivatePresenceForm", "varko.deactivate_presence_simulation");
        this._addFormListener("addZoneForm", "varko.add_activation_zone");
        this._addFormListener("removeZoneForm", "varko.remove_activation_zone");
        this._addFormListener("enableDeviceForm", "varko.enable_device");
        this._addFormListener("disableDeviceForm", "varko.disable_device");
    }

    _addFormListener(formId, service) {
        this.querySelector(`#${formId}`)?.addEventListener("submit", (event) => {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            this._callService(service, data);
        });
    }

    _loadEntities() {
        const selects = this.querySelectorAll("select.entitySelect");
        const entities = Object.values(this.hass.entities);

        for (const entity of entities) {
            const option = document.createElement("option");
            option.value = entity.entity_id;
            option.textContent = entity.name;
            selects.forEach(select => select.appendChild(option.cloneNode(true)));
        }
    }

    _loadZones() {
        const selects = this.querySelectorAll("select.selectZone");
        const zones = Object.values(this.hass.states).filter(e => e.entity_id.startsWith("zone."));

        for (const zone of zones) {
            const option = document.createElement("option");
            option.value = zone.entity_id;
            option.textContent = zone.attributes.friendly_name;
            selects.forEach(select => select.appendChild(option.cloneNode(true)));
        }
    }

    _callService(service, data = {}) {
        const [domain, serviceName] = service.split(".");
        this.hass.callService(domain, serviceName, data);
    }
}

customElements.define("varko-panel", VarkoPanel);
