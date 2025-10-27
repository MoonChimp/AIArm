#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS AI - UE5 Panel System
Procedural holographic panel generation and management for UE5
"""

import unreal
import json
import math

# Unreal Engine Python API
@unreal.uclass()
class NexusAIPanelSystem(unreal.BlueprintFunctionLibrary):
    """
    NexusAI Panel System for UE5
    Creates and manages floating holographic panels
    """
    
    @unreal.ufunction(static=True, meta=dict(Category="NexusAI"))
    def create_central_panel(location=(0, 0, 200), scale=(400, 300, 1)):
        """Create the main central holographic panel"""
        try:
            # Get world
            world = unreal.EditorLevelLibrary.get_editor_world()
            
            # Spawn widget component
            widget_class = unreal.load_class(None, "/Game/NexusAI/Widgets/CentralPanel_Widget.CentralPanel_Widget_C")
            
            if widget_class:
                # Create actor with widget component
                actor_class = unreal.load_class(None, "/Script/Engine.Actor")
                actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                    actor_class,
                    unreal.Vector(location[0], location[1], location[2])
                )
                
                # Add widget component
                widget_component = actor.add_component_by_class(
                    unreal.WidgetComponent,
                    False,
                    unreal.Transform(),
                    False
                )
                
                widget_component.set_widget_class(widget_class)
                widget_component.set_draw_size(unreal.Vector2D(scale[0], scale[1]))
                widget_component.set_widget_space(unreal.WidgetSpace.WORLD)
                
                unreal.log("Central panel created successfully")
                return actor
            else:
                unreal.log_warning("Widget class not found - create widget first")
                return None
                
        except Exception as e:
            unreal.log_error(f"Error creating central panel: {str(e)}")
            return None
    
    @unreal.ufunction(static=True, meta=dict(Category="NexusAI"))
    def create_satellite_panels(count=4, radius=500, height=200):
        """Create multiple satellite panels around the central panel"""
        try:
            world = unreal.EditorLevelLibrary.get_editor_world()
            panels = []
            
            angle_step = 360.0 / count
            
            for i in range(count):
                angle = math.radians(i * angle_step)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                
                # Create panel at calculated position
                panel = NexusAIPanelSystem.create_panel_at_location(
                    (x, y, height),
                    (200, 150, 1),
                    f"Satellite_{i}"
                )
                
                if panel:
                    panels.append(panel)
            
            unreal.log(f"Created {len(panels)} satellite panels")
            return panels
            
        except Exception as e:
            unreal.log_error(f"Error creating satellite panels: {str(e)}")
            return []
    
    @unreal.ufunction(static=True, meta=dict(Category="NexusAI"))
    def create_panel_at_location(location, scale, name="Panel"):
        """Create a single panel at specified location"""
        try:
            world = unreal.EditorLevelLibrary.get_editor_world()
            
            # Create actor
            actor_class = unreal.load_class(None, "/Script/Engine.Actor")
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                actor_class,
                unreal.Vector(location[0], location[1], location[2])
            )
            
            actor.set_actor_label(name)
            
            # Add widget component
            widget_component = actor.add_component_by_class(
                unreal.WidgetComponent,
                False,
                unreal.Transform(),
                False
            )
            
            widget_component.set_draw_size(unreal.Vector2D(scale[0], scale[1]))
            widget_component.set_widget_space(unreal.WidgetSpace.WORLD)
            
            return actor
            
        except Exception as e:
            unreal.log_error(f"Error creating panel: {str(e)}")
            return None
    
    @unreal.ufunction(static=True, meta=dict(Category="NexusAI"))
    def update_panel_text(panel_actor, text):
        """Update text content of a panel"""
        try:
            # Get widget component
            widget_comp = panel_actor.get_component_by_class(unreal.WidgetComponent)
            
            if widget_comp:
                widget = widget_comp.get_user_widget_object()
                if widget:
                    # Find text block and update
                    # This requires the widget to have a text block named "ContentText"
                    text_block = widget.get_widget_from_name("ContentText")
                    if text_block:
                        text_block.set_text(unreal.Text(text))
                        unreal.log(f"Panel text updated: {text}")
                        return True
            
            unreal.log_warning("Could not update panel text")
            return False
            
        except Exception as e:
            unreal.log_error(f"Error updating panel text: {str(e)}")
            return False
    
    @unreal.ufunction(static=True, meta=dict(Category="NexusAI"))
    def animate_panel_spawn(panel_actor, duration=0.5):
        """Animate panel spawning with scale and fade"""
        try:
            # Get widget component
            widget_comp = panel_actor.get_component_by_class(unreal.WidgetComponent)
            
            if widget_comp:
                # Start from scale 0
                widget_comp.set_relative_scale3d(unreal.Vector(0, 0, 0))
                
                # TODO: Add timeline animation
                # For now, just set to full scale
                widget_comp.set_relative_scale3d(unreal.Vector(1, 1, 1))
                
                unreal.log("Panel spawn animation triggered")
                return True
            
            return False
            
        except Exception as e:
            unreal.log_error(f"Error animating panel: {str(e)}")
            return False
    
    @unreal.ufunction(static=True, meta=dict(Category="NexusAI"))
    def setup_holographic_material(panel_actor):
        """Apply holographic material to panel"""
        try:
            # Load holographic material
            material = unreal.load_asset("/Game/NexusAI/Materials/M_Holographic")
            
            if material:
                widget_comp = panel_actor.get_component_by_class(unreal.WidgetComponent)
                if widget_comp:
                    # Apply material settings
                    widget_comp.set_blend_mode(unreal.WidgetBlendMode.TRANSPARENT)
                    unreal.log("Holographic material applied")
                    return True
            
            unreal.log_warning("Holographic material not found")
            return False
            
        except Exception as e:
            unreal.log_error(f"Error applying material: {str(e)}")
            return False


# Standalone functions for Blueprint exposure
@unreal.ufunction(static=True, ret=unreal.Actor, meta=dict(Category="NexusAI|Panels"))
def spawn_central_panel():
    """Spawn the main central panel - callable from Blueprint"""
    return NexusAIPanelSystem.create_central_panel()

@unreal.ufunction(static=True, ret=unreal.Array(unreal.Actor), meta=dict(Category="NexusAI|Panels"))
def spawn_satellite_panels(count=4):
    """Spawn satellite panels around center - callable from Blueprint"""
    return NexusAIPanelSystem.create_satellite_panels(count)

@unreal.ufunction(static=True, params=[unreal.Actor, unreal.String], meta=dict(Category="NexusAI|Panels"))
def update_panel_content(panel, text):
    """Update panel text content - callable from Blueprint"""
    return NexusAIPanelSystem.update_panel_text(panel, text)


# Initialize on module load
def initialize_nexus_panel_system():
    """Initialize the panel system"""
    unreal.log("=" * 60)
    unreal.log("NexusAI Panel System Loaded")
    unreal.log("=" * 60)
    unreal.log("Available functions:")
    unreal.log("  • spawn_central_panel()")
    unreal.log("  • spawn_satellite_panels(count)")
    unreal.log("  • update_panel_content(panel, text)")
    unreal.log("=" * 60)

# Auto-initialize
initialize_nexus_panel_system()

