library(shiny)

#----1.---------------------------UI block-------------------------------
#This is where the UI component will go.
#this will decide what your shiny APP will LOOK like (presentation, inputs, outputs, text, plots etc)



ui <- fluidPage ("Hello Shweta")
#-------------------------------UI block-------------------------------








#------2.-------------------------SERVER block-------------------------------
# This will determine WHAT your Rshiny app will do. i.e. when you interact with the UI
#above WHAT will happen


server <- function (input, output){}
#-------------------------------SERVER block-------------------------------





#--------3.-----------------------APP block-------------------------------
#this command packs your APP together
shinyApp ( ui = ui, server=server);