const countries  = [
    { name: "Austria", code: "AT" },
    { name: "Belgium", code: "BE" },
    { name: "Bulgaria", code: "BG" },
    { name: "Croatia", code: "HR" },
    { name: "Cyprus", code: "CY" },
    { name: "Czech Republic", code: "CZ" },
    { name: "Denmark", code: "DK" },
    { name: "Estonia", code: "EE" },
    { name: "Finland", code: "FI" },
    { name: "France", code: "FR" },
    { name: "Germany", code: "DE" },
    { name: "Greece", code: "GR" },
    { name: "Hungary", code: "HU" },
    { name: "Iceland", code: "IS" },
    { name: "Ireland", code: "IE" },
    { name: "Italy", code: "IT" },
    { name: "Latvia", code: "LV" },
    { name: "Lithuania", code: "LT" },
    { name: "Luxembourg", code: "LU" },
    { name: "Malta", code: "MT" },
    { name: "Netherlands", code: "NL" },
    { name: "Norway", code: "NO" },
    { name: "Poland", code: "PL" },
    { name: "Portugal", code: "PT" },
    { name: "Romania", code: "RO" },
    { name: "Slovakia", code: "SK" },
    { name: "Slovenia", code: "SI" },
    { name: "Spain", code: "ES" },
    { name: "Sweden", code: "SE" },
    { name: "Switzerland", code: "CH" },
    { name: "United Kingdom", code: "GB" },
    { name: "United States", code: "US" },
]

class VarkoPanel extends HTMLElement {
    connectedCallback() {
        this.attachShadow({mode: "open"})
        this.render();
    }

    async render() {
        this.shadowRoot.innerHTML = "";
        this.hass = document.querySelector("home-assistant")?.hass;
        if (!this.hass) return;


        const css = await fetch('/local/varko_panel.css').then(r => r.text())
        const style = document.createElement('style')
        style.textContent = css

        const container = document.createElement('div')
        container.innerHTML = await fetch('/local/varko_panel.html').then(r => r.text())

        this.shadowRoot.append(style, container);

        this._loadLights();
        this._loadZones();
        this._loadPersons();
        this._loadAddDeviceDialog()
        this._loadDeviceElementDialog();
        this._loadZoneElementDialog();
        this._loadUserElementDialog()
        this._loadStatesListeners();
        this._populateCountrySelect();
        this._setupRadioStationsListeners();
        this._setupRadioButtons();
    }

    _setupRadioButtons() {
        const selectStationButton = this.shadowRoot.getElementById("select-station-button");
        const countrySelect = this.shadowRoot.getElementById("country-select");
        const stationSelect = this.shadowRoot.getElementById("station-select");

        selectStationButton.addEventListener("click", async () => {
            const selectedStation = stationSelect.value;
            const selectedCountry = countrySelect.value;
            await this._callService("varko.choose_radio_station", { station_name: selectedStation, radio_country_code: selectedCountry });
            console.log("Selected station:", selectedStation);
            console.log("Selected country:", selectedCountry);
        });
    }

    _populateCountrySelect() {
        const countrySelect = this.shadowRoot.getElementById("country-select");
        countries.forEach(country => {
            const option = document.createElement("option");
            option.value = country.code;
            option.textContent = country.name;
            countrySelect.appendChild(option);
        });

        countrySelect.addEventListener("change", async () => {
            const selectedCountry = countrySelect.value;
            await this._callService("varko.get_list_of_stations_per_country", { radio_country_code: selectedCountry });
            console.log("Selected country:", selectedCountry);
        });
    }

    _setupRadioStationsListeners() {
        this.hass.connection.subscribeEvents(
            (event) => {
                console.log("Received event:", event);
                if (event.event_type === "varko.radio_stations_list") {
                    this._handleRadioStations(event);
                }
            },
            "varko.radio_stations_list"
        );
    }

