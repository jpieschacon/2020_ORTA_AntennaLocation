# Antenna Location Problem

Let us consider a set of squared cells, each one characterized by a different demand R<sub>mn</sub>. We can
install the antennas in the vertexes of each cell. Hence, the possible locations are the ones shown
below. Each antenna absorbs demand by all the four cells that share the vertex in which the
antenna is located.

![Problem description](images/problemDescription.PNG)

If more antennas cover a cell (as below) R<sub>mn</sub> is equally divided among all the antennas.

Each antenna has a maximum capacity that must not be exceeded q<sub>ij</sub> and an installation cost c<sub>ij</sub>.
The objective is to minimize the total cost while covering all the demand.

## Scripts
### /etc/config.json(Config file)
Every instance generation needs configuration settings. The configured parameters will define the nature of the input instance.

| Variable | Description |
| ------------- | ------------------------- |
| antenna_row|     Number of rows of the grid |
| antenna_column|   Number of columns of the grid  |
| max_capacity|     Maximum capacity for each antenna |
| min_capacity|   Minimum capacity for each antenna|
| max_demand|    Maximum traffic demand for each cell|
| min_demand|    Minimum traffic demand for each cell |
| max_cost|      Maximum installation cost for each antenna |
| min_cost|     Minimum installation cost for each antenna |
 
```json
{
	"antenna_row":4, 
	"antenna_column":4,
	"max_capacity":40,
	"min_capacity":20,
	"max_demand":25,
	"min_demand":15,
	"max_cost":10000,
	"min_cost":8000,
	"distribution": "uniform"
}
```
There are three input instances:R<sub>mn</sub>,c<sub>ij</sub>, and q<sub>ij</sub>. The generation of these inputs is based on the specific test that will be performed to the exact and heuristic solutions. Moreover, each entry sample can be generated using different distributions.
For executing each script, the **config file must be modified** according with the defined input instance or each test.

### /graph/graph.py
JS
### /heuristic/simpleHeu.py
F
### /simulator/instance.py
instance.py has the task to generate every instance for each one of the tests. The constructor of the class Instance() receives all the parameters included in the configuration file *config.json*.
The method get_data() returns the instance more relevant information, the demand *R*, the total capacity *Q*, the cost *C*, number of grid rows *ar*, and the number of grid columns *ac*.

The methods distribution_uniform(), distribution_gauss(), and realistic() are only called if the parameter "distribution" in *config.json* is correctly entered.
These methods define how the instances for demand *R*, total capacity *Q*, and the cost *C* are going to be constructed making use also of the configuration parameters: "antenna_row",	"antenna_column", "max_capacity", "min_capacity", "max_demand", "min_demand", "max_cost", and "min_cost". 
Further explanation of how instances where created can be found in Section 4 of the report.
### main.py
This script will execute the solver and the heuristic methods for only one instance, 
### mainIter.py
L
### mainIterDistro.py
F
### mainIterHeuristic.py
L
### mainIterRatio.py
F
### mainSolverStd.py
JS
### graphResults.py
graphResults.py was created to plot all of our results, the class Plot() includes the methods: plot3Dbar, plot2D, plot2DIter, plot2Ddistros, plot2DRatio, and plotBox. The constructor of Plot() only needs as input the path of the data that is intended to be processed and plotted. The result of each graph is stored in the path results/Figures. 
The method plot3Dbar only receives as input the z axis title, and plots the execution time and objective function of every heuristic w.r.t. the solver (Results depicted in Test 1 Section 6.1).  
The method plot2D does not have any input argument, plots the execution time vs the dimensions of the grid of the solver and every heuristic method (Results depicted in Test 1 Section 6.1). 
The method plot2DIter does not have any input argument, plots the total cost ratio vs the number of iterations or plots the execution time vs the number of iterations of every heuristic having as reference the solver (Results depicted in Test 2 Section 6.2).
The method plot2Ddistros does not have any input argument, plots the execution time vs the NxN grid dimensions comparing the different proposed input instances (Results depicted in Test 4 Section 6.4).
The method plot2DRatio does not have any input argument, plots the execution time vs the ratio between R<sub>mn</sub> and Q<sub>ij</sub> for different NxN grid instances (Results depicted in Test 3 Section 6.3).
The method plotBox does not have any input argument, plots the descriptive analysis of running the solver for a given number of iterations for a same seed (Results depicted in Test 5 Section 6.5).  

```bash
python -m parlai.scripts.eval_model -m ir_baseline -t personachat -dt valid
```

