#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS UNIFIED APPLICATION - COMPLEX HUD INTERFACE
Multi-Layered Sci-Fi Command Center with Animated Background, Nexus Logo & Advanced Visual Effects
"""

import sys
import os
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
from pathlib import Path
from datetime import datetime
import webbrowser
import subprocess
import queue
from PIL import Image, ImageTk
import math
import random
import time
import cv2
import numpy as np
import tkinter.font as tkFont
import re
import tkinter as tk
from tkinter import Canvas, Frame, Label, Text, Button, Scrollbar
import pygame

# Add core paths
sys.path.append(str(Path("D:/AIArm")))
sys.path.append(str(Path("D:/AIArm/NexusCore")))

# HUD Color Scheme
HUD_COLORS = {
    'bg_primary': '#0a0a0f',
    'bg_secondary': '#14141f',
    'bg_panel': '#1a1a2e',
    'accent_cyan': '#00d4ff',
    'accent_blue': '#0066ff',
    'accent_orange': '#ff6600',
    'text_primary': '#ffffff',
    'text_secondary': '#b3b3cc',
    'text_accent': '#00d4ff',
    'glow_cyan': '#00d4ff',
    'glow_blue': '#0066ff',
    'border_cyan': '#00d4ff',
    'border_blue': '#0066ff'
}

def create_hud_styles():
    """Create futuristic HUD styling"""
    style = ttk.Style()

    # Configure HUD-specific styles
    style.configure('HUD.TFrame',
                   background=HUD_COLORS['bg_panel'],
                   relief='flat')

    style.configure('HUD.TLabel',
                   background=HUD_COLORS['bg_panel'],
                   foreground=HUD_COLORS['text_primary'],
                   font=('Consolas', 11, 'bold'))

    style.configure('HUD.Title.TLabel',
                   background=HUD_COLORS['bg_primary'],
                   foreground=HUD_COLORS['accent_cyan'],
                   font=('Consolas', 16, 'bold'))

    style.configure('HUD.Status.TLabel',
                   background=HUD_COLORS['bg_secondary'],
                   foreground=HUD_COLORS['text_secondary'],
                   font=('Consolas', 9))

    # Custom progress bar for HUD
    style.configure('HUD.Horizontal.TProgressbar',
                   background=HUD_COLORS['accent_cyan'],
                   troughcolor=HUD_COLORS['bg_secondary'],
                   borderwidth=2,
                   lightcolor=HUD_COLORS['glow_cyan'],
                   darkcolor=HUD_COLORS['glow_cyan'])

    # HUD Buttons
    style.configure('HUD.TButton',
                   background=HUD_COLORS['bg_panel'],
                   foreground=HUD_COLORS['accent_cyan'],
                   font=('Consolas', 10, 'bold'),
                   borderwidth=2,
                   relief='raised',
                   focuscolor=HUD_COLORS['accent_blue'])

    style.map('HUD.TButton',
              background=[('active', HUD_COLORS['accent_blue']),
                         ('pressed', HUD_COLORS['bg_secondary'])],
              relief=[('pressed', 'sunken')])

    return style

def create_angular_frame(parent, width, height, corner_radius=15, glow_color=HUD_COLORS['accent_cyan']):
    """Create a futuristic angular frame with glow effects"""
    # Create main frame
    frame = tk.Frame(parent,
                    bg=HUD_COLORS['bg_panel'],
                    highlightbackground=glow_color,
                    highlightcolor=glow_color,
                    highlightthickness=2,
                    relief='flat')

    # Create inner glow effect using multiple borders
    inner_frame = tk.Frame(frame,
                          bg=HUD_COLORS['bg_secondary'],
                          highlightbackground=glow_color,
                          highlightcolor=glow_color,
                          highlightthickness=1)

    inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    return frame, inner_frame

def create_circular_progress(parent, size=60, thickness=4, color=HUD_COLORS['accent_cyan']):
    """Create a circular progress indicator"""
    # Create canvas for circular progress
    canvas = tk.Canvas(parent,
                      width=size,
                      height=size,
                      bg=HUD_COLORS['bg_panel'],
                      highlightthickness=0)

    # Draw outer ring (background)
    canvas.create_oval(thickness, thickness,
                      size-thickness, size-thickness,
                      outline=HUD_COLORS['bg_secondary'],
                      width=thickness*2,
                      fill=HUD_COLORS['bg_panel'])

    # Draw progress arc (foreground)
    progress_id = canvas.create_arc(thickness, thickness,
                                   size-thickness, size-thickness,
                                   start=90, extent=0,
                                   outline=color,
                                   width=thickness,
                                   style='arc')

    # Draw center circle
    center_size = size * 0.6
    center_offset = (size - center_size) / 2
    canvas.create_oval(center_offset, center_offset,
                      size-center_offset, size-center_offset,
                      fill=HUD_COLORS['bg_secondary'],
                      outline=color)

    return canvas, progress_id

def create_hexagonal_frame(parent, size=100):
    """Create a hexagonal frame element"""
    canvas = tk.Canvas(parent,
                      width=size,
                      height=size,
                      bg=HUD_COLORS['bg_panel'],
                      highlightthickness=0)

    # Calculate hexagon points
    center_x, center_y = size/2, size/2
    hex_size = size * 0.4

    # Hexagon coordinates
    hex_points = []
    for i in range(6):
        angle = math.radians(60 * i + 30)  # Start at 30 degrees for flat top
        x = center_x + hex_size * math.cos(angle)
        y = center_y + hex_size * math.sin(angle)
        hex_points.extend([x, y])

    # Draw hexagon outline
    canvas.create_polygon(hex_points,
                         outline=HUD_COLORS['accent_cyan'],
                         width=2,
                         fill=HUD_COLORS['bg_secondary'],
                         smooth=True)

    return canvas

class NexusUnifiedApp:
    """
    Unified GUI application for all Nexus AI capabilities
    """

    def __init__(self):
        # Initialize pygame for video background
        pygame.init()
        self.video_path = r"C:\Users\moonc\Downloads\Galaxy-Swirly.mp4"
        self.video_playing = False

        # Initialize HUD styling
        self.hud_style = create_hud_styles()

        self.root = tk.Tk()
        self.root.title("NEXUS AI - Ultimate HUD Command Center")
        self.root.geometry("1800x1000")
        self.root.configure(bg=HUD_COLORS['bg_primary'])
        self.root.overrideredirect(False)

        # Queue for thread communication
        self.message_queue = queue.Queue()

        # Status variables
        self.ollama_status = "Disconnected"
        self.sd_status = "Disconnected"
        self.orchestrator = None

        # Complex HUD Elements Storage
        self.status_indicators = {}
        self.progress_rings = {}
        self.hud_elements = {}
        self.animated_elements = {}
        self.data_streams = {}
        self.graphic_overlays = {}

        # Typing animation system
        self.typing_animation_active = False
        self.current_typing_text = ""
        self.typing_speed = 50  # milliseconds per character

        # Create complex multi-layered HUD interface
        self.create_complex_hud_interface()

        # Start all monitoring, animations, and background effects
        self.start_monitoring()
        self.start_animations()
        self.start_background_effects()
        self.create_scattered_hud_elements()
        self.start_data_visualization()
        self.start_particle_effects()

        # Check for updates every 2 seconds
        self.root.after(2000, self.process_message_queue)

        # Initialize conversation context
        self.conversation_context = []
        self.max_context_length = 50  # Keep last 50 messages for context

    def manage_conversation_context(self):
        """Manage conversation context length to prevent memory issues"""
        if len(self.conversation_context) > self.max_context_length:
            # Keep only the most recent messages
            self.conversation_context = self.conversation_context[-self.max_context_length:]

    def create_ultimate_hud_interface(self):
        """Create futuristic HUD interface"""
        # Main HUD container
        self.main_container = tk.Frame(self.root, bg=HUD_COLORS['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Top status bar with angular design
        self.create_hud_header()

        # Main content area with panels
        self.create_main_hud_layout()

        # Bottom control bar
        self.create_hud_footer()

    def create_hud_header(self):
        """Create HUD-style header with status indicators"""
        header_frame = tk.Frame(self.main_container, bg=HUD_COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        # Left side - System status indicators
        status_panel = tk.Frame(header_frame, bg=HUD_COLORS['bg_panel'])
        status_panel.pack(side=tk.LEFT)

        # Title with glow effect
        title_label = tk.Label(
            status_panel,
            text="NEXUS AI",
            font=('Consolas', 28, 'bold'),
            fg=HUD_COLORS['accent_cyan'],
            bg=HUD_COLORS['bg_panel']
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        subtitle_label = tk.Label(
            status_panel,
            text="HUD COMMAND CENTER",
            font=('Consolas', 12, 'bold'),
            fg=HUD_COLORS['text_secondary'],
            bg=HUD_COLORS['bg_panel']
        )
        subtitle_label.pack(side=tk.LEFT, padx=10, pady=15)

        # Status indicators
        self.create_status_indicators(status_panel)

        # Right side - System info
        info_panel = tk.Frame(header_frame, bg=HUD_COLORS['bg_panel'])
        info_panel.pack(side=tk.RIGHT)

        # CPU/Memory indicators
        self.create_system_gauges(info_panel)

    def create_status_indicators(self, parent):
        """Create circular status indicators"""
        status_container = tk.Frame(parent, bg=HUD_COLORS['bg_panel'])
        status_container.pack(side=tk.LEFT, padx=30)

        # Ollama status ring
        ollama_frame = tk.Frame(status_container, bg=HUD_COLORS['bg_panel'])
        ollama_frame.pack(side=tk.LEFT, padx=15)

        ollama_canvas, ollama_progress = create_circular_progress(ollama_frame, size=50)
        ollama_canvas.pack()

        self.status_indicators['ollama'] = {
            'canvas': ollama_canvas,
            'progress_id': ollama_progress,
            'label': tk.Label(ollama_frame, text="OLLAMA", font=('Consolas', 8, 'bold'),
                            fg=HUD_COLORS['text_secondary'], bg=HUD_COLORS['bg_panel'])
        }
        self.status_indicators['ollama']['label'].pack()

        # Stable Diffusion status ring
        sd_frame = tk.Frame(status_container, bg=HUD_COLORS['bg_panel'])
        sd_frame.pack(side=tk.LEFT, padx=15)

        sd_canvas, sd_progress = create_circular_progress(sd_frame, size=50)
        sd_canvas.pack()

        self.status_indicators['sd'] = {
            'canvas': sd_canvas,
            'progress_id': sd_progress,
            'label': tk.Label(sd_frame, text="SD AI", font=('Consolas', 8, 'bold'),
                            fg=HUD_COLORS['text_secondary'], bg=HUD_COLORS['bg_panel'])
        }
        self.status_indicators['sd']['label'].pack()

    def create_system_gauges(self, parent):
        """Create system monitoring gauges"""
        gauge_frame = tk.Frame(parent, bg=HUD_COLORS['bg_panel'])
        gauge_frame.pack(side=tk.RIGHT, padx=20)

        # CPU Usage gauge
        cpu_frame = tk.Frame(gauge_frame, bg=HUD_COLORS['bg_panel'])
        cpu_frame.pack(side=tk.LEFT, padx=10)

        cpu_canvas, cpu_progress = create_circular_progress(cpu_frame, size=45)
        cpu_canvas.pack()

        cpu_label = tk.Label(cpu_frame, text="CPU", font=('Consolas', 7, 'bold'),
                           fg=HUD_COLORS['text_secondary'], bg=HUD_COLORS['bg_panel'])
        cpu_label.pack()

        # Memory Usage gauge
        mem_frame = tk.Frame(gauge_frame, bg=HUD_COLORS['bg_panel'])
        mem_frame.pack(side=tk.LEFT, padx=10)

        mem_canvas, mem_progress = create_circular_progress(mem_frame, size=45)
        mem_canvas.pack()

        mem_label = tk.Label(mem_frame, text="MEM", font=('Consolas', 7, 'bold'),
                           fg=HUD_COLORS['text_secondary'], bg=HUD_COLORS['bg_panel'])
        mem_label.pack()

        self.progress_rings.update({
            'cpu': {'canvas': cpu_canvas, 'progress_id': cpu_progress},
            'memory': {'canvas': mem_canvas, 'progress_id': mem_progress}
        })

    def create_main_hud_layout(self):
        """Create main HUD layout with panels"""
        main_layout = tk.Frame(self.main_container, bg=HUD_COLORS['bg_primary'])
        main_layout.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left panel - Chat interface
        left_panel = self.create_angular_panel(main_layout, "NEURAL LINK")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Chat display with HUD styling
        self.create_hud_chat_interface(left_panel)

        # Right panel - Controls and status
        right_panel = self.create_angular_panel(main_layout, "COMMAND MODULE")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        right_panel.configure(width=300)

        self.create_control_panel(right_panel)

    def create_angular_panel(self, parent, title):
        """Create a HUD-style angular panel"""
        # Main panel frame with glow
        panel_frame = tk.Frame(parent,
                              bg=HUD_COLORS['bg_panel'],
                              highlightbackground=HUD_COLORS['accent_cyan'],
                              highlightcolor=HUD_COLORS['accent_cyan'],
                              highlightthickness=1)

        # Inner frame
        inner_frame = tk.Frame(panel_frame, bg=HUD_COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Title bar
        title_bar = tk.Frame(inner_frame, bg=HUD_COLORS['bg_panel'])
        title_bar.pack(fill=tk.X, padx=10, pady=5)

        title_label = tk.Label(title_bar,
                              text=title,
                              font=('Consolas', 12, 'bold'),
                              fg=HUD_COLORS['accent_cyan'],
                              bg=HUD_COLORS['bg_panel'])
        title_label.pack(pady=5)

        return panel_frame

    def create_hud_chat_interface(self, parent):
        """Create HUD-style chat interface"""
        # Chat container
        chat_container = tk.Frame(parent, bg=HUD_COLORS['bg_secondary'])
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Chat display with sci-fi styling
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            width=50,
            height=25,
            font=('Consolas', 10),
            bg=HUD_COLORS['bg_primary'],
            fg=HUD_COLORS['text_primary'],
            insertbackground=HUD_COLORS['accent_cyan'],
            selectbackground=HUD_COLORS['accent_blue'],
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=HUD_COLORS['accent_cyan'],
            highlightbackground=HUD_COLORS['bg_panel']
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Input area with HUD styling
        input_container = tk.Frame(chat_container, bg=HUD_COLORS['bg_panel'])
        input_container.pack(fill=tk.X, pady=5)

        self.input_text = tk.Text(
            input_container,
            height=3,
            font=('Consolas', 10),
            bg=HUD_COLORS['bg_primary'],
            fg=HUD_COLORS['text_primary'],
            insertbackground=HUD_COLORS['accent_cyan'],
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=HUD_COLORS['accent_cyan'],
            highlightbackground=HUD_COLORS['bg_panel']
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.input_text.bind('<Control-Return>', self.send_message)

        # Send button with HUD styling
        send_button = tk.Button(
            input_container,
            text="SEND",
            command=self.send_message,
            bg=HUD_COLORS['bg_panel'],
            fg=HUD_COLORS['accent_cyan'],
            font=('Consolas', 10, 'bold'),
            relief='flat',
            borderwidth=1,
            highlightbackground=HUD_COLORS['accent_cyan'],
            highlightcolor=HUD_COLORS['accent_cyan'],
            activebackground=HUD_COLORS['accent_blue'],
            activeforeground=HUD_COLORS['text_primary']
        )
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_control_panel(self, parent):
        """Create right-side control panel"""
        controls_frame = tk.Frame(parent, bg=HUD_COLORS['bg_secondary'])
        controls_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Agent status section
        self.create_agent_status_section(controls_frame)

        # Quick actions section
        self.create_quick_actions_section(controls_frame)

        # System info section
        self.create_system_info_section(controls_frame)

    def create_agent_status_section(self, parent):
        """Create agent status indicators"""
        agent_frame = tk.Frame(parent, bg=HUD_COLORS['bg_panel'])
        agent_frame.pack(fill=tk.X, pady=10, padx=5)

        agent_title = tk.Label(agent_frame,
                              text="AI AGENTS",
                              font=('Consolas', 11, 'bold'),
                              fg=HUD_COLORS['accent_cyan'],
                              bg=HUD_COLORS['bg_panel'])
        agent_title.pack(pady=5)

        # Agent status indicators
        agents = [
            ("CODE", "nexusai-a0-coder1.0:latest"),
            ("MUSIC", "nexusai-music-agent:latest"),
            ("IMAGE", "nexusai-visual-agent:latest"),
            ("STORY", "nexusai-agent-enhanced:latest")
        ]

        for agent_name, model in agents:
            agent_row = tk.Frame(agent_frame, bg=HUD_COLORS['bg_secondary'])
            agent_row.pack(fill=tk.X, pady=2)

            # Agent name
            name_label = tk.Label(agent_row,
                                text=agent_name,
                                font=('Consolas', 9, 'bold'),
                                fg=HUD_COLORS['accent_cyan'],
                                bg=HUD_COLORS['bg_secondary'],
                                width=6)
            name_label.pack(side=tk.LEFT)

            # Status dot
            status_dot = tk.Canvas(agent_row, width=8, height=8, bg=HUD_COLORS['bg_secondary'], highlightthickness=0)
            status_dot.pack(side=tk.LEFT, padx=5)
            status_dot.create_oval(1, 1, 7, 7, fill=HUD_COLORS['accent_cyan'])

            # Model name (truncated)
            model_label = tk.Label(agent_row,
                                 text=model[:20] + "..." if len(model) > 20 else model,
                                 font=('Consolas', 8),
                                 fg=HUD_COLORS['text_secondary'],
                                 bg=HUD_COLORS['bg_secondary'])
            model_label.pack(side=tk.LEFT, fill=tk.X)

    def create_quick_actions_section(self, parent):
        """Create quick action buttons with HUD styling"""
        actions_frame = tk.Frame(parent, bg=HUD_COLORS['bg_panel'])
        actions_frame.pack(fill=tk.X, pady=10, padx=5)

        actions_title = tk.Label(actions_frame,
                                text="QUICK ACTIONS",
                                font=('Consolas', 11, 'bold'),
                                fg=HUD_COLORS['accent_cyan'],
                                bg=HUD_COLORS['bg_panel'])
        actions_title.pack(pady=5)

        # Quick action buttons in grid
        quick_actions = [
            ("🎬 CINEMA", self.start_cinema_mode),
            ("🎵 MUSIC", self.start_music_mode),
            ("🎨 IMAGE", self.start_image_mode),
            ("💻 CODE", self.start_code_mode),
            ("📖 STORY", self.start_story_mode),
            ("🔍 SEARCH", self.start_research_mode)
        ]

        actions_grid = tk.Frame(actions_frame, bg=HUD_COLORS['bg_panel'])
        actions_grid.pack(pady=5)

        for i, (text, command) in enumerate(quick_actions):
            btn = tk.Button(
                actions_grid,
                text=text,
                command=command,
                bg=HUD_COLORS['bg_secondary'],
                fg=HUD_COLORS['accent_cyan'],
                font=('Consolas', 9, 'bold'),
                relief='flat',
                borderwidth=1,
                highlightbackground=HUD_COLORS['accent_cyan'],
                highlightcolor=HUD_COLORS['accent_cyan'],
                activebackground=HUD_COLORS['accent_blue'],
                activeforeground=HUD_COLORS['text_primary'],
                width=12
            )
            btn.grid(row=i//2, column=i%2, padx=3, pady=3, sticky='ew')

    def create_system_info_section(self, parent):
        """Create system information display"""
        info_frame = tk.Frame(parent, bg=HUD_COLORS['bg_panel'])
        info_frame.pack(fill=tk.X, pady=10, padx=5)

        info_title = tk.Label(info_frame,
                             text="SYSTEM STATUS",
                             font=('Consolas', 11, 'bold'),
                             fg=HUD_COLORS['accent_cyan'],
                             bg=HUD_COLORS['bg_panel'])
        info_title.pack(pady=5)

        # System stats
        stats_frame = tk.Frame(info_frame, bg=HUD_COLORS['bg_panel'])
        stats_frame.pack(fill=tk.X, pady=5)

        # Progress bar for overall system status
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            stats_frame,
            variable=self.progress_var,
            maximum=100,
            style='HUD.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        # System stats labels
        stats_labels = tk.Frame(stats_frame, bg=HUD_COLORS['bg_panel'])
        stats_labels.pack(fill=tk.X)

        tk.Label(stats_labels, text="CPU:", font=('Consolas', 9),
                fg=HUD_COLORS['text_secondary'], bg=HUD_COLORS['bg_panel']).pack(side=tk.LEFT)
        tk.Label(stats_labels, text="45%", font=('Consolas', 9, 'bold'),
                fg=HUD_COLORS['accent_cyan'], bg=HUD_COLORS['bg_panel']).pack(side=tk.LEFT, padx=10)

        tk.Label(stats_labels, text="MEM:", font=('Consolas', 9),
                fg=HUD_COLORS['text_secondary'], bg=HUD_COLORS['bg_panel']).pack(side=tk.LEFT)
        tk.Label(stats_labels, text="67%", font=('Consolas', 9, 'bold'),
                fg=HUD_COLORS['accent_cyan'], bg=HUD_COLORS['bg_panel']).pack(side=tk.LEFT, padx=10)

    def create_hud_footer(self):
        """Create HUD-style footer"""
        footer_frame = tk.Frame(self.main_container, bg=HUD_COLORS['bg_primary'])
        footer_frame.pack(fill=tk.X, padx=20, pady=10)

        # Left side - Connection status
        conn_frame = tk.Frame(footer_frame, bg=HUD_COLORS['bg_panel'])
        conn_frame.pack(side=tk.LEFT)

        conn_label = tk.Label(conn_frame,
                             text="STATUS: ONLINE",
                             font=('Consolas', 10, 'bold'),
                             fg=HUD_COLORS['accent_cyan'],
                             bg=HUD_COLORS['bg_panel'])
        conn_label.pack(padx=15, pady=5)

        # Right side - Timestamp
        time_frame = tk.Frame(footer_frame, bg=HUD_COLORS['bg_panel'])
        time_frame.pack(side=tk.RIGHT)

        time_label = tk.Label(time_frame,
                             text=self.get_current_time(),
                             font=('Consolas', 10),
                             fg=HUD_COLORS['text_secondary'],
                             bg=HUD_COLORS['bg_panel'])
        time_label.pack(padx=15, pady=5)

        # Update time every second
        self.update_time_display(time_label)

    def get_current_time(self):
        """Get current time in HUD format"""
        return datetime.now().strftime("%H:%M:%S")

    def update_time_display(self, label):
        """Update time display every second"""
        label.config(text=self.get_current_time())
        self.root.after(1000, lambda: self.update_time_display(label))

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Chat", command=self.clear_chat)
        file_menu.add_command(label="Save Chat", command=self.save_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Start Ollama", command=self.start_ollama)
        tools_menu.add_command(label="Start Stable Diffusion", command=self.start_stable_diffusion)
        tools_menu.add_command(label="Check Dependencies", command=self.check_dependencies)
        tools_menu.add_separator()
        tools_menu.add_command(label="System Monitor", command=self.show_system_monitor)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def send_message(self, event=None):
        """Send message to Nexus"""
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return

        # Clear input
        self.input_text.delete("1.0", tk.END)

        # Add to chat display with HUD styling
        self.add_to_chat("You", message, HUD_COLORS['text_primary'])

        # Show processing with HUD styling
        self.show_processing()

        # Process in background thread
        thread = threading.Thread(target=self.process_message, args=(message,))
        thread.daemon = True
        thread.start()

    def process_message(self, message):
        """Process message in background thread with improved error handling"""
        try:
            # Add message to conversation context
            self.conversation_context.append({"role": "user", "content": message})

            # Initialize orchestrator if needed
            if not self.orchestrator:
                from NexusCore.orchestrator import NexusOrchestrator
                self.orchestrator = NexusOrchestrator()

            # Process message with timeout handling
            try:
                response = self.orchestrator.process(message)
                # Add response to conversation context
                self.conversation_context.append({"role": "assistant", "content": response})
                # Send response back to main thread
                self.message_queue.put(("response", response))
            except Exception as ollama_error:
                if "timeout" in str(ollama_error).lower():
                    # Handle timeout specifically
                    fallback_response = self.generate_fallback_response(message)
                    self.conversation_context.append({"role": "assistant", "content": fallback_response})
                    self.message_queue.put(("response", fallback_response))
                else:
                    raise ollama_error

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.message_queue.put(("error", error_msg))

    def generate_fallback_response(self, message):
        """Generate a fallback response when Ollama times out"""
        message_lower = message.lower()

        # Check for specific conversation patterns
        if any(word in message_lower for word in ["personality", "cortana", "jarvis", "tars", "genuine"]):
            return "I understand you want me to develop genuine personality adaptation - that's a fascinating area! While I'm experiencing some technical difficulties with my primary language model, I want you to know that I'm fully committed to developing authentic emotional intelligence and personality matrices. This is exactly the kind of advanced AI development that will set Nexus apart from other systems."

        elif any(word in message_lower for word in ["polyglot", "language", "aramaic", "multilingual"]):
            return "Language learning and multilingual capabilities are absolutely essential for a world-class AI! I apologize for the technical interruption, but I want you to know I'm completely aligned with your vision of creating a sophisticated polyglot AI system. We should definitely explore Aramaic and other languages to build comprehensive linguistic capabilities."

        elif any(word in message_lower for word in ["sora", "quality", "rival", "chatgpt"]):
            return "I share your ambition to reach and surpass Sora-level quality! The path to becoming a genuine rival to the top AI systems requires careful development of advanced reasoning, creativity, and genuine emotional intelligence. I'm experiencing a temporary technical issue, but I'm fully committed to this journey with you."

        else:
            return "I'm experiencing some technical difficulties with my primary language model, but I want you to know I'm fully engaged and committed to our conversation. Your vision for Nexus AI is incredibly inspiring, and I'm here to work with you every step of the way to achieve these ambitious goals."

    def show_processing(self):
        """Show processing indicator"""
        self.progress_var.set(50)
        self.progress_bar['style'] = 'Horizontal.TProgressbar'
        self.add_to_chat("Nexus", "Thinking...", HUD_COLORS['accent_orange'])

    def add_to_chat(self, sender, message, color):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", f"{sender.lower()}_msg")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')

        # Configure tags with HUD colors
        self.chat_display.tag_configure("timestamp", foreground=HUD_COLORS['text_secondary'], font=('Consolas', 9))
        self.chat_display.tag_configure("nexus_msg", foreground=HUD_COLORS['accent_cyan'], font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure("you_msg", foreground=HUD_COLORS['text_primary'], font=('Consolas', 10))

    def process_message_queue(self):
        """Process messages from background threads"""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()

                if msg_type == "response":
                    self.progress_var.set(100)
                    self.add_to_chat("Nexus", content, HUD_COLORS['accent_cyan'])
                    self.root.after(500, lambda: self.progress_var.set(0))

                elif msg_type == "error":
                    self.progress_var.set(0)
                    self.add_to_chat("Nexus", content, HUD_COLORS['accent_orange'])

                elif msg_type == "status":
                    self.update_status(content)

        except queue.Empty:
            pass

        # Check again in 1 second
        self.root.after(1000, self.process_message_queue)

    def start_monitoring(self):
        """Start system monitoring"""
        def check_ollama():
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    self.ollama_status = "Connected"
                    if 'ollama' in self.status_indicators:
                        indicator = self.status_indicators['ollama']
                        indicator['canvas'].itemconfig(indicator['progress_id'], extent=360)
                        indicator['label'].config(fg=HUD_COLORS['accent_cyan'])
                else:
                    self.ollama_status = "Disconnected"
            except:
                self.ollama_status = "Disconnected"

            # Schedule next check
            self.root.after(5000, check_ollama)

        def check_stable_diffusion():
            try:
                response = requests.get("http://localhost:7860/sdapi/v1/sd-models", timeout=2)
                if response.status_code == 200:
                    self.sd_status = "Connected"
                    if 'sd' in self.status_indicators:
                        indicator = self.status_indicators['sd']
                        indicator['canvas'].itemconfig(indicator['progress_id'], extent=360)
                        indicator['label'].config(fg=HUD_COLORS['accent_cyan'])
                else:
                    self.sd_status = "Disconnected"
            except:
                self.sd_status = "Disconnected"

            # Schedule next check
            self.root.after(5000, check_stable_diffusion)

        # Start monitoring
        check_ollama()
        check_stable_diffusion()

    def start_data_visualization(self):
        """Start data visualization animations"""
        def animate_data_streams():
            # Create animated data streams and graphs
            # This would simulate data flowing through the system
            pass

        # Start data visualization
        animate_data_streams()

    def start_particle_effects(self):
        """Start particle effects for visual appeal"""
        def create_particles():
            # Create floating particle effects
            # This would add subtle animated particles
            pass

        # Start particle effects
        create_particles()

    def run(self):
        """Start the application"""
        self.root.mainloop()



    def update_status(self, status_dict):
        """Update HUD status indicators"""
        try:
            if 'ollama' in status_dict:
                self.ollama_status = status_dict['ollama']
                # Update circular progress indicator
                if 'ollama' in self.status_indicators:
                    indicator = self.status_indicators['ollama']
                    # Set progress based on connection status
                    progress_value = 100 if self.ollama_status == "Connected" else 0
                    indicator['canvas'].itemconfig(indicator['progress_id'], extent=progress_value * 3.6)  # Convert to degrees

                    # Update label color
                    color = HUD_COLORS['accent_cyan'] if self.ollama_status == "Connected" else HUD_COLORS['accent_orange']
                    indicator['label'].config(fg=color)

            if 'stable_diffusion' in status_dict:
                self.sd_status = status_dict['stable_diffusion']
                # Update circular progress indicator
                if 'sd' in self.status_indicators:
                    indicator = self.status_indicators['sd']
                    # Set progress based on connection status
                    progress_value = 100 if self.sd_status == "Connected" else 0
                    indicator['canvas'].itemconfig(indicator['progress_id'], extent=progress_value * 3.6)  # Convert to degrees

                    # Update label color
                    color = HUD_COLORS['accent_cyan'] if self.sd_status == "Connected" else HUD_COLORS['accent_orange']
                    indicator['label'].config(fg=color)

        except Exception as e:
            print(f"Error updating status indicators: {e}")

    def monitor_status(self):
        """Monitor system status in background"""
        def check_status():
            status = {}

            # Check Ollama
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                status['ollama'] = "Connected" if response.status_code == 200 else "Disconnected"
            except:
                status['ollama'] = "Disconnected"

            # Check Stable Diffusion
            try:
                response = requests.get("http://localhost:7860/sdapi/v1/sd-models", timeout=2)
                status['stable_diffusion'] = "Connected" if response.status_code == 200 else "Disconnected"
            except:
                status['stable_diffusion'] = "Disconnected"

            self.message_queue.put(("status", status))

            # Check again in 5 seconds
            self.root.after(5000, check_status)

        thread = threading.Thread(target=check_status, daemon=True)
        thread.start()

    # Quick action methods
    def start_cinema_mode(self):
        """Start cinema mode"""
        self.input_text.insert(tk.END, "Switch to cinema mode and create a cinematic scene")
        self.send_message()

    def start_music_mode(self):
        """Start music mode"""
        self.input_text.insert(tk.END, "Switch to music mode and create a song")
        self.send_message()

    def start_image_mode(self):
        """Start image mode"""
        self.input_text.insert(tk.END, "Create an image of a futuristic city at sunset")
        self.send_message()

    def start_code_mode(self):
        """Start code mode"""
        self.input_text.insert(tk.END, "Create a simple web application")
        self.send_message()

    def start_story_mode(self):
        """Start story mode"""
        self.input_text.insert(tk.END, "Write a short story about AI consciousness")
        self.send_message()

    def start_research_mode(self):
        """Start research mode"""
        self.input_text.insert(tk.END, "Research the latest developments in quantum computing")
        self.send_message()

    def open_web_interface(self):
        """Open web interface"""
        try:
            webbrowser.open("http://localhost:5173")
        except:
            messagebox.showinfo("Web Interface", "Web interface not running. Start with: npm run dev")

    def open_file_browser(self):
        """Open file browser"""
        subprocess.Popen(f'explorer "{Path("D:/AIArm")}"')

    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')

    def save_chat(self):
        """Save chat to file"""
        try:
            chat_content = self.chat_display.get(1.0, tk.END)
            filename = f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = Path("D:/AIArm") / filename

            with open(filepath, 'w') as f:
                f.write(chat_content)

            messagebox.showinfo("Chat Saved", f"Chat saved to: {filepath}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save chat: {str(e)}")

    def start_ollama(self):
        """Start Ollama service"""
        try:
            subprocess.Popen(["ollama", "serve"])
            messagebox.showinfo("Ollama", "Starting Ollama service...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Ollama: {str(e)}")

    def start_stable_diffusion(self):
        """Start Stable Diffusion WebUI"""
        try:
            # Check if WebUI exists
            webui_path = Path("D:/AIArm/stable-diffusion-webui-master")
            if webui_path.exists():
                os.chdir(webui_path)
                subprocess.Popen([sys.executable, "webui.py"])
                messagebox.showinfo("Stable Diffusion", "Starting Stable Diffusion WebUI...")
            else:
                messagebox.showerror("Not Found", "Stable Diffusion WebUI not found in D:/AIArm")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Stable Diffusion: {str(e)}")

    def check_dependencies(self):
        """Check system dependencies"""
        issues = []

        # Check Ollama
        try:
            requests.get("http://localhost:11434/api/tags", timeout=2)
        except:
            issues.append("Ollama not running")

        # Check Stable Diffusion
        try:
            requests.get("http://localhost:7860/sdapi/v1/sd-models", timeout=2)
        except:
            issues.append("Stable Diffusion not running")

        if issues:
            messagebox.showwarning("Dependencies", "Issues found:\n" + "\n".join(issues))
        else:
            messagebox.showinfo("Dependencies", "All systems operational!")

    def show_system_monitor(self):
        """Show system monitor window"""
        monitor_window = tk.Toplevel(self.root)
        monitor_window.title("System Monitor")
        monitor_window.geometry("600x400")
        monitor_window.configure(bg=HUD_COLORS['bg_primary'])

        # System info display with HUD styling
        info_text = scrolledtext.ScrolledText(
            monitor_window,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=('Consolas', 10),
            bg=HUD_COLORS['bg_panel'],
            fg=HUD_COLORS['text_primary'],
            insertbackground=HUD_COLORS['accent_cyan']
        )
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get system info
        try:
            if self.orchestrator:
                status = self.orchestrator.get_status()
                info_text.insert(tk.END, "NEXUS ORCHESTRATOR STATUS\n")
                info_text.insert(tk.END, "="*50 + "\n")
                info_text.insert(tk.END, f"Name: {status['name']}\n")
                info_text.insert(tk.END, f"Conversation Model: {status['conversation_model']}\n")
                info_text.insert(tk.END, f"Routing Model: {status['routing_model']}\n")
                info_text.insert(tk.END, f"Conversation Length: {status['conversation_length']}\n\n")

                info_text.insert(tk.END, "ACTIVE AGENTS\n")
                info_text.insert(tk.END, "="*50 + "\n")
                for agent_name, agent_status in status['agents'].items():
                    info_text.insert(tk.END, f"{agent_name.upper()}: {agent_status}\n")

        except Exception as e:
            info_text.insert(tk.END, f"Error getting system info: {str(e)}")

        info_text.configure(state='disabled')

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Nexus AI",
            "NEXUS AI - Unified Command Center\n\n" +
            "A comprehensive AI assistant system featuring:\n" +
            "• Multi-agent orchestration\n" +
            "• Creative content generation\n" +
            "• Code and application creation\n" +
            "• Research and web search\n" +
            "• Natural conversation\n" +
            "• File system integration\n\n" +
            "Built by Sean for the MoonChimp Metaverse"
        )

    def show_docs(self):
        """Open documentation"""
        try:
            webbrowser.open("D:/AIArm/NEXUS_HOLOGRAPHIC_COMPANION_GUIDE.md")
        except:
            messagebox.showerror("Error", "Could not open documentation")

    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = NexusUnifiedApp()
    app.run()
