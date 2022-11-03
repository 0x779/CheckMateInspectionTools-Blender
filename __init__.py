# Very small add on to start from

bl_info = {
    "name" : "CheckMate Inspection Tools",
    "description" : "CheckMate Pro/Lite Inspection Tools for Blender",
    "author" : "0x779",
    "version" : (0, 1, 0),
    "blender" : (2, 80, 0),
    "location" : "View3D and Properties Panel",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "https://github.com/0x779/CheckMateInspectionTools-Blender",
    "category" : "3D View"
}

from re import S
import bpy, bmesh
from mathutils import Vector, Euler, kdtree
from bpy.props import (
                       PointerProperty,
                       EnumProperty,
                       FloatProperty,
                       IntProperty,
                       StringProperty,
                       )

from bpy.types import (
                       PropertyGroup,
                       )

defaultNamesKeywords = ['Cube.', 
                        'Sphere.',
                        'Plane.',
                        'Cylinder.',
                        'Cone.', 
                        'Torus.', 
                        ]

objectsTests = {
    "sceneObjects" : "sceneObjectsResult",
    "sceneGeometry" : "sceneGeometryResult",
    "sceneLights" : "sceneLightsResult",
    "sceneCameras" : "sceneCamerasResult",
    "sceneShapes" :  "sceneShapesResult"
}

geometryTests = {
    "sceneVertices" : "sceneVerticesResult",
    "sceneFaces" : "sceneFacesResult",
    "sceneQuads" : "sceneQuadsResult",
    "sceneTriangles" : "sceneTrianglesResult",
}

resettableTests = {
    "sceneObjects" : "sceneObjectsResult",
    "sceneGeometry" : "sceneGeometryResult",
    "sceneLights" : "sceneLightsResult",
    "sceneCameras" : "sceneCamerasResult",
    "sceneShapes" :  "sceneShapesResult",
    "sceneCollection" :  "sceneCollectionResult",
    "sceneDefaultNames" :  "sceneDefaultNamesResult",
    "sceneInvalidTransforms" :  "sceneInvalidTransformsResult",
    "sceneVertices" : "sceneVerticesResult",
    "sceneFaces" : "sceneFacesResult",
    "sceneQuads" : "sceneQuadsResult",
    "sceneTriangles" : "sceneTrianglesResult",
    "sceneTrianglesPercentage" : "sceneTrianglesPercentageResult",
    "sceneNgons" : "sceneNgonsResult",
    "sceneNgonsPercentage" : "sceneNgonsPercentageResult",
    "sceneIsolatedVertices" : "sceneIsolatedVerticesResult",
    "sceneOverlappingVertices" : "sceneOverlappingVerticesResult",
    "sceneOverlappingFaces" : "sceneOverlappingFacesResult",
    "sceneObjectsNoMat" : "sceneObjectsNoMatResult",
    "sceneMaterialsNoTex" : "sceneMaterialsNoTexResult",
}

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class CMIProperties(PropertyGroup):

    testType: EnumProperty(
        items=(
            ("lite", "CheckMate Lite", ""),
            ("pro", "CheckMate Pro", ""),
        ),
        name="CheckMate Test Type",
        default="lite",
        description="CheckMate Test Type",
    )

    # Objects
    sceneObjects : IntProperty()
    sceneGeometry : IntProperty()
    sceneLights : IntProperty()
    sceneCameras : IntProperty()
    sceneShapes : IntProperty()
    sceneCollection: StringProperty()
    sceneDefaultNames: IntProperty()
    sceneInvalidTransforms: IntProperty()

    # Need three states, so Ints will replace Bools
    # 0 = FAIL
    # 1 = PASS
    # 2 = NOT RUN
    sceneObjectsResult : IntProperty(default = 2)
    sceneGeometryResult : IntProperty(default = 2)
    sceneLightsResult : IntProperty(default = 2)
    sceneCamerasResult : IntProperty(default = 2)
    sceneShapesResult : IntProperty(default = 2)
    sceneCollectionResult : IntProperty(default = 2)
    sceneDefaultNamesResult: IntProperty(default = 2)
    sceneInvalidTransformsResult: IntProperty(default = 2)

    # Geometry
    sceneVertices: IntProperty()
    sceneFaces: IntProperty()
    sceneQuads: IntProperty()
    sceneQuadsPercentage: FloatProperty()
    sceneTriangles: IntProperty()
    sceneTrianglesPercentage: FloatProperty()
    sceneNgons: IntProperty()
    sceneNgonsPercentage: FloatProperty()

    sceneIsolatedVertices : IntProperty()
    sceneOverlappingVertices : IntProperty()
    sceneOverlappingFaces : IntProperty()

    sceneVerticesResult : IntProperty(default = 2)
    sceneFacesResult : IntProperty(default = 2)
    sceneQuadsResult : IntProperty(default = 2)
    sceneQuadsPercentageResult : IntProperty(default = 2)
    sceneTrianglesResult : IntProperty(default = 2)
    sceneTrianglesPercentageResult : IntProperty(default = 2)
    sceneNgonsResult : IntProperty(default = 2)
    sceneNgonsPercentageResult : IntProperty(default = 2)
    sceneIsolatedVerticesResult : IntProperty(default = 2)
    sceneOverlappingVerticesResult : IntProperty(default = 2)
    sceneOverlappingFacesResult : IntProperty(default = 2)

    # Materials
    sceneObjectsNoMat: IntProperty()

    sceneObjectsNoMatResult: IntProperty(default = 2)

    # Textures
    sceneMaterialsNoTex: IntProperty()

    sceneMaterialsNoTexResult: IntProperty(default = 2)

