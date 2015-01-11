bl_info = {
    "name": "Animation Markers Exporter For Urho3D",
    "author": "codingmonkey",
    "category": "Object",
    "blender": (2, 73, 1)   
}

import bpy
import os
import struct
import sys
import mathutils
from math import radians
from bpy.props import (BoolProperty)

          
class MarkersExporter(bpy.types.Operator):
    bl_idname = "object.markersexporter"   # unique identifier for buttons and menu items to reference.
    bl_label = "Urho3D Markers Create"     # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    normalizeMarkers = BoolProperty( name="Normalize markers", description="Normalize markers", default=False )
   
    def SaveLocalActionMarkes(self, context):
        
        print ("Actions count:", len(bpy.data.actions));
        fps = context.scene.render.fps
        print ("render fps:{0}".format(fps))
        
        
        
        
        for i, action in enumerate(bpy.data.actions):
            print ("index: {0} action name: {1} have {2} markers".format(i, action.name, len(action.pose_markers)))
            print ("frame range {0} to {1}".format(action.frame_range[0], action.frame_range[1]))
            print ("action len {0}".format(action.frame_range[1] - action.frame_range[0]))
            startFrame =  action.frame_range[0]
            endFrame = action.frame_range[1] 
            lenAction = endFrame - startFrame
            
            isThisActionHasMarkers = len(action.pose_markers)
            
            if (isThisActionHasMarkers):
                # markers write
                file = open(action.name + ".xml", 'wt')
                file.write("<animation>\n")
                
                for i, marker in enumerate(action.pose_markers):
                    if (self.normalizeMarkers == False):
                        print ("marker index: {0} frame: {1} name: {2}".format(i, marker.frame, marker.name))
                        file.write('    <trigger time="{0:.2f}" type="String" value="{1}" />\n'.format(marker.frame / fps, marker.name))
                    else:
                        print ("marker index: {0} normalizedtime: {1} name: {2}".format(i, marker.frame / lenAction, marker.name))
                        file.write('    <trigger normalizedtime="{0:.2f}" type="String" value="{1}" />\n'.format(marker.frame / lenAction, marker.name))
                        
            
                file.write("</animation>")                 
                file.close()
            
    def SaveGlobalSceneMarkers(self, context):
        isSceneHasMarkers = len(context.scene.timeline_markers)  
        scene = context.scene
        fps = scene.render.fps
        lenScene = scene.frame_end
        
        if (isSceneHasMarkers):
            file = open(scene.name + "_global_markers.xml", 'wt')
            file.write("<animation>\n")
            
            for i, marker in enumerate(scene.timeline_markers):
                if (self.normalizeMarkers == False):
                    file.write('    <trigger time="{0:.2f}" type="String" value="{1}" />\n'.format(marker.frame / fps, marker.name))
                else:
                    file.write('    <trigger normalizedtime="{0:.2f}" type="String" value="{1}" />\n'.format(marker.frame / lenScene, marker.name))
                    
                        
            file.write("</animation>")                 
            file.close()
                
            
        
                      
    def execute(self, context):
        self.SaveLocalActionMarkes(context)
        self.SaveGlobalSceneMarkers(context)
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MarkersExporter.bl_idname)

def register():
    bpy.utils.register_class(MarkersExporter)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(MarkersExporter)