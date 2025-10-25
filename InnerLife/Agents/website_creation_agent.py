#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Website Creation Agent
Enables Nexus to design and develop websites
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class WebsiteCreationAgent(Agent):
    """Agent for website creation and development capabilities"""
    
    def __init__(self):
        """Initialize the website creation agent"""
        super().__init__(
            name="WebsiteCreation",
            description="Creates and develops websites based on specifications",
            capabilities=[
                "Design website layouts and wireframes",
                "Generate responsive HTML/CSS/JavaScript code",
                "Create full websites from descriptions",
                "Build interactive web applications",
                "Design and implement UI/UX elements"
            ]
        )
        self.project_history = []
        self.active_projects = {}
        self.projects_dir = Path("D:/AIArm/InnerLife/Generated/Websites")
        self.projects_dir.mkdir(exist_ok=True, parents=True)
        
    def process(self, specification, context=None, options=None):
        """Process a website creation request"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}
        
        self.last_used = datetime.now().isoformat()
        
        # Set default options if none provided
        if options is None:
            options = {
                "framework": "vanilla",  # vanilla, react, vue, etc.
                "responsive": True,
                "include_cms": False,
                "template": "modern"
            }
        
        # Generate a project ID
        project_id = f"website_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create project directory
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # Log the project
        project_entry = {
            "project_id": project_id,
            "specification": specification,
            "timestamp": self.last_used,
            "context": context,
            "options": options,
            "directory": str(project_dir)
        }
        self.project_history.append(project_entry)
        
        # Add to active projects
        self.active_projects[project_id] = project_entry
        
        # Generate the website
        result = self._generate_website(project_id, specification, options)
        
        # Update project entry with result
        project_entry["result"] = result
        
        return {
            "status": result["status"],
            "message": result["message"],
            "project_id": project_id,
            "project_dir": str(project_dir),
            "files": result.get("files", [])
        }
    
    def _generate_website(self, project_id, specification, options):
        """Generate website based on specification"""
        project_dir = self.projects_dir / project_id
        
        try:
            # Create specification file
            spec_file = project_dir / "specification.txt"
            with open(spec_file, "w") as f:
                f.write(f"Website Specification:\n\n{specification}\n\n")
                f.write(f"Options:\n{json.dumps(options, indent=2)}\n\n")
                f.write(f"Generated at: {datetime.now().isoformat()}\n")
            
            # Create project structure based on framework
            framework = options.get("framework", "vanilla")
            
            if framework == "vanilla":
                # Create basic HTML/CSS/JS structure
                self._create_vanilla_structure(project_dir, specification, options)
            elif framework == "react":
                # Create React project structure
                self._create_react_structure(project_dir, specification, options)
            elif framework == "vue":
                # Create Vue project structure
                self._create_vue_structure(project_dir, specification, options)
            else:
                # Default to vanilla
                self._create_vanilla_structure(project_dir, specification, options)
            
            # Get list of generated files
            files = []
            for path in project_dir.glob("**/*"):
                if path.is_file():
                    files.append(str(path.relative_to(project_dir)))
            
            return {
                "status": "success",
                "message": f"Website project created successfully using {framework} framework",
                "files": files
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating website: {str(e)}"
            }
    
    def _create_vanilla_structure(self, project_dir, specification, options):
        """Create a basic HTML/CSS/JS website structure"""
        # Create index.html
        with open(project_dir / "index.html", "w") as f:
            f.write(self._generate_html_template(specification, options))
        
        # Create CSS directory and styles
        css_dir = project_dir / "css"
        css_dir.mkdir(exist_ok=True)
        
        with open(css_dir / "styles.css", "w") as f:
            f.write(self._generate_css_template(options))
        
        # Create JS directory and script
        js_dir = project_dir / "js"
        js_dir.mkdir(exist_ok=True)
        
        with open(js_dir / "main.js", "w") as f:
            f.write(self._generate_js_template(options))
        
        # Create assets directory
        assets_dir = project_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        # Create a readme file
        with open(project_dir / "README.md", "w") as f:
            f.write(self._generate_readme(specification, options))
    
    def _create_react_structure(self, project_dir, specification, options):
        """Create a React project structure"""
        # In a real implementation, this would use npm/yarn to create a React project
        # For this simulation, we'll create a simplified structure
        
        # Create package.json
        with open(project_dir / "package.json", "w") as f:
            f.write(json.dumps({
                "name": project_dir.name,
                "version": "0.1.0",
                "private": True,
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "react-scripts": "5.0.1"
                },
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                }
            }, indent=2))
        
        # Create src directory
        src_dir = project_dir / "src"
        src_dir.mkdir(exist_ok=True)
        
        # Create App.js
        with open(src_dir / "App.js", "w") as f:
            f.write(self._generate_react_app(specification, options))
        
        # Create index.js
        with open(src_dir / "index.js", "w") as f:
            f.write(self._generate_react_index())
        
        # Create public directory
        public_dir = project_dir / "public"
        public_dir.mkdir(exist_ok=True)
        
        # Create index.html
        with open(public_dir / "index.html", "w") as f:
            f.write(self._generate_react_html_template())
        
        # Create a readme file
        with open(project_dir / "README.md", "w") as f:
            f.write(self._generate_readme(specification, options))
    
    def _create_vue_structure(self, project_dir, specification, options):
        """Create a Vue project structure"""
        # In a real implementation, this would use Vue CLI to create a Vue project
        # For this simulation, we'll create a simplified structure
        
        # Create package.json
        with open(project_dir / "package.json", "w") as f:
            f.write(json.dumps({
                "name": project_dir.name,
                "version": "0.1.0",
                "private": True,
                "scripts": {
                    "serve": "vue-cli-service serve",
                    "build": "vue-cli-service build"
                },
                "dependencies": {
                    "core-js": "^3.8.3",
                    "vue": "^3.2.13"
                },
                "devDependencies": {
                    "@vue/cli-plugin-babel": "~5.0.0",
                    "@vue/cli-service": "~5.0.0"
                }
            }, indent=2))
        
        # Create src directory
        src_dir = project_dir / "src"
        src_dir.mkdir(exist_ok=True)
        
        # Create App.vue
        with open(src_dir / "App.vue", "w") as f:
            f.write(self._generate_vue_app(specification, options))
        
        # Create main.js
        with open(src_dir / "main.js", "w") as f:
            f.write(self._generate_vue_main())
        
        # Create public directory
        public_dir = project_dir / "public"
        public_dir.mkdir(exist_ok=True)
        
        # Create index.html
        with open(public_dir / "index.html", "w") as f:
            f.write(self._generate_vue_html_template())
        
        # Create a readme file
        with open(project_dir / "README.md", "w") as f:
            f.write(self._generate_readme(specification, options))
    
    def _generate_html_template(self, specification, options):
        """Generate HTML template based on specification"""
        template = options.get("template", "modern")
        responsive = options.get("responsive", True)
        
        # Extract a title from the specification
        lines = specification.split('\n')
        title = "New Website"
        for line in lines:
            if line.strip().lower().startswith(("title:", "website title:", "site title:")):
                title = line.split(':', 1)[1].strip()
                break
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">
                <h1>{title}</h1>
            </div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
            <div class="burger">
                <div class="line1"></div>
                <div class="line2"></div>
                <div class="line3"></div>
            </div>
        </nav>
    </header>

    <main>
        <section class="hero">
            <h2>Welcome to {title}</h2>
            <p>This is a website generated by Nexus AI based on your specifications.</p>
        </section>

        <section class="content">
            <h3>About Us</h3>
            <p>This section would contain information about your company or organization.</p>
        </section>

        <section class="services">
            <h3>Our Services</h3>
            <div class="service-grid">
                <div class="service-card">
                    <h4>Service 1</h4>
                    <p>Description of service 1</p>
                </div>
                <div class="service-card">
                    <h4>Service 2</h4>
                    <p>Description of service 2</p>
                </div>
                <div class="service-card">
                    <h4>Service 3</h4>
                    <p>Description of service 3</p>
                </div>
            </div>
        </section>

        <section class="contact">
            <h3>Contact Us</h3>
            <form>
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" name="message" rows="5" required></textarea>
                </div>
                <button type="submit">Send Message</button>
            </form>
        </section>
    </main>

    <footer>
        <p>&copy; {datetime.now().year} {title}. All rights reserved.</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
"""
        return html
    
    def _generate_css_template(self, options):
        """Generate CSS template based on options"""
        template = options.get("template", "modern")
        responsive = options.get("responsive", True)
        
        css = """/* Base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

/* Navigation */
nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 8vh;
    background-color: #2c3e50;
    padding: 0 5%;
    color: white;
}

.logo h1 {
    font-size: 1.5rem;
}

.nav-links {
    display: flex;
    justify-content: space-around;
    width: 40%;
}

.nav-links li {
    list-style: none;
}

.nav-links a {
    color: white;
    text-decoration: none;
    letter-spacing: 2px;
    font-weight: bold;
    font-size: 14px;
}

.burger {
    display: none;
    cursor: pointer;
}

.burger div {
    width: 25px;
    height: 3px;
    background-color: white;
    margin: 5px;
    transition: all 0.3s ease;
}

/* Main content */
main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

section {
    margin-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 3rem 0;
    background-color: #ecf0f1;
    border-radius: 5px;
    margin-bottom: 2rem;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.service-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.service-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.service-card h4 {
    margin-bottom: 0.5rem;
    color: #2c3e50;
}

/* Forms */
form {
    background-color: white;
    padding: 2rem;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

input, textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-family: inherit;
}

button {
    background-color: #2c3e50;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 3px;
    cursor: pointer;
    font-weight: bold;
}

button:hover {
    background-color: #1a252f;
}

/* Footer */
footer {
    background-color: #2c3e50;
    color: white;
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
}

/* Responsive styles */
@media screen and (max-width: 1024px) {
    .nav-links {
        width: 60%;
    }
}

@media screen and (max-width: 768px) {
    body {
        overflow-x: hidden;
    }
    
    .nav-links {
        position: absolute;
        right: 0px;
        height: 92vh;
        top: 8vh;
        background-color: #2c3e50;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 50%;
        transform: translateX(100%);
        transition: transform 0.5s ease-in;
        z-index: 1;
    }
    
    .nav-links li {
        opacity: 0;
    }
    
    .burger {
        display: block;
    }
    
    .nav-active {
        transform: translateX(0%);
    }
    
    .service-grid {
        grid-template-columns: 1fr;
    }
}

@keyframes navLinkFade {
    from {
        opacity: 0;
        transform: translateX(50px);
    }
    to {
        opacity: 1;
        transform: translateX(0px);
    }
}

.toggle .line1 {
    transform: rotate(-45deg) translate(-5px, 6px);
}

.toggle .line2 {
    opacity: 0;
}

.toggle .line3 {
    transform: rotate(45deg) translate(-5px, -6px);
}
"""
        return css
    
    def _generate_js_template(self, options):
        """Generate JavaScript template based on options"""
        js = """// Mobile Navigation Toggle
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    
    burger.addEventListener('click', () => {
        // Toggle Navigation
        nav.classList.toggle('nav-active');
        
        // Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });
        
        // Burger Animation
        burger.classList.toggle('toggle');
    });
}

// Form Validation
const formValidation = () => {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Basic validation
            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');
            
            let isValid = true;
            
            if (!name.value.trim()) {
                isValid = false;
                alert('Please enter your name');
            }
            
            if (!email.value.trim()) {
                isValid = false;
                alert('Please enter your email');
            } else if (!isValidEmail(email.value)) {
                isValid = false;
                alert('Please enter a valid email');
            }
            
            if (!message.value.trim()) {
                isValid = false;
                alert('Please enter your message');
            }
            
            if (isValid) {
                // Here you would typically submit the form or send the data
                alert('Form submitted successfully!');
                form.reset();
            }
        });
    }
}

// Helper function to validate email
const isValidEmail = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

// Initialize
const app = () => {
    navSlide();
    formValidation();
}

document.addEventListener('DOMContentLoaded', app);
"""
        return js
    
    def _generate_react_app(self, specification, options):
        """Generate React App.js based on specification"""
        js = """import React, { useState } from 'react';
import './App.css';

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  
  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // Form validation would go here
    console.log('Form submitted:', formData);
    alert('Form submitted successfully!');
    setFormData({
      name: '',
      email: '',
      message: ''
    });
  };
  
  return (
    <div className="App">
      <header>
        <nav>
          <div className="logo">
            <h1>React Website</h1>
          </div>
          <ul className={`nav-links ${menuOpen ? 'nav-active' : ''}`}>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
          <div className={`burger ${menuOpen ? 'toggle' : ''}`} onClick={toggleMenu}>
            <div className="line1"></div>
            <div className="line2"></div>
            <div className="line3"></div>
          </div>
        </nav>
      </header>

      <main>
        <section className="hero">
          <h2>Welcome to React Website</h2>
          <p>This is a React website generated by Nexus AI based on your specifications.</p>
        </section>

        <section className="content">
          <h3>About Us</h3>
          <p>This section would contain information about your company or organization.</p>
        </section>

        <section className="services">
          <h3>Our Services</h3>
          <div className="service-grid">
            {[1, 2, 3].map((num) => (
              <div className="service-card" key={num}>
                <h4>Service {num}</h4>
                <p>Description of service {num}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="contact">
          <h3>Contact Us</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input 
                type="text" 
                id="name" 
                name="name" 
                value={formData.name}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input 
                type="email" 
                id="email" 
                name="email" 
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="message">Message</label>
              <textarea 
                id="message" 
                name="message" 
                rows="5" 
                value={formData.message}
                onChange={handleInputChange}
                required
              ></textarea>
            </div>
            <button type="submit">Send Message</button>
          </form>
        </section>
      </main>

      <footer>
        <p>&copy; {new Date().getFullYear()} React Website. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
"""
        return js
    
    def _generate_react_index(self):
        """Generate React index.js"""
        js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
        return js
    
    def _generate_react_html_template(self):
        """Generate React HTML template"""
        html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Website created using React"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>React Website</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""
        return html
    
    def _generate_vue_app(self, specification, options):
        """Generate Vue App.vue based on specification"""
        vue = """<template>
  <div id="app">
    <header>
      <nav>
        <div class="logo">
          <h1>Vue Website</h1>
        </div>
        <ul class="nav-links" :class="{ 'nav-active': menuOpen }">
          <li><a href="#">Home</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Services</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
        <div class="burger" :class="{ 'toggle': menuOpen }" @click="toggleMenu">
          <div class="line1"></div>
          <div class="line2"></div>
          <div class="line3"></div>
        </div>
      </nav>
    </header>

    <main>
      <section class="hero">
        <h2>Welcome to Vue Website</h2>
        <p>This is a Vue website generated by Nexus AI based on your specifications.</p>
      </section>

      <section class="content">
        <h3>About Us</h3>
        <p>This section would contain information about your company or organization.</p>
      </section>

      <section class="services">
        <h3>Our Services</h3>
        <div class="service-grid">
          <div class="service-card" v-for="n in 3" :key="n">
            <h4>Service {{ n }}</h4>
            <p>Description of service {{ n }}</p>
          </div>
        </div>
      </section>

      <section class="contact">
        <h3>Contact Us</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">Name</label>
            <input 
              type="text" 
              id="name" 
              v-model="formData.name"
              required
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email"
              required
            />
          </div>
          <div class="form-group">
            <label for="message">Message</label>
            <textarea 
              id="message" 
              rows="5" 
              v-model="formData.message"
              required
            ></textarea>
          </div>
          <button type="submit">Send Message</button>
        </form>
      </section>
    </main>

    <footer>
      <p>&copy; {{ new Date().getFullYear() }} Vue Website. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      menuOpen: false,
      formData: {
        name: '',
        email: '',
        message: ''
      }
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    handleSubmit() {
      // Form validation would go here
      console.log('Form submitted:', this.formData);
      alert('Form submitted successfully!');
      this.formData = {
        name: '',
        email: '',
        message: ''
      };
    }
  }
}
</script>

<style>
/* Base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
}

/* Navigation */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 8vh;
  background-color: #2c3e50;
  padding: 0 5%;
  color: white;
}

.logo h1 {
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  justify-content: space-around;
  width: 40%;
}

.nav-links li {
  list-style: none;
}

.nav-links a {
  color: white;
  text-decoration: none;
  letter-spacing: 2px;
  font-weight: bold;
  font-size: 14px;
}

.burger {
  display: none;
  cursor: pointer;
}

.burger div {
  width: 25px;
  height: 3px;
  background-color: white;
  margin: 5px;
  transition: all 0.3s ease;
}

/* Main content */
main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

section {
  margin-bottom: 3rem;
}

.hero {
  text-align: center;
  padding: 3rem 0;
  background-color: #ecf0f1;
  border-radius: 5px;
  margin-bottom: 2rem;
}

.hero h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.service-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.service-card h4 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

/* Forms */
form {
  background-color: white;
  padding: 2rem;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 3px;
  font-family: inherit;
}

button {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 3px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #1a252f;
}

/* Footer */
footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
}

/* Responsive styles */
@media screen and (max-width: 1024px) {
  .nav-links {
    width: 60%;
  }
}

@media screen and (max-width: 768px) {
  body {
    overflow-x: hidden;
  }
  
  .nav-links {
    position: absolute;
    right: 0px;
    height: 92vh;
    top: 8vh;
    background-color: #2c3e50;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 50%;
    transform: translateX(100%);
    transition: transform 0.5s ease-in;
    z-index: 1;
  }
  
  .nav-links li {
    opacity: 0;
  }
  
  .burger {
    display: block;
  }
  
  .nav-active {
    transform: translateX(0%);
  }
  
  .service-grid {
    grid-template-columns: 1fr;
  }
}

@keyframes navLinkFade {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0px);
  }
}

.toggle .line1 {
  transform: rotate(-45deg) translate(-5px, 6px);
}

.toggle .line2 {
  opacity: 0;
}

.toggle .line3 {
  transform: rotate(45deg) translate(-5px, -6px);
}
</style>
"""
        return vue
    
    def _generate_vue_main(self):
        """Generate Vue main.js"""
        js = """import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
"""
        return js
    
    def _generate_vue_html_template(self):
        """Generate Vue HTML template"""
        html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="icon" href="<%= BASE_URL %>favicon.ico">
    <title>Vue Website</title>
  </head>
  <body>
    <noscript>
      <strong>We're sorry but this website doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
    </noscript>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>
