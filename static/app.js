/**
 * OptiCrop Client-Side Interactivity
 * Handles dual slider-input synchronization, live weather sync via Open-Meteo,
 * dynamic pH status meters, and farm preset auto-fill.
 */

document.addEventListener("DOMContentLoaded", () => {
    // ----------------------------------------------------
    // 1. Dual Slider & Number Input Synchronization
    // ----------------------------------------------------
    const paramPairs = [
        { slider: "N_slider", input: "N" },
        { slider: "P_slider", input: "P" },
        { slider: "K_slider", input: "K" },
        { slider: "ph_slider", input: "ph" },
        { slider: "temp_slider", input: "temperature" },
        { slider: "hum_slider", input: "humidity" },
        { slider: "rain_slider", input: "rainfall" },
    ];

    const phBadge = document.getElementById("phBadge");

    function updatePhBadge(val) {
        if (!phBadge) return;
        const ph = parseFloat(val);
        phBadge.className = "ph-badge";

        if (ph < 6.0) {
            phBadge.classList.add("ph-acid");
            phBadge.textContent = `Acidic (${ph.toFixed(1)})`;
        } else if (ph <= 7.5) {
            phBadge.classList.add("ph-neutral");
            phBadge.textContent = `Optimal Neutral (${ph.toFixed(1)})`;
        } else {
            phBadge.classList.add("ph-alkaline");
            phBadge.textContent = `Alkaline (${ph.toFixed(1)})`;
        }
    }

    paramPairs.forEach(({ slider, input }) => {
        const sliderEl = document.getElementById(slider);
        const inputEl = document.getElementById(input);

        if (!sliderEl || !inputEl) return;

        // Slider -> Input
        sliderEl.addEventListener("input", (e) => {
            inputEl.value = e.target.value;
            if (input === "ph") updatePhBadge(e.target.value);
        });

        // Input -> Slider
        inputEl.addEventListener("input", (e) => {
            sliderEl.value = e.target.value;
            if (input === "ph") updatePhBadge(e.target.value);
        });
    });

    // Initialize pH badge state on load
    const initialPh = document.getElementById("ph");
    if (initialPh) updatePhBadge(initialPh.value);

    // ----------------------------------------------------
    // 2. Preset Farm Profiles Autofill
    // ----------------------------------------------------
    const presetButtons = document.querySelectorAll(".preset-chip");

    function setFieldValue(id, val) {
        const input = document.getElementById(id);
        const slider = document.getElementById(id + "_slider") || document.getElementById(id.replace("temperature", "temp").replace("humidity", "hum").replace("rainfall", "rain") + "_slider");

        if (input) input.value = val;
        if (slider) slider.value = val;
        if (id === "ph") updatePhBadge(val);
    }

    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            try {
                const values = JSON.parse(btn.getAttribute("data-preset"));
                if (!values) return;

                setFieldValue("N", values.N);
                setFieldValue("P", values.P);
                setFieldValue("K", values.K);
                setFieldValue("ph", values.ph);
                setFieldValue("temperature", values.temperature);
                setFieldValue("humidity", values.humidity);
                setFieldValue("rainfall", values.rainfall);

                // Highlight chosen preset briefly
                presetButtons.forEach(b => b.style.borderColor = "var(--border)");
                btn.style.borderColor = "var(--primary)";
                btn.style.backgroundColor = "var(--primary-light)";

                showWeatherStatus(`Loaded preset: ${btn.querySelector('.chip-title')?.textContent || 'Farm Profile'}`, "success");
            } catch (err) {
                console.error("Failed to load preset:", err);
            }
        });
    });

    // ----------------------------------------------------
    // 3. Live Weather Integration (Open-Meteo)
    // ----------------------------------------------------
    const cityInput = document.getElementById("cityInput");
    const btnSearchCity = document.getElementById("btnSearchCity");
    const btnDetectLocation = document.getElementById("btnDetectLocation");
    const weatherStatus = document.getElementById("weatherStatus");
    const weatherStatusText = document.getElementById("weatherStatusText");

    function showWeatherStatus(message, type = "info") {
        if (!weatherStatus || !weatherStatusText) return;
        weatherStatusText.textContent = message;
        weatherStatus.className = `weather-status-badge ${type}`;
        weatherStatus.classList.remove("hidden");
    }

    async function fetchWeather(queryParams) {
        showWeatherStatus("Connecting to meteorological satellite feed...", "info");
        try {
            const res = await fetch(`/api/weather?${queryParams}`);
            const data = await res.json();

            if (data.status === "success") {
                setFieldValue("temperature", data.temperature);
                setFieldValue("humidity", data.humidity);
                setFieldValue("rainfall", data.rainfall);

                showWeatherStatus(
                    `📍 Synced for ${data.location}: ${data.temperature}°C, ${data.humidity}% Humidity, ~${data.rainfall}mm Rainfall`,
                    "success"
                );
            } else {
                showWeatherStatus(`Weather Error: ${data.message || "Failed to fetch"}`, "error");
            }
        } catch (err) {
            showWeatherStatus("Unable to contact weather service. Check your internet connection.", "error");
        }
    }

    if (btnSearchCity && cityInput) {
        btnSearchCity.addEventListener("click", () => {
            const city = cityInput.value.trim();
            if (!city) {
                showWeatherStatus("Please type a city name (e.g., Pune, Punjab, Cairo, Fresno).", "error");
                return;
            }
            fetchWeather(`city=${encodeURIComponent(city)}`);
        });

        cityInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                btnSearchCity.click();
            }
        });
    }

    if (btnDetectLocation) {
        btnDetectLocation.addEventListener("click", () => {
            if (!navigator.geolocation) {
                showWeatherStatus("Geolocation is not supported by your browser.", "error");
                return;
            }

            showWeatherStatus("Requesting device GPS coordinates...", "info");

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude.toFixed(4);
                    const lon = position.coords.longitude.toFixed(4);
                    fetchWeather(`lat=${lat}&lon=${lon}`);
                },
                (error) => {
                    showWeatherStatus(`GPS location access denied or unavailable (${error.message}). You can still enter your city name above.`, "error");
                },
                { timeout: 8000 }
            );
        });
    }

    // ----------------------------------------------------
    // 4. Reset Button
    // ----------------------------------------------------
    const btnReset = document.getElementById("btnReset");
    if (btnReset) {
        btnReset.addEventListener("click", () => {
            setFieldValue("N", 90);
            setFieldValue("P", 42);
            setFieldValue("K", 43);
            setFieldValue("ph", 6.5);
            setFieldValue("temperature", 23.5);
            setFieldValue("humidity", 82);
            setFieldValue("rainfall", 200);

            if (cityInput) cityInput.value = "";
            if (weatherStatus) weatherStatus.classList.add("hidden");
            presetButtons.forEach(b => {
                b.style.borderColor = "var(--border)";
                b.style.backgroundColor = "var(--bg)";
            });
        });
    }
});