# ------------------------------------------------------------------------
#    Panel in N-Panel
# ------------------------------------------------------------------------

class CMIResults_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CheckMate Results"
    bl_options = {"HIDE_HEADER"}


class CMIResults_PT_panel_1(CMIResults_panel, bpy.types.Panel):
    bl_idname = "CMIResults_PT_panel_1"
    bl_label = "Panel 1"
    def draw(self, context):
        layout = self.layout
        layout.label(text="CheckMate Results")
        
class CMIResults_PT_panel_2(CMIResults_panel, bpy.types.Panel):
    bl_parent_id = "CMIResults_PT_panel_1"
    bl_label = "Panel 2"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Objects")

        cmiProperties = context.scene.cmi_tool
        if cmiProperties.testType == "pro":
            addTestUI("Total Objects", cmiProperties.sceneObjects, layout, cmiProperties.sceneObjectsResult, None)
            addTestUI("Geometry", cmiProperties.sceneGeometry, layout,cmiProperties.sceneGeometryResult, None)
            addTestUI("Cameras", cmiProperties.sceneCameras, layout, cmiProperties.sceneCamerasResult, None)
            addTestUI("Lights", cmiProperties.sceneLights, layout, cmiProperties.sceneLightsResult, None)
            addTestUI("Shapes", cmiProperties.sceneShapes, layout, cmiProperties.sceneShapesResult, None)
            addTestUI("Required Collection", "", layout, cmiProperties.sceneCollectionResult, CMI_OT_CollectionTest)
            addTestUI("Objects with Default Names", cmiProperties.sceneDefaultNames, layout, cmiProperties.sceneDefaultNamesResult, CMI_OT_DefaultNamesTest)
            addTestUI("Objects with Invalid Transforms", cmiProperties.sceneInvalidTransforms, layout, cmiProperties.sceneInvalidTransformsResult, CMI_OT_InvalidTransformsTest)
        else:
            addTestUI("Total Objects", cmiProperties.sceneObjects, layout, cmiProperties.sceneObjectsResult, None)
            addTestUI("Geometry", cmiProperties.sceneGeometry, layout,cmiProperties.sceneGeometryResult, None)
            addTestUI("Cameras", cmiProperties.sceneCameras, layout, cmiProperties.sceneCamerasResult, None)
            addTestUI("Lights", cmiProperties.sceneLights, layout, cmiProperties.sceneLightsResult, None)
            addTestUI("Shapes", cmiProperties.sceneShapes, layout, cmiProperties.sceneShapesResult, None)

