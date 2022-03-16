selectFile = {
    "Allowed extensions": "obj",
    "Requirements": "Manifold, triangulation(only triangles), one connected figure, no unused vertices",
}
selectMode = {
    "Manual": "In manual mode you have the option to give the program information about the "
    "object in the 'anazlyze' menu that will show up and get runtime predictions and "
    "suggestions for the next steps. After that you it is optional to segment the mesh with the button "
    "below the 3d plotter. The number next to it stands for the desired amount of resulting pieces.",
    "Automatic": "The program performs iterative segmentation and parameterization automatically",
}
analyze = {
    "About": "Here you can enter information about the object in order to get advice on how to proceed."
}
flatten = {
    "BFF": "Cones are cuts into the surface done by the algorithm when flattening. "
    "This works especially well with basic objects.",
    "ARAP": "Focuses on length and area preservation.",
}
plottingOptions = {
    "Edges": "Edge visibility can be turned on and off in order to view the distortion better and have a "
    "faster refreshing liveview when placing patterns",
    "Chart Colors": "Shows the corresponding chart colors if the mesh was segmented before the flattening.",
    "Angular Distortion": "Shows how much the angles of the triangles got changed during the parameterization.",
    "Isometric Distortion": "Shows how much the area of the triangle got changed.",
    "Max. Isometric Distortion": "A different formula which results in a more delicate way of showing the area changes.",
}
measuringTool = {
    "Measure length": "Clicking once on the canvas sets a point A and after that the length "
    "between A and the cursor will be displayed.",
    "Measure angle": "Clicking two times on the canvas will set up points A and B. Afterwards the angle of the angle "
    "made up of A, B and the cursor will be measured.",
}
exportShapes = {
    "Output format": "obj",
    "About": "Here you can export the flat shapes for further processing.",
}
allPatterns = {
    "Placing": "When pressing 'place', you can enter all values "
    "required(Parameters etc). When entering these values, the pattern will change in realtime according to "
    "the values you enter. Once finished, the pattern will be inserted into the placed-patterns-list."
}
palcedPatterns = {
    "About": "Here you can view all your placed patterns",
    "Colors": "If a pattern is checking its location validity it is blue. Once it finished the color turns to red or green "
    "depending on whether it is inside a shape or not.",
    "E Factor": "Each time the printer prints, the distance will be multiplied with this value and added to the GCode command",
    "Overruns": "Before and After printing the printer will move on the print height without printing. These values "
    " specify the distances of the overruns.",
    "Print Overruns": "Same as the start overrun, but instead of just moving the device will print.",
    "F Value": "Indicates the speed of the 3d printer. This is added to every GCode command.",
}
