# GmE 205: Laboratory 6 
## From UML Class Diagram to Python Code

### *Description*
This project aims to demonstrate how a UML diagram can be translated into Python code using object-oriented design to define the different classes required in the model.

### *Dependencies*
* Python 3.14
* Visual Studio Code
* shapely
* Folium
* NetworkX
* osmnx

### *Part B Summary*
In the Lecture 6 case study, `SpatialObject` serves as the base class, which provides different functions, such as `distance_to()`and `intersects()`The subclasses `Parcel`, `Road` and `Building`inherit these functions or methods, while also extending the base class with their own specific attributes, such as height, length, and area. These shared methods allow all spatial object classes to compute distances and verify overlapping areas consistently, without the need to repeat the same code. The relationships in the case study show how spatial and socioeconomic entities connect to form a complete model. `Buildings` object are linked to `Parcels`, which denotes that a building is located inside a specific parcel. `Households` are also associated with `Buildings`, which indicates that households reside within buildings, and each building keeps a list of its households. Lastly, `Road` is connected to `Parcel` to check their adjacency. These relationships create a network of interactions among classes while maintaining clear responsibilities for each.<br>

### *Part C Summary*
The UML diagram saved in `uml/own_uml.jpg` was translated into a code by defining classes for the spatial accessibility problem. These include `SpatialObject`, `Dormitory`, `HealthcareFacility`, `Road`, `TransportNetwork`, and `AccessibilityResult`, which represent a distinct entity in the model. Each class contains specific attributes, such as `geometry`, `name`, `facilityType`, `length`, `travelSpeed`, `distance`, and `travelTime`, which describe the nature of the object. To define behavior, methods such as ``classifyAccessibility()`, `findNearestFacility()`, `getTravelTime()`, `calculateDistance()`, and `describeRoute()` were implemented and performed these actions that are only consistent or lies within their roles. As the relationship of the classes were established, the hardest relationship to implement was those involving `Route` and `TransportNetwork`, due to the integration of graph-based logic and the dependency of one class on the results of another. The UML presented a structured concept that was succeessfully turned into a functional and accurate code.<br>

### *UML Evidence*
My UML diagram is stored at: `uml/own_uml.jpg`


### *Reflection*
1. **Why does SpatialObject own geometry?** <br>
The base class `SpatialObject` owns the geometry because it represents spatial attributes that are shared by all spatial entities. Geometry contains coordinates that define the position and shape of each object, which will make it a core property in calculating distance and intersection. By placing the geometry in the base class, all subclasses will inherit this significant feature and will avoid duplication of codes across different classes. It ensures that spatial data is stored and accessed. <br>

2. **Why should `distance_to()` not be rewritten in every subclass?** <br>
`distance_to()` should not be rewritten in every subclass because the logic for computing Euclidean distance is mathematically universal, which means that the distance calculation between two points in space follows the same rule, whether the object is a dormitory, road, or facility. If this function is rewritten in every subclass, it will introduce redundancy and `god functions`. Writing `distance_to()` in the base class ensures that all subclasses will inherit a single and reliable implementation of this function, which probidess consistency and makes it easier to debug across the entire hierarchy.<br>

3. **How does this support abstraction and reuse?** <br>
The base class `SpatialObject` encapsulates the shared spatial operations so that subclasses do not need to duplicate these functions. For instance, `distance_to()` provides the same calculation manner of distance, in which subclasses can directly call it without explicitly redefining the formula.   `distance_to() can easily work within a new created class, as `SpatialObject` already handles the math operation. This abstraction hides the implementation details while showing a consistent method or function that other classes can reuse. Reusing can prevent duplication of the same formula across all classes, since they automatically inherit these shared spatial operations.<br> 

4. **Did I include the important attributes?** <br>
 After implementing the different case study classes, the important attributes for each class are included in the code. The subclass `Building` has its unique identifier, usage, height, and connections to parcels and households for spatial analysis. The subclass `Parcel` also contains  unique identifier, area, zoning, and adjacency to roads and buildings for land class modelling. Moreover, the subclass `Road` has also its unique identifier, road type, length, and adjacency to parcels for connectivity and accessibility analyses. Lastly, the class `Household`, which is a non-spatial object, contains population size, income, tenure type, and its association to buildings as a core socioeconomic attribute.<br>

5. **Did I place them in the correct class?**<br>
Each attribute is correctly placed in their corresponding class. For instance, socioeconomic attributes, such as income and tenure type, are placed under the class `Household`, while specific details, such as height and usage, correctly belong to the class `Building`. Furthermore, the class `Parcel` exhibits land characteristics, while the class `Road` represents transportation features, which are all placed and assigned to their respective classes.<br>

6. **Did I avoid putting unrelated data into this object?**<br>
While checking all the attributes, unrelated data were avoided in these objects. It shows that the `Building` class does not contain road networks or other land characteristics, which are handled by the `Road` and `Parcel` classes, respectively. The `Parcel` class does not contain any household-level data. This separation of concerns makes the classes clean and easier to maintain and debug.<br>  

7. **What was easier to translate into code: attributes, methods, or inheritance?**<br>
It is easier to translate attributes into code because they are straightforward data fields like `facilityType`, `distance`, `travelTime`, `roadType`, and other attributes that define the classes. Methods under each class require logic in order for it to work, such as `distance_to()`and `classifyAccessibility`. Inheritance is also easier since the base class `SpatialObject` provides a clear structure for reusee and sharing with other subclasses. When implementing methods, I encountered difficulty in correctly making them interact with other classes, such as the `Route` class calling the `TransportNetwork` class.<br>

8. **Which relationship in your UML was hardest to implement?**<br>
The hardest relationship in my UML to implement was between the `Route` and `TransportNetwork` classes. Any changes made in `TransportNetwork` might also affect `Route` and `main_own_model.py`. This relationship required integrating a shortest path algorithm from the `TransportNetwork` library and ensuring that nodes and edges were correctly represented in the `TransportNetwork` class that is used by the `Route` class. Since `Route` depends on these computations to generate paths and travel times, any changes in `TransportNetwork` directly affect how the `Route` class functions, as well as in the overall `.py` model.  The relationship between these two classes involves dynamic and graph computation. It also requires the correct and accurate representation of road attributes like travel time and length to produce realistic outputs.  

9. **Did your code exactly match your UML, or did you revise some parts during implementation?**<br>
The code I developed did not exactly match my UML. Some parts were revised during implementation. When I initially translated my UML into code, it only computed Euclidean distance without considering real-life road networks, which resulted in inaccurate results and map representation. To improve the results, additional methods were added to the `TransportNetwork` class, such as `get_path_roads`, to fully support route descriptions. Minor adjustments were also made to ensure compatibility with the `NetworkX`and `Folium` libraries.

10. **What did you learn about the importance of OOAD from this exercise?**<br>
This exercise highlighted the importance of OOAD in structuring complex systems. OOAD ensures that responsibilities are clearly assigned to different objects or classes, which prevents data and logic from being tangled or resulting in `god functions` or `god objects`. It provides a clear direction of the workflow, which makes it easier to translate concepts into codes. It also allows new features like additional facility or functions to be added easily. The system becomes easier to maintain and debug. Overall, OOAD serves as the blueprint of the system, which guides the transition of concepts into organized and working codes.


## Author
Maria Graciella L. Roque  
Discord:[@grachiebob]

## Acknowledgements
* GmE 205 Laboratory Exercise 6 Manual
* [MarkDown](https://www.markdownguide.org/cheat-sheet/)

Edited on VS Code