class CMIResults_PT_panel_3(CMIResults_panel, bpy.types.Panel):
    bl_parent_id = "CMIResults_PT_panel_1"
    bl_label = "Panel 3"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Geometry")

        cmiProperties = context.scene.cmi_tool
        if cmiProperties.testType == "pro":
            addTestUI("Vertices", cmiProperties.sceneVertices, layout, cmiProperties.sceneObjectsResult, None)
            addTestUI("Faces", cmiProperties.sceneFaces, layout, cmiProperties.sceneFacesResult, None)
            addTestUI("Quads", cmiProperties.sceneQuads, layout, cmiProperties.sceneQuadsResult, None)
            addTestUI("Triangles", cmiProperties.sceneTriangles, layout, cmiProperties.sceneTrianglesResult, None)
            addTestUI("Triangles Percentage", str(round(cmiProperties.sceneTrianglesPercentage, 2)) + "%", layout, cmiProperties.sceneTrianglesPercentageResult, CMI_OT_SelectTrianglesTest)
            addTestUI("N-Gons", cmiProperties.sceneNgons, layout, cmiProperties.sceneNgonsResult, None)
            addTestUI("N-Gons Percentage", str(round(cmiProperties.sceneNgonsPercentage,2)) + "%", layout, cmiProperties.sceneNgonsPercentageResult, CMI_OT_SelectNgonsTest)
            addTestUI("Loose Vertices", cmiProperties.sceneIsolatedVertices, layout, cmiProperties.sceneIsolatedVerticesResult, CMI_OT_IsolatedVerticesTest)
            addTestUI("Overlapping Vertices", cmiProperties.sceneOverlappingVertices, layout, cmiProperties.sceneOverlappingVerticesResult, CMI_OT_OverlappingVerticesTest)
            addTestUI("Overlapping Faces", cmiProperties.sceneOverlappingFaces, layout, cmiProperties.sceneOverlappingFacesResult, CMI_OT_OverlappingFacesTest)
        else:
            addTestUI("Vertices", cmiProperties.sceneVertices, layout, cmiProperties.sceneObjectsResult, None)
            addTestUI("Faces", cmiProperties.sceneFaces, layout, cmiProperties.sceneFacesResult, None)
            addTestUI("Quads", cmiProperties.sceneQuads, layout, cmiProperties.sceneQuadsResult, None)
            addTestUI("Triangles", cmiProperties.sceneTriangles, layout, cmiProperties.sceneTrianglesResult, None)


class CMIResults_PT_panel_4(CMIResults_panel, bpy.types.Panel):
    bl_parent_id = "CMIResults_PT_panel_1"
    bl_label = "Panel 4"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Materials")

        cmiProperties = context.scene.cmi_tool

        if cmiProperties.testType == "pro" or cmiProperties.testType == "lite":
            addTestUI("Objects without materials", cmiProperties.sceneObjectsNoMat, layout, cmiProperties.sceneObjectsNoMatResult, CMI_OT_MissingMaterialsTest)
            
class CMIResults_PT_panel_5(CMIResults_panel, bpy.types.Panel):
    bl_parent_id = "CMIResults_PT_panel_1"
    bl_label = "Panel 5"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Textures")

        cmiProperties = context.scene.cmi_tool

        if cmiProperties.testType == "pro" or cmiProperties.testType == "lite":
            addTestUI("Missing textures", cmiProperties.sceneMaterialsNoTex, layout, cmiProperties.sceneMaterialsNoTexResult, CMI_OT_MissingTexturesTest)