    _loadLights() {
        const holder = this.shadowRoot.getElementById("devices-holder");
        const entities = Object.values(this.hass.entities).filter(e => e.entity_id.startsWith("light."));

        for (const entity of entities) {
            const element = document.createElement("div")
            element.id = entity.entity_id;
            element.className = "element";
            element.textContent = entity.name;
            element.addEventListener("click", () => {
                const deviceElementDialog = this.shadowRoot.getElementById("device-element-dialog");
                deviceElementDialog.setAttribute("entityId", entity.entity_id);
                this._openDeviceElementDialog();
            });
            holder.appendChild(element);

            const option = document.createElement("option");
            option.value = entity.entity_id;
            option.textContent = entity.name;
            this.shadowRoot.getElementById("shelly-entity").appendChild(option.cloneNode(true));
        }
    }

    _loadZones() {
        const holder = this.shadowRoot.getElementById("zones-holder");
        const zones = Object.values(this.hass.states).filter(e => e.entity_id.startsWith("zone."));

        for (const zone of zones) {
            const element = document.createElement("div")
            element.id = zone.entity_id;
            element.className = "element";
            element.textContent = zone.attributes.friendly_name;
            element.addEventListener("click", () => {
                const zoneElementDialog = this.shadowRoot.getElementById("zone-element-dialog");
                zoneElementDialog.setAttribute("entityId", zone.entity_id);
                this._openZoneElementDialog();
            })
            holder.appendChild(element)
        }
    }

    _loadPersons() {
        const holder = this.shadowRoot.getElementById("groups-holder");
        const persons = Object.values(this.hass.states).filter(e => e.entity_id.startsWith("person."));

        for (const person of persons) {
            const element = document.createElement("div")
            element.id = person.entity_id;
            element.className = "element";
            element.textContent = person.attributes.friendly_name;
            element.addEventListener("click", () => {
                const userElementDialog = this.shadowRoot.getElementById("user-element-dialog");
                userElementDialog.setAttribute("entityId", person.entity_id);
                this._openUserElementDialog();
            })
            holder.appendChild(element)
        }
    }

    _loadAddDeviceDialog() {
        const addDeviceButton = this.shadowRoot.getElementById("add-device-button");
        const addDeviceDialog = this.shadowRoot.getElementById("add-device-dialog");
        addDeviceButton.addEventListener("click", () => {
            addDeviceDialog.showModal();
        })

        const closeButton = this.shadowRoot.getElementById("cancel-add-device");
        closeButton.addEventListener("click", () => {
            addDeviceDialog.close();
        })

        const shellyInput = this.shadowRoot.getElementById("shelly-entity");
        const conditionalFields = this.shadowRoot.getElementById("conditional-fields");

        shellyInput.addEventListener("input", () => {
            const isShellyFilled = shellyInput.value.trim() !== "";
            conditionalFields.classList.toggle("hidden", isShellyFilled);

            conditionalFields.querySelectorAll("input").forEach(input => {
                input.disabled = isShellyFilled;
            });
        });

        const addDeviceForm = this.shadowRoot.getElementById("addDeviceForm");
        addDeviceForm.addEventListener("submit", async (event) => {
            event.preventDefault()
            const formData = new FormData(addDeviceForm);
            const data = Object.fromEntries(formData.entries());
            data.is_enabled = addDeviceForm.elements.is_enabled.checked;
            await this._callService("varko.add_device", data);
            addDeviceDialog.close();
            await this.render()
        })
    }

    _loadDeviceElementDialog() {
        const deviceElementDialog = this.shadowRoot.getElementById("device-element-dialog");
        const closeButton = deviceElementDialog.querySelector("#cancel-device-button");
        closeButton.addEventListener("click", () => {
            deviceElementDialog.close();
        });

        const enableButton = deviceElementDialog.querySelector("#enable-device-button");
        enableButton.addEventListener("click", async() => {
            const entityId = deviceElementDialog.getAttribute("entityId");
            await this._callService("varko.enable_device", { entity: entityId });
            deviceElementDialog.close();
            await this.render();
        });

        const disableButton = deviceElementDialog.querySelector("#disable-device-button");
        disableButton.addEventListener("click", async () => {
            const entityId = deviceElementDialog.getAttribute("entityId");
            await this._callService("varko.disable_device", { entity: entityId });
            deviceElementDialog.close();
            await this.render();
        });

        const removeButton = deviceElementDialog.querySelector("#remove-device-button");
        removeButton.addEventListener("click", async () => {
            const entityId = deviceElementDialog.getAttribute("entityId");
            await this._callService("varko.remove_device", { entity: entityId });
            deviceElementDialog.close();
            await this.render();
        });
    }

