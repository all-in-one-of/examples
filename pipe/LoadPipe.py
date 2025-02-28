# Loads a point cloud dataset of a section of a pipe capture by LIDAR

# TODO: append GeoLoader package to python search path in omegalib: workaround
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

from omega import setEventFunction, setUpdateFunction
from cyclops import ProgramAsset, PrimitiveType, UniformType, getSceneManager, Light
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler
from pipelines.util import vmCheck
from pointCloud import PointCloud

VM = vmCheck()

program = ProgramAsset()
program.name = "pointsDepth"

modelName = "pipe"
modelPath = basePath + "/squarePipeSliceA.002"
modelExtension = "ply"

shaderPath = "pointCloud/shaders"

if VM:
	pointSize = 5.0
	pointCloudMaker = PointCloud.createAndInitialize(getSceneManager(), modelName, modelPath, modelExtension, pointSize)
	pipe = Geometry()
	pipe.setStaticObject(pointCloudMaker.getStaticObject())
	program.vertexShaderName = shaderPath + "/pointsVM.vert"
	program.fragmentShaderName = shaderPath + "/pointsVM.frag"
else:
	pipe = Geometry(modelPath+"."+modelExtension)
	program.vertexShaderName = shaderPath + "/Sphere.vert"
	program.fragmentShaderName = shaderPath + "/Sphere.frag"
	program.geometryShaderName = shaderPath + "/Sphere.geom"
	program.geometryOutVertices = 4
	program.geometryInput = PrimitiveType.Points
	program.geometryOutput = PrimitiveType.TriangleStrip


pipe.initialRotation = [-30, -135, 0]
pipe.initialPosition = [0, 0, -200]
pipe.setShader(program)

light = Light.create()
light.setPosition(0, 250, -100)

if not VM:
	pipe.getMaterial().addUniform('pointScale', UniformType.Float)
	pipe.getMaterial().getUniform('pointScale').setFloat(0.07)

pipe.xMoveClamp = pipe.yMoveClamp = 100
pipe.zMoveClamp = 200

handler = GeometryHandler()

handler.allowZRot = False
handler.xMoveSensitivity *= 4
handler.yMoveSensitivity *= 4
handler.zMoveSensitivity *= 50
handler.xRotSensitivity *= 2
handler.yRotSensitivity *= 2
handler.zRotSensitivity *= 2

handler.spaceNavRotSensitivity *= 7

handler.addGeo(pipe)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)