# ------------------------------------------------------------------------
#    Buttons
# ------------------------------------------------------------------------


class CMI_OT_CollectionTest(bpy.types.Operator):
    bl_idname = "scene.collectiontest"
    bl_label = "Select objects"

    def execute(self, context):
        #print(checkIfHasCollection()[1])
        for obj in checkIfHasCollection()[1]:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}

class CMI_OT_DefaultNamesTest(bpy.types.Operator):
    bl_idname = "scene.defaultnamestest"
    bl_label = "Select objects"

    def execute(self, context):            
        for obj in checkDefaultNames()[1]:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.view3d.view_selected()

        bpy.ops.view3d.view_selected()
        return {'FINISHED'}

class CMI_OT_InvalidTransformsTest(bpy.types.Operator):
    bl_idname = "scene.invalidtransformstest"
    bl_label = "Select objects"

    def execute(self, context):            
        for obj in checkValidTransforms()[1]:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.view3d.view_selected()

        bpy.ops.view3d.view_selected()
        return {'FINISHED'}


class CMI_OT_SelectTrianglesTest(bpy.types.Operator):
    bl_idname = "scene.selectrianglestest"
    bl_label = "View Triangles"

    def execute(self, context):    
        for obj in bpy.context.scene.objects:
            if (obj.type == "MESH"):
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_face_by_sides(number=3, type='EQUAL', extend=True)
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}
        
class CMI_OT_SelectNgonsTest(bpy.types.Operator):
    bl_idname = "scene.selectngonstest"
    bl_label = "View N-gons"

    def execute(self, context):    
        for obj in bpy.context.scene.objects:
            if (obj.type == "MESH"):
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER', extend=True)
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}

class CMI_OT_IsolatedVerticesTest(bpy.types.Operator):
    bl_idname = "scene.isolatedverticestest"
    bl_label = "View vertices"

    def execute(self, context):
        checkLooseVerts(True)
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}

class CMI_OT_OverlappingVerticesTest(bpy.types.Operator):
    bl_idname = "scene.overlappingverticestest"
    bl_label = "View vertices"

    def execute(self, context):
        checkOverlappingVerts(0.0001, True)
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}

class CMI_OT_OverlappingFacesTest(bpy.types.Operator):
    bl_idname = "scene.overlappingfacestest"
    bl_label = "View faces"

    def execute(self, context):
        checkOverlappingFaces(0.0001, True)
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}

class CMI_OT_MissingMaterialsTest(bpy.types.Operator):
    bl_idname = "scene.missingmaterialstest"
    bl_label = "Select objects"

    def execute(self, context):
        for obj in checkMissingMaterials()[1]:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.view3d.view_selected()
        return {'FINISHED'}


class CMI_OT_MissingTexturesTest(bpy.types.Operator):
    bl_idname = "scene.missingtexturestest"
    bl_label = "Report Missing Textures"

    def execute(self, context):
        bpy.ops.screen.info_log_show()
        bpy.ops.info.select_all(action='SELECT')
        bpy.ops.info.report_delete()
        for tex in checkMissingTextures()[1]:
            self.report({'WARNING'},str(tex.name) + " (" + str(tex.filepath) + ")")
        
        return {'FINISHED'}


def addTestUI(testName, value, layout, icon, buttonOperator):
    iconLocal = "QUESTION"
    alert = False
    status = ""
    showButton = False
    match icon:
        case 0: 
            iconLocal="X"
            status = "FAIL"
            alert = True
            showButton = True
        case 1: 
            iconLocal="CHECKMARK"
            status = "PASS"
            alert = False
            showButton = False
        case 2: 
            iconLocal="QUESTION"
            status = ""
            alert = False
            showButton = False

    col = layout.column()
    box = col.box()
    mainBox = box.column()
    row = mainBox.row()
    row.alert = alert
    split = row.split(factor=0.55) # use factor instead of percentage for Blender 2.8+

    c = split.column()
    box = c.box()
    box.label(text=testName)

    split = split.split(factor=0.45)

    c = split.column()
    box = c.box()
    box.label(text=str(value))
    split = split.split(factor=1)

    c = split.column()
    box = c.box()
    box.label(text=status, icon=iconLocal)
    if showButton and not buttonOperator == None:
         mainBox.operator(buttonOperator.bl_idname)