    _openDeviceElementDialog() {
        const deviceElementDialog = this.shadowRoot.getElementById("device-element-dialog");
        const entityId = deviceElementDialog.getAttribute("entityId");
        deviceElementDialog.querySelector("h2").textContent = this.hass.states[entityId].attributes.friendly_name;
        deviceElementDialog.showModal();
    }

    _loadZoneElementDialog() {
        const zoneElementDialog = this.shadowRoot.getElementById("zone-element-dialog");
        const closeButton = zoneElementDialog.querySelector("#cancel-zone-button");
        closeButton.addEventListener("click", () => {
            zoneElementDialog.close();
        });

        const removeButton = zoneElementDialog.querySelector("#select-zone-button");
        removeButton.addEventListener("click", async () => {
            const entityId = zoneElementDialog.getAttribute("entityId");
            await this._callService("varko.select_activation_zone", { zone_entity_id: entityId });
            zoneElementDialog.close();
            await this.render();
        });
    }

    _openZoneElementDialog() {
        const zoneElementDialog = this.shadowRoot.getElementById("zone-element-dialog");
        const entityId = zoneElementDialog.getAttribute("entityId");
        zoneElementDialog.querySelector("h2").textContent = this.hass.states[entityId].attributes.friendly_name;
        zoneElementDialog.showModal();
    }

    _loadUserElementDialog() {
        const userElementDialog = this.shadowRoot.getElementById("user-element-dialog");
        const closeButton = userElementDialog.querySelector("#cancel-user-button");
        closeButton.addEventListener("click", () => {
            userElementDialog.close();
        });

        const removeButton = userElementDialog.querySelector("#remove-user-button");
        removeButton.addEventListener("click", async () => {
            const entityId = userElementDialog.getAttribute("entityId");
            await this._callService("varko.remove_person", { person: entityId });
            userElementDialog.close();
            await this.render();
        });

        const addButton = userElementDialog.querySelector("#add-user-button");
        addButton.addEventListener("click", async () => {
            const entityId = userElementDialog.getAttribute("entityId");
            await this._callService("varko.add_person", { person: entityId });
            userElementDialog.close();
            await this.render();
        });
    }

    _openUserElementDialog() {
        const userElementDialog = this.shadowRoot.getElementById("user-element-dialog");
        const entityId = userElementDialog.getAttribute("entityId");
        userElementDialog.querySelector("h2").textContent = this.hass.states[entityId].attributes.friendly_name;
        userElementDialog.showModal();
    }

    _loadStatesListeners() {
        const idleButton = this.shadowRoot.getElementById("set-state-idle");
        const activeButton = this.shadowRoot.getElementById("set-state-active");
        const readyButton = this.shadowRoot.getElementById("set-state-ready");

        idleButton.addEventListener("click", () => {
            this._callService("varko.set_state_idle", {});
            alert("State set to idle");
        });
        activeButton.addEventListener("click", () => {
            this._callService("varko.set_state_active", {});
            alert("State set to active");
        });
        readyButton.addEventListener("click", () => {
            this._callService("varko.set_state_ready", {});
            alert("State set to ready");
        });
    }

    _handleRadioStations(event) {
        console.log("Handling radio stations");
        const radioStations = event.data.stations;
        const countryCode = event.data.country_code;
        console.log(radioStations);
        console.log(countryCode);

        const stationSelect = this.shadowRoot.getElementById("station-select");
        stationSelect.innerHTML = "";
        radioStations.forEach(station => {
            const option = document.createElement("option");
            option.value = station;
            option.textContent = station;
            stationSelect.appendChild(option);
        });
    }

    async _callService(service, data = {}) {
        const [domain, serviceName] = service.split(".");
        await this.hass.callService(domain, serviceName, data);
    }
}

customElements.define("varko-panel", VarkoPanel);
