// NEXUS OS - Advanced Visual Effects
// Particle system, animations, and interactive elements

class ParticleSystem {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'particle-canvas';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '0';
        this.canvas.style.opacity = '0.4';

        document.body.insertBefore(this.canvas, document.body.firstChild);

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.connectionDistance = 150;
        this.mouseX = 0;
        this.mouseY = 0;

        this.resize();
        this.init();
        this.animate();

        window.addEventListener('resize', () => this.resize());
        document.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    init() {
        const particleCount = Math.floor((this.canvas.width * this.canvas.height) / 15000);
        this.particles = [];

        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw particles
        this.particles.forEach((particle, i) => {
            // Move particle
            particle.x += particle.vx;
            particle.y += particle.vy;

            // Bounce off edges
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;

            // Mouse interaction - repel particles
            const dx = this.mouseX - particle.x;
            const dy = this.mouseY - particle.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 100) {
                const force = (100 - dist) / 100;
                particle.x -= dx * force * 0.05;
                particle.y -= dy * force * 0.05;
            }

            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 102, 0, ${particle.opacity})`;
            this.ctx.fill();

            // Draw connections
            for (let j = i + 1; j < this.particles.length; j++) {
                const other = this.particles[j];
                const dx = particle.x - other.x;
                const dy = particle.y - other.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < this.connectionDistance) {
                    const opacity = (1 - distance / this.connectionDistance) * 0.3;
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(255, 102, 0, ${opacity})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(other.x, other.y);
                    this.ctx.stroke();
                }
            }
        });

        requestAnimationFrame(() => this.animate());
    }
}

// Glowing cursor trail
class CursorTrail {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '9999';

        document.body.appendChild(this.canvas);

        this.ctx = this.canvas.getContext('2d');
        this.trail = [];
        this.maxTrail = 20;

        this.resize();
        this.animate();

        window.addEventListener('resize', () => this.resize());
        document.addEventListener('mousemove', (e) => {
            this.trail.push({
                x: e.clientX,
                y: e.clientY,
                life: 1
            });

            if (this.trail.length > this.maxTrail) {
                this.trail.shift();
            }
        });
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.trail.forEach((point, index) => {
            point.life -= 0.05;

            if (point.life > 0) {
                const size = 8 * point.life;
                const gradient = this.ctx.createRadialGradient(
                    point.x, point.y, 0,
                    point.x, point.y, size
                );

                gradient.addColorStop(0, `rgba(255, 102, 0, ${point.life * 0.4})`);
                gradient.addColorStop(1, 'rgba(255, 102, 0, 0)');

                this.ctx.fillStyle = gradient;
                this.ctx.fillRect(point.x - size, point.y - size, size * 2, size * 2);
            }
        });

        this.trail = this.trail.filter(p => p.life > 0);

        requestAnimationFrame(() => this.animate());
    }
}

// Scan line effect
class ScanLineEffect {
    constructor() {
        this.scanLine = document.createElement('div');
        this.scanLine.style.position = 'fixed';
        this.scanLine.style.left = '0';
        this.scanLine.style.width = '100%';
        this.scanLine.style.height = '2px';
        this.scanLine.style.background = 'linear-gradient(90deg, transparent, rgba(255, 102, 0, 0.6), transparent)';
        this.scanLine.style.pointerEvents = 'none';
        this.scanLine.style.zIndex = '1';
        this.scanLine.style.boxShadow = '0 0 20px rgba(255, 102, 0, 0.8)';

        document.body.appendChild(this.scanLine);

        this.position = 0;
        this.animate();
    }

    animate() {
        this.position += 2;

        if (this.position > window.innerHeight) {
            this.position = -100;
        }

        this.scanLine.style.top = `${this.position}px`;

        requestAnimationFrame(() => this.animate());
    }
}

// Hexagonal grid overlay
function createHexGrid() {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.style.position = 'fixed';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.width = '100%';
    svg.style.height = '100%';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '0';
    svg.style.opacity = '0.03';

    const pattern = document.createElementNS('http://www.w3.org/2000/svg', 'pattern');
    pattern.setAttribute('id', 'hexPattern');
    pattern.setAttribute('x', '0');
    pattern.setAttribute('y', '0');
    pattern.setAttribute('width', '50');
    pattern.setAttribute('height', '43');
    pattern.setAttribute('patternUnits', 'userSpaceOnUse');

    const hexPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    hexPath.setAttribute('d', 'M25,5 L45,15 L45,35 L25,45 L5,35 L5,15 Z');
    hexPath.setAttribute('fill', 'none');
    hexPath.setAttribute('stroke', '#FF6600');
    hexPath.setAttribute('stroke-width', '1');

    pattern.appendChild(hexPath);
    svg.appendChild(pattern);

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('width', '100%');
    rect.setAttribute('height', '100%');
    rect.setAttribute('fill', 'url(#hexPattern)');

    svg.appendChild(rect);
    document.body.insertBefore(svg, document.body.firstChild);
}

// Initialize all effects when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEffects);
} else {
    initEffects();
}

function initEffects() {
    // Wait a bit for page to settle
    setTimeout(() => {
        new ParticleSystem();
        new CursorTrail();
        new ScanLineEffect();
        createHexGrid();

        console.log('Visual effects initialized');
    }, 500);
}

// Add button ripple effect
document.addEventListener('click', (e) => {
    const button = e.target.closest('button, .btn, .mode-card, .app-card');

    if (button) {
        const ripple = document.createElement('div');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.position = 'absolute';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = size + 'px';
        ripple.style.height = size + 'px';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'radial-gradient(circle, rgba(255, 102, 0, 0.6), transparent)';
        ripple.style.pointerEvents = 'none';
        ripple.style.animation = 'ripple 0.6s ease-out';

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