# ------------------------------------------------------------------------
#    Panel in Properties
# ------------------------------------------------------------------------

class PANEL_PT_cmi(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "CheckMate Inspector "
    bl_idname = "cmi.propertiespanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        col = layout.column(align=True)
        col.prop(scene.cmi_tool, "testType", text="")
        col.separator()
        row = layout.row()
        row.scale_y = 2.0
        row.operator(StartTest_OT.bl_idname)
        
        row = layout.row()
        row.separator()
        row.scale_y = 1.0
        row.operator(ResetTests_OT.bl_idname)
        row.separator()

class StartTest_OT(bpy.types.Operator):
    """Start the CheckMate test"""
    bl_idname = "object.cmiteststart"
    bl_label = "Start Tests"
    def execute(self, context):    
        startTest(context, context.scene.cmi_tool.testType)
        self.report({"INFO"}, "Success")
        return {'FINISHED'}
        #self.report({"WARNING"}, "Nothing selected")
        #return {'CANCELLED'}

class ResetTests_OT(bpy.types.Operator):
    """Resets all CheckMate tests"""
    bl_idname = "object.cmitestreset"
    bl_label = "Reset Tests"

    def execute(self, context):
        resetTests(context)
        self.report({"INFO"}, "Success")
        return {'FINISHED'}
        #self.report({"WARNING"}, "Nothing selected")
        #return {'CANCELLED'}


# ------------------------------------------------------------------------
#    Tests
# ------------------------------------------------------------------------


# Do the objects belong to a collection?
# Returns TRUE or FALSE, list of objects without a collection (FALSE), list of collections (TRUE/FALSE)
def checkIfHasCollection():
    objectsWithoutCollection = []
    collections = []
    for col in bpy.data.collections:
        collections.append(col.name)
    for obj in bpy.data.objects:    
        if (len(obj.users_collection) == 1):
            if (obj.users_collection[0].name == "Scene Collection"):
                objectsWithoutCollection.append(obj)
        #if obj.users_collection in collections:
        #if (obj.users_collection[0].name == "Scene Collection"):
        #    objectsWithoutCollection.append(obj)
    return False if len(objectsWithoutCollection) > 0 else True, objectsWithoutCollection, collections

# What is the percentage of triangles?
# Returns TRUE or FALSE, percentage (TRUE if > 20%, FALSE otherwise)
def checkPercentageTriangles():
    polys = getSceneStats()[1]['sceneFaces']
    tris = getSceneStats()[1]['sceneTriangles']
    try:
        if (round((tris/polys) * 100, 2) > 20):
            return False, round((tris/polys) * 100, 2)
        else:
            return True, round((tris/polys) * 100, 2)
    except ZeroDivisionError:
        return True, 100

# What is the percentage of N-Gons?
# Returns TRUE or FALSE, percentage (TRUE if > 20%, FALSE otherwise)
def checkPercentageNgons():
    polys = getSceneStats()[1]['sceneFaces']
    ngons = getSceneStats()[1]['sceneNgons']
    try:
        return False if round((ngons/polys) * 100, 2) > 0 else True, round((ngons/polys) * 100, 2)
    except ZeroDivisionError:
        return True, 100

# Are all textures present?
# Returns TRUE or FALSE, list of missing files (TRUE), list of objects with missing textures
def checkMissingTextures():
    missingTextures = []
    objMissingTextures = []
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            for s in obj.material_slots:
                if s.material and s.material.use_nodes:
                    for n in s.material.node_tree.nodes:
                        if n.type == 'TEX_IMAGE':
                            if not n.image.has_data:
                                if n.image not in missingTextures:
                                    missingTextures.append(n.image)
                                if obj not in objMissingTextures:
                                    objMissingTextures.append(obj)

    return False if len(missingTextures) > 0 else True, missingTextures, objMissingTextures

# Are all materials present?
# Returns TRUE or FALSE, number of missing materials, list of objects with missing materials
def checkMissingMaterials():
    objMissingMaterials = []
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            if not len(obj.material_slots) > 0:
                objMissingMaterials.append(obj)
    return False if len(objMissingMaterials) > 0 else True, objMissingMaterials

# Do objects have loose, disconnected vertices?
# Returns TRUE or FALSE, number of loose vertices, number of objects with loose vertices
def checkLooseVerts(selectVerts):
    looseVerts = 0
    objsLooseVerts = [] 
    deselectAllEditMode()
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_loose()
            looseVerts += obj.data.total_vert_sel
            if obj.data.total_vert_sel > 0: 
                objsLooseVerts.append(obj)
            if not selectVerts: bpy.ops.object.mode_set(mode="OBJECT")
    return False if len(objsLooseVerts) > 0 else True, looseVerts, objsLooseVerts

# Do objects have overlapping vertices?
# Returns TRUE or FALSE, number of overlapping vertices, number of objects with overlapping vertices
def checkOverlappingVerts(distance, selectVerts):
    overlappingVerts = 0
    objOverlappingVerts = []
    deselectAllEditMode()
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            verts = bm.verts
            verts.ensure_lookup_table()

            size = len(verts)
            kd = kdtree.KDTree(size)
            for i, vtx in enumerate(verts):
                kd.insert(vtx.co, i)
            kd.balance()

            temp_verts = 0

            for i, vtx in enumerate(verts):
                vtx_group = []
                for (co, index, dist) in kd.find_range(vtx.co, distance):
                    vtx_group.append(index)
                if len(vtx_group) > 1:
                    overlappingVerts += 1
                    temp_verts += 1
                    for index in vtx_group:
                       if selectVerts: verts[index].select = True
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

            bmesh.update_edit_mesh(me, destructive=False)
            
            if temp_verts > 0:
                objOverlappingVerts.append(obj)
            
        if not selectVerts: bpy.ops.object.mode_set(mode="OBJECT")
        
    return False if overlappingVerts > 0 else True, overlappingVerts, objOverlappingVerts

# Do objects have overlapping faces?
# Returns TRUE or FALSE, number of overlapping faces, number of objects with overlapping faces
def checkOverlappingFaces(distance, selectVerts):
    overlappingFaces = 0
    objOverlappingFaces = []
    deselectAllEditMode()
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            faces = bm.faces
            faces.ensure_lookup_table()

            size = len(faces)
            kd = kdtree.KDTree(size)
            for i, vtx in enumerate(faces):
                face_location = vtx.calc_center_median()
                vec = Vector((face_location[0], face_location[1], face_location[2]))
                kd.insert(vec, i)
            kd.balance()


            temp_polys = 0

            for i, vtx in enumerate(faces):
                vtx_group = []
                face_location = vtx.calc_center_median()
                vec = Vector((face_location[0], face_location[1], face_location[2]))
                for (vec, index, dist) in kd.find_range(vec, distance):
                    vtx_group.append(index)
                if len(vtx_group) > 1:
                    overlappingFaces += 1
                    temp_polys += 1
                    for index in vtx_group:
                       if selectVerts: faces[index].select = True
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

            bmesh.update_edit_mesh(me, destructive=False)
            
            if temp_polys > 0:
                objOverlappingFaces.append(obj)
            
        if not selectVerts: bpy.ops.object.mode_set(mode="OBJECT")
        
    return False if overlappingFaces > 0 else True, overlappingFaces, objOverlappingFaces

# Do objects have default names?
# Returns TRUE or FALSE, list of objects with default names
def checkDefaultNames():
    objDefaultNames = []
    for obj in bpy.context.scene.objects:
        containsKeyword = any(defaultNamesKeyword in obj.name for defaultNamesKeyword in defaultNamesKeywords)
        if containsKeyword: objDefaultNames.append(obj)
    return False if len(objDefaultNames) > 0 else True, objDefaultNames

# Do objects have zeroed transforms (location/rotation/scale set to 0,0,0 and 1,1,1)?
# Returns TRUE or FALSE, list of objects with invalid transforms
def checkValidTransforms():
    objInvalidTransforms = []
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            if not ((obj.location == Vector((0,0,0)) and obj.rotation_euler == Euler((0,0,0), 'XYZ') and  obj.scale == Vector((1,1,1)))):
                objInvalidTransforms.append(obj)
    return False if len(objInvalidTransforms) > 0 else True, objInvalidTransforms


# ------------------------------------------------------------------------
#    Helper functions
# ------------------------------------------------------------------------

def is_object_in_collection(object_name, collection_name):
    object = bpy.data.objects.get(object_name)
    if not object:
        return False
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        return False
    return collection in object.users_collection


# Deselect everything in Edit Mode
def deselectAllEditMode():
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode="OBJECT")

