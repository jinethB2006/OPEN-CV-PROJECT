document.addEventListener('DOMContentLoaded', () => {
    // Clock update
    const clockElement = document.getElementById('clock');
    setInterval(() => {
        const now = new Date();
        clockElement.textContent = now.toLocaleTimeString();
    }, 1000);

    // API Polling
    const fpsElement = document.getElementById('fps');
    const latencyElement = document.getElementById('latency');
    const cpuBarElement = document.getElementById('cpu-bar');
    const cpuTextElement = document.getElementById('cpu');
    const alertListElement = document.getElementById('alert-list');
    
    // Store last alerts to prevent DOM flicker
    let lastAlertCount = 0;

    async function pollStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            // Update Metrics
            fpsElement.innerHTML = `${data.fps} <small>FPS</small>`;
            latencyElement.innerHTML = `${data.latency} <small>ms</small>`;
            
            // Update CPU Bar and Text
            cpuBarElement.style.width = `${data.cpu_load}%`;
            cpuTextElement.textContent = `${data.cpu_load}%`;
            
            // Change color based on load
            if (data.cpu_load > 80) {
                cpuBarElement.style.background = 'linear-gradient(90deg, var(--danger), #ff8a00)';
            } else {
                cpuBarElement.style.background = 'linear-gradient(90deg, var(--accent), #0066ff)';
            }

            // Update Alerts
            if (data.alerts.length === 0) {
                if (lastAlertCount !== 0) {
                    alertListElement.innerHTML = '<li class="alert-item empty-state">No critical alerts detected in the current session.</li>';
                    lastAlertCount = 0;
                }
            } else {
                alertListElement.innerHTML = '';
                data.alerts.slice().reverse().forEach(alertMsg => {
                    const li = document.createElement('li');
                    li.className = 'alert-item';
                    li.textContent = alertMsg;
                    alertListElement.appendChild(li);
                });
                lastAlertCount = data.alerts.length;
            }

        } catch (error) {
            console.error('Error fetching system status:', error);
        }
    }

    // Poll every 500ms
    setInterval(pollStatus, 500);
});