"""
        return html
    
    def _generate_readme(self, specification, options):
        """Generate README.md for the project"""
        framework = options.get("framework", "vanilla")
        
        readme = f"""# Website Project

This website was generated by the Nexus Website Creation Agent.

## Specification

{specification}

## Technical Details

- Framework: {framework}
- Responsive: {options.get('responsive', True)}
- Include CMS: {options.get('include_cms', False)}
- Template: {options.get('template', 'modern')}

## Getting Started

### Vanilla HTML/CSS/JS

Simply open the `index.html` file in a web browser to view the website.

### React

To run the React website:

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

3. Build for production:
   ```
   npm run build
   ```

### Vue

To run the Vue website:

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm run serve
   ```

3. Build for production:
   ```
   npm run build
   ```

## Project Structure

- `/` - Root directory
- `/css` - CSS files (Vanilla only)
- `/js` - JavaScript files (Vanilla only)
- `/assets` - Images and other assets
- `/src` - Source files (React/Vue only)
- `/public` - Public files (React/Vue only)

## Generated at

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return readme
    
    def get_project(self, project_id):
        """Get details of a specific project"""
        if project_id in self.active_projects:
            return self.active_projects[project_id]
        
        # Check project history
        for project in self.project_history:
            if project["project_id"] == project_id:
                return project
        
        return None
    
    def get_project_history(self, limit=10):
        """Get recent project history"""
        return self.project_history[-limit:] if self.project_history else []