# General statistics about the scene
def getSceneStats():
    cmiProperties = bpy.context.scene.cmi_tool
    sceneObjects = {
        'sceneCameras': 0,
        'sceneLights': 0,
        'sceneShapes': 0,
        'sceneGeometry': 0,
        'sceneObjects': 0
    }
    sceneStats = {
        'sceneVertices': 0,
        'sceneQuads': 0,
        'sceneFaces': 0,
        'sceneTriangles': 0,
        'sceneNgons': 0
    }
    for obj in bpy.context.scene.objects:
        sceneObjects['sceneObjects']+=1
        if (obj.type == "MESH"):
            showSubdiv(False, obj)
            sceneStats['sceneFaces'] += len(obj.data.polygons)
            for poly in obj.data.polygons:
                if (len(poly.vertices) == 4):
                    sceneStats['sceneQuads'] += 1
                elif (len(poly.vertices) == 3):
                    sceneStats['sceneTriangles'] += 1
                elif (len(poly.vertices) > 3):
                    sceneStats['sceneNgons'] += 1
            sceneStats['sceneVertices'] += len(obj.data.vertices)
            
            showSubdiv(True, obj)
        match obj.type:
            case 'MESH': sceneObjects['sceneGeometry']+=1
            case 'LIGHT': sceneObjects['sceneLights']+=1
            case 'CAMERA': sceneObjects['sceneCameras']+=1
            case 'CURVE': sceneObjects['sceneShapes']+=1
    return sceneObjects, sceneStats
 
