# ZeroHunger
Food Wastage on side of the globe, hunger / poverty on the other side -> Make the world free of hunger faster. 
2 parts – ML Prediction, Graph Logistic Optimization Part. 

ML Prediction  
Project begins with the data collection from UN. 
Cleaning the data, sampled the data to a smaller subset. 
ML model to predict agricultural land available, crop produced based on land, temperature effects, fertilizers and livestock. 
We have crops produced, population -> arrive at food consumption patterns, surplus/deficiency. 

For each country, we have food surplus/deficiency for each crop. 
  Surplus -> Exports 
  Deficiency -> Imports 

Where to export to or import from? 
  F(profitability) 
    F(demand, shipping cost) 
      F(demand) -> surplus 
    F(shipping cost) -> F(distance, route) -> Route - land/sea 

Quantity to be exported to or imported from a different country. 
