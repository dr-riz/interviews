# Amazon 


### Problem statement
The BIA role requires you to be able to analyze large quantities of data and present metrics indicating if Amazon is improving or getting worse in certain areas.  A good example of this is determining if our forecasts match what actually happened. 

Assume we have the following table and columns 

Table: UnitsSold

   ProductID

   Quantity

   Date

  ForecastOrActual – can be “A” for actual and “B” for forecast. 

Sample Data would look like 


| ProductID | Quantity | Date        | ForecastOrActual |
| --------- | -------- | ----------- | ---------------- |
| Widget    | 100      | 1-June-2015 | F 				|
| Widget    | 120      | 1-June-2015 | A 				|
| Gizmo     | 90       | 1-June-2015 | F 				| 
| Gizmo     | 80       | 1-June-2015 | A				|
| Doohickey | 200      | 1-June-2015 | A 				|

### 1st task

Write an SQL query which returns a single metric indicating how well actuals met forecast for a given week.  What assumptions did you make?

### 2nd task

Given Truck A arrives at a random time between 9am and 11am, and Truck B arrives at a random time between 10am and 12am.  What are the Odds that Truck A arrives before Truck B?  Why?