def showSubdiv(show, obj):
    for m in obj.modifiers:
        if(m.type == "SUBSURF"):
            m.show_viewport = show



def startTest(context, type):
    cmiProperties = context.scene.cmi_tool
    match type:
        case "lite":
            
             # Test objects
            for test in objectsTests:
                cmiProperties[test] = getSceneStats()[0][test]
                cmiProperties[objectsTests[test]] = 1
            
            # Get scene stats
            for test in geometryTests:
                cmiProperties[test] = getSceneStats()[1][test]
                cmiProperties[geometryTests[test]] = 1

            # Test materials
            cmiProperties.sceneObjectsNoMat = len(checkMissingMaterials()[1])
            cmiProperties.sceneObjectsNoMatResult = checkMissingMaterials()[0]

            # Test textures
            cmiProperties.sceneMaterialsNoTex = len(checkMissingTextures()[1])
            cmiProperties.sceneMaterialsNoTexResult = checkMissingTextures()[0]


        case "pro":

            # Test objects
            for test in objectsTests:
                cmiProperties[test] = getSceneStats()[0][test]
                cmiProperties[objectsTests[test]] = 1

            # Test default names
            cmiProperties.sceneDefaultNames = len(checkDefaultNames()[1])
            cmiProperties.sceneDefaultNamesResult = checkDefaultNames()[0]

            # Test valid transforms
            cmiProperties.sceneInvalidTransforms = len(checkValidTransforms()[1])
            cmiProperties.sceneInvalidTransformsResult = checkValidTransforms()[0]


            # Test collection
            cmiProperties.sceneCollection = str(checkIfHasCollection()[2])
            cmiProperties.sceneCollectionResult = int(checkIfHasCollection()[0])
            
            # Get scene stats
            for test in geometryTests:
                cmiProperties[test] = getSceneStats()[1][test]
                cmiProperties[geometryTests[test]] = 1

            # Test triangles percentage
            cmiProperties.sceneTrianglesPercentage = checkPercentageTriangles()[1]
            cmiProperties.sceneTrianglesPercentageResult = checkPercentageTriangles()[0]

            # Test ngons/ngons percentage
            cmiProperties.sceneNgons = getSceneStats()[1]["sceneNgons"]
            cmiProperties.sceneNgonsResult = 0 if getSceneStats()[1]["sceneNgons"] > 0 else 1

            cmiProperties.sceneNgonsPercentage = checkPercentageNgons()[1]
            cmiProperties.sceneNgonsPercentageResult = checkPercentageNgons()[0]

            # Test overlapping/loose vertices/faces
            cmiProperties.sceneIsolatedVertices = checkLooseVerts(False)[1]
            cmiProperties.sceneIsolatedVerticesResult = 1 if checkLooseVerts(False)[0] else 0

            cmiProperties.sceneOverlappingVertices = checkOverlappingVerts(0.0001, False)[1]
            cmiProperties.sceneOverlappingVerticesResult = 1 if checkOverlappingVerts(0.001, False)[0] else 0

            cmiProperties.sceneOverlappingFaces = checkOverlappingFaces(0.0001, False)[1]
            cmiProperties.sceneOverlappingFacesResult = 1 if checkOverlappingFaces(0.001, False)[0] else 0

            # Test materials
            cmiProperties.sceneObjectsNoMat = len(checkMissingMaterials()[1])
            cmiProperties.sceneObjectsNoMatResult = checkMissingMaterials()[0]

            # Test textures
            cmiProperties.sceneMaterialsNoTex = len(checkMissingTextures()[1])
            cmiProperties.sceneMaterialsNoTexResult = checkMissingTextures()[0]

        case _:
            print ("default test")
    
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def resetTests(context):
    cmiProperties = context.scene.cmi_tool

    for test in resettableTests:
        cmiProperties[test] = 0
        cmiProperties[resettableTests[test]] = 2
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    CMIProperties,
    PANEL_PT_cmi,
    StartTest_OT,
    ResetTests_OT,
    CMI_OT_CollectionTest,
    CMI_OT_InvalidTransformsTest,
    CMI_OT_DefaultNamesTest,
    CMI_OT_SelectTrianglesTest,
    CMI_OT_SelectNgonsTest,
    CMI_OT_IsolatedVerticesTest,
    CMI_OT_OverlappingVerticesTest,
    CMI_OT_OverlappingFacesTest,
    CMI_OT_MissingMaterialsTest,
    CMI_OT_MissingTexturesTest,
    CMIResults_PT_panel_1,
    CMIResults_PT_panel_2,
    CMIResults_PT_panel_3,
    CMIResults_PT_panel_4,
    CMIResults_PT_panel_5,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.cmi_tool = PointerProperty(type=CMIProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.cmi_tool


if __name__ == "__main__":
    register()