# -*- coding: utf-8 -*-
"""
Neal Gordon
Abaqus Scripting
http://nagordon.github.io/
2015-04-2

"""

# Import abaqus modules
from abaqus import session
import visualization
import xyPlot
from abaqusConstants import PNG, AVI, CONTOURS_ON_DEF, \
                            INTEGRATION_POINT, COMPONENT, OFF, ON, \
                            FEATURE, DISCRETE, CONTINUOUS, ALL_FRAMES, \
                            TIME_HISTORY, UNLIMITED, UNDEFORMED, \
                            SCALE_FACTOR, NODAL, LARGE

jobName = sys.argv[-1]


# load odb file
myViewport = session.Viewport(name='myViewport', origin=(10, 10), width=300, height=200)
myOdb = visualization.openOdb(path=jobName + '.odb')
myViewport.setValues(displayedObject=myOdb)

# set viewport settings
v = 'Iso'
myViewport.view.setValues(session.views[v])
myViewport.maximize()
myViewport.view.fitView()
myViewport.odbDisplay.basicOptions.setValues(coordSystemDisplay=OFF, translucencySort=ON)
myViewport.odbDisplay.commonOptions.setValues(visibleEdges=FEATURE)  # NONE
myViewport.odbDisplay.contourOptions.setValues(contourStyle=CONTINUOUS) # DISCRETE CONTINUOUS
#myViewport.odbDisplay.contourOptions.setValues(showMinLocation=ON,showMaxLocation=ON)
#myViewport.odbDisplay.contourOptions.setValues(numIntervals=6)
myViewport.viewportAnnotationOptions.setValues(triad=OFF, title=OFF, state=ON,  compass=OFF,
                                              legend=ON, legendPosition=(75, 95), legendBox=OFF,
                                              legendFont='-*-verdana-medium-r-normal-*-*-120-*-*-p-*-*-*',
                                              statePosition=(1, 15),
                                              titleFont='-*-verdana-medium-r-normal-*-*-120-*-*-p-*-*-*',
                                              stateFont='-*-verdana-medium-r-normal-*-*-120-*-*-p-*-*-*')


# saving undeformed image
myViewport.odbDisplay.display.setValues(plotState=(UNDEFORMED, ))
path_filename = '%s_%s' % (myOdb.name.replace('.odb',''),v)
try:
    session.printToFile(path_filename, PNG, (myViewport,))
    print('saving %s' % path_filename)
except:
    pass

# save stress plots
v = 'Iso' ; o = 'S' ; c = 'S11' ; s = 0 ; f = -1
myViewport.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
myViewport.odbDisplay.setFrame(step=s, frame=f)

myViewport.odbDisplay.setPrimaryVariable(variableLabel=o,outputPosition=INTEGRATION_POINT,refinement=(COMPONENT, c), )
path_filename = '%s_step-%s_%s_%s_%s' % (myOdb.name.replace('.odb',''),s,o,c,v)
try:
    myViewport.view.fitView()
    session.printToFile(path_filename+'.png', PNG, (myViewport,))
    print('saving %s' % path_filename)

    myViewport.view.fitView()
    session.animationController.setValues(animationType=TIME_HISTORY, viewports=(myViewport.name, ))    # SCALE_FACTOR   TIME_HISTORY
    session.animationController.play(duration=UNLIMITED)
    session.animationController.animationOptions.setValues(frameRate=15)
    session.writeImageAnimation(fileName=path_filename+'.avi', format=AVI, canvasObjects=(myViewport,))
    print('saving %s' % path_filename+'.avi')
except:
    pass


# PLotting
xyp = session.XYPlot(name='XYPlot-1')
## can be run multiple times but the line >>>session.xyPlots['XYPlot-1'] , can only be run once >>>ession.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
chart.legend.setValues(show=False)
chart.legend.titleStyle.setValues(font='-*-verdana-medium-r-normal-*-*-240-*-*-p-*-*-*')
chart.gridArea.style.setValues(fill=False)
xyp.title.style.setValues(font='-*-arial-medium-r-normal-*-*-240-*-*-p-*-*-*')

# x = 'Strain energy: ALLSE for Whole Model'
# sName = myOdb.steps.keys()[s]
# xy1 = xyPlot.XYDataFromHistory(odb=myOdb, outputVariableName=x, steps=(sName, ), )
# c1 = session.Curve(xyData=xy1)
# chart.setValues(curvesToPlot=(c1, ), )
# myViewport.setValues(displayedObject=xyp)
# chartName = xyp.charts.keys()[0]
# chart = xyp.charts[chartName]
# path_filename = '%s_Xplot_step-%s_x-%s' % \
#     (myOdb.name.replace('.odb',''), sName, x.split(':')[1].split(' ')[1])
# try:
#     myViewport.view.fitView()
#     session.printToFile(path_filename+'.png', PNG, (myViewport,))
#
#     myViewport.view.fitView()
#     session.animationController.setValues(animationType=TIME_HISTORY, viewports=(myViewport.name, ))    # SCALE_FACTOR   TIME_HISTORY
#     session.animationController.play(duration=UNLIMITED)
#     session.animationController.animationOptions.setValues(xyShowSymbol=True, xySymbolSize=LARGE)
#     session.writeImageAnimation(fileName=path_filename+'.avi', format=AVI, canvasObjects=(session.viewports[myViewport.name], ))
#     print('saved %s' % path_filename+'.avi')
# except:
    pass
