// NEXUS AI - Control Center
// NitroSense Style Interface

// Circular Gauge Class (same as before, optimized)
class CircularGauge {
    constructor(canvas, options) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.value = options.value || 0;
        this.max = options.max || 100;
        this.unit = options.unit || '';
        this.label = options.label || '';
        this.rotation = 0;

        this.animate();
    }

    setValue(value) {
        this.value = value;
    }

    draw() {
        const ctx = this.ctx;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;

        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Background circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.strokeStyle = 'rgba(255, 102, 0, 0.15)';
        ctx.lineWidth = 15;
        ctx.stroke();

        // Progress arc with gradient
        const progress = (this.value / this.max) * 2 * Math.PI;
        const gradient = ctx.createLinearGradient(
            centerX - radius, centerY,
            centerX + radius, centerY
        );
        gradient.addColorStop(0, '#FF6600');
        gradient.addColorStop(0.5, '#ff8833');
        gradient.addColorStop(1, '#ff3333');

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, -Math.PI / 2, -Math.PI / 2 + progress);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 15;
        ctx.lineCap = 'round';
        ctx.stroke();

        // Center text
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 48px Segoe UI';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(this.value), centerX, centerY - 5);

        ctx.fillStyle = '#888888';
        ctx.font = '18px Segoe UI';
        ctx.fillText(this.unit, centerX, centerY + 30);
    }

    animate() {
        this.rotation += 0.01;
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Live Wave Graph Class
class LiveWave {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.data = [];
        this.maxPoints = 40;

        // Initialize with some data
        for (let i = 0; i < this.maxPoints; i++) {
            this.data.push(Math.random() * 30 + 10);
        }
    }

    addData(value) {
        this.data.push(value);
        if (this.data.length > this.maxPoints) {
            this.data.shift();
        }
        this.draw();
    }

    draw() {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        ctx.clearRect(0, 0, width, height);

        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.fillRect(0, 0, width, height);

        // Draw waveform
        if (this.data.length > 1) {
            const stepX = width / (this.maxPoints - 1);

            // Gradient line
            const gradient = ctx.createLinearGradient(0, 0, width, 0);
            gradient.addColorStop(0, '#ff3333');
            gradient.addColorStop(0.5, '#FF6600');
            gradient.addColorStop(1, '#ff8833');

            ctx.beginPath();
            this.data.forEach((value, index) => {
                const x = index * stepX;
                const y = height - (value / 100) * height;

                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });

            ctx.strokeStyle = gradient;
            ctx.lineWidth = 2.5;
            ctx.shadowBlur = 8;
            ctx.shadowColor = 'rgba(255, 102, 0, 0.6)';
            ctx.stroke();
            ctx.shadowBlur = 0;
        }
    }
}

// Initialize
let gauges = {};
let waves = {};

document.addEventListener('DOMContentLoaded', () => {
    initializeGauges();
    initializeWaves();
    initializeTabNavigation();
    initializeInteractions();

    // Start live updates
    setInterval(updateMetrics, 2000);
    updateMetrics();
});

function initializeGauges() {
    // Frequency gauge
    const freqCanvas = document.getElementById('frequencyGauge');
    if (freqCanvas) {
        gauges.frequency = new CircularGauge(freqCanvas, {
            value: 1320,
            max: 3000,
            unit: 'MHz',
            label: 'GPU'
        });
    }

    // Temperature gauges
    const gpuTempCanvas = document.getElementById('gpuTempGauge');
    if (gpuTempCanvas) {
        gauges.gpuTemp = new CircularGauge(gpuTempCanvas, {
            value: 50,
            max: 100,
            unit: '°C'
        });
    }

    const cpuTempCanvas = document.getElementById('cpuTempGauge');
    if (cpuTempCanvas) {
        gauges.cpuTemp = new CircularGauge(cpuTempCanvas, {
            value: 61,
            max: 100,
            unit: '°C'
        });
    }

    const sysTempCanvas = document.getElementById('sysTempGauge');
    if (sysTempCanvas) {
        gauges.sysTemp = new CircularGauge(sysTempCanvas, {
            value: 49,
            max: 100,
            unit: '°C'
        });
    }
}

function initializeWaves() {
    const gpuWave = document.getElementById('gpuUsageWave');
    if (gpuWave) {
        waves.gpuUsage = new LiveWave(gpuWave);
    }

    const cpuWave = document.getElementById('cpuUsageWave');
    if (cpuWave) {
        waves.cpuUsage = new LiveWave(cpuWave);
    }

    const aiMonitor = document.getElementById('aiMonitorGraph');
    if (aiMonitor) {
        waves.aiMonitor = new LiveWave(aiMonitor);
    }

    const sysMonitor = document.getElementById('sysMonitorGraph');
    if (sysMonitor) {
        waves.sysMonitor = new LiveWave(sysMonitor);
    }
}

function initializeTabNavigation() {
    const tabs = document.querySelectorAll('.nav-tab');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = tab.dataset.tab;

            // Remove active from all
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // Add active to selected
            tab.classList.add('active');
            const targetContent = document.getElementById(`tab-${targetTab}`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

function initializeInteractions() {
    // Mode selector
    document.querySelectorAll('.mode-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.mode-option').forEach(o => o.classList.remove('active'));
            option.classList.add('active');
        });
    });

    // App launch buttons
    document.querySelectorAll('.launch-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            btn.textContent = 'ACTIVE';
            btn.style.background = '#FF6600';
            btn.style.color = '#fff';

            setTimeout(() => {
                btn.textContent = 'Launch';
                btn.style.background = '';
                btn.style.color = '';
            }, 2000);
        });
    });
}

function updateMetrics() {
    // Simulate realistic data
    const gpuFreq = Math.random() * 300 + 1200;
    const gpuTemp = Math.random() * 15 + 45;
    const cpuTemp = Math.random() * 15 + 55;
    const sysTemp = Math.random() * 10 + 45;
    const gpuUsage = Math.random() * 30 + 10;
    const cpuUsage = Math.random() * 30 + 10;
    const ramPercent = Math.random() * 10 + 60;

    // Update gauges
    if (gauges.frequency) gauges.frequency.setValue(gpuFreq);
    if (gauges.gpuTemp) gauges.gpuTemp.setValue(gpuTemp);
    if (gauges.cpuTemp) gauges.cpuTemp.setValue(cpuTemp);
    if (gauges.sysTemp) gauges.sysTemp.setValue(sysTemp);

    // Update waves
    if (waves.gpuUsage) waves.addData(gpuUsage);
    if (waves.cpuUsage) waves.addData(cpuUsage);
    if (waves.aiMonitor) waves.addData(gpuUsage);
    if (waves.sysMonitor) waves.addData(cpuUsage);

    // Update text values
    updateElement('gpuUsageText', Math.round(gpuUsage) + '%');
    updateElement('cpuUsageText', Math.round(cpuUsage) + '%');

    // Update sidebar metrics
    updateElement('gpuPercent', Math.round(gpuUsage));
    updateElement('gpuDegrees', Math.round(gpuTemp));
    updateElement('cpuPercent', Math.round(cpuUsage));
    updateElement('cpuDegrees', Math.round(cpuTemp));
    updateElement('sysDegrees', Math.round(sysTemp));
    updateElement('ramPercent', ramPercent.toFixed(1));
}

function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

console.log('NEXUS AI Control Center initialized');
