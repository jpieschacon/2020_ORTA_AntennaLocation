# Antenna Location Problem

Let us consider a set of squared cells, each one characterized by a different demand R<sub>mn</sub>. We can
install the antennas in the vertexes of each cell. Hence, the possible locations are the ones shown
below. Each antenna absorbs demand by all the four cells that share the vertex in which the
antenna is located.

![Problem description](images/problemDescription.PNG)

If more antennas cover a cell (as below) R<sub>mn</sub> is equally divided among all the antennas.

Each antenna has a maximum capacity that must not be exceeded Q<sub>ij</sub> and an installation cost c<sub>ij</sub>.
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

With the objective of visualizing the given solution for every instance and test, a script that generates a graph was created. One of the generated images is ilustrated below. The green dots symbolize that the antenna was installed, while the red represent the non-installation of them. 

In every vertex, it is indicated the installation cost (c), the portion of capacity given (q), and the total capacity (Q) of each antenna. The demand required by each cell is depicted in the center of every four adjacent antennas.

![Graph problem](images/graph.png)
### /heuristic/simpleHeu.py
This file contains all the methods used for all the heuristic algorithms. The constructor method defines the attributes for this class, in this case, the problem definition(prb), all the instance parameters (dict_data) and the maximum cost for the instance.

The **solveRandom** method implements the random heuristic algorithm described in **Section 5.1**, the input parameter N_iter is the maximum number of iterations.

The **solveRandomPDF** method corresponds to the PDFT1 and PDFT2 heuristic algorithm described in **Sections 5.2** and **5.3**, respectively. The input parameters are the maximum number of iterations and the probability type (prob_type). This method uses the **defineProbabilities** method that computes the three probabilities for each antenna and return the probability matrix according with PDFT1 and PDFT2.

 The **solve_N21** and **solve_12N** methods implement the **N to 1(N21)** and **1 to N(12N)** heuristic algorithms described in **Section 5.4** and **5.5**, both method receive as input parameter the maximum number of iterations.  
 
 The **validateFeasibility** method is used for all the heuristic methods to validate the feasibility of a new possible solution, the input parameters are the new possible solution(newSol), the actual best solution(sol_x), the actual solution for q(sol_q) and the cost of the best solution. The method defines the variable values according to the input parameters and compute the value for the variables z, q_SE, q_SW, q_NE, q_NW and q, then each constraint is validated, if some constraint is not met then the possible solution is classified as unfeasible and the constraint name, that it is not met, are returned. If the solution meets all constraints and if the cost is less than the best cost parameter, then the solution and cost are updated and the new solution is returned.
 
 The **destroyAndRebuild** implements the Destroy and Rebuil algorithm described in **Section 5.6**

### /simulator/instance.py
instance.py has the task to generate every instance for each one of the tests. The constructor of the class Instance() receives all the parameters included in the configuration file *config.json*.
The method get_data() returns the instance more relevant information, the demand *R*, the total capacity *Q*, the cost *C*, number of grid rows *ar*, and the number of grid columns *ac*.

The methods distribution_uniform(), distribution_gauss(), and realistic() are only called if the parameter "distribution" in *config.json* is correctly entered.
These methods define how the instances for demand *R*, total capacity *Q*, and the cost *C* are going to be constructed making use also of the configuration parameters: "antenna_row",	"antenna_column", "max_capacity", "min_capacity", "max_demand", "min_demand", "max_cost", and "min_cost". 
Further explanation of how instances where created can be found in Section 4 of the report.
### main.py
This script executes the solver and the heuristic methods for only one instance. The solver's maximum execution time in seconds, the number of iterations of the heuristic algorithms and the output file path to collect the results are set at the beggining of the script as folows:
```bash
    time_limit = 60*60  # maximum execution time in seconds
    iter_number = 1000  # Max number of iteration for each heuristic algorithm
    output_file = "./results/exp_general_table.csv"  # output file
```
After the execution of this script it is possible to see in console the total cost and the consumed time for each method. Moreover, the graphs with the instance and the solution of each method are generated and stored in results/Figures/Instances.
### mainIter.py
In this script, the seeds and dimensions of the grid are varied. In addition to the execution time and number of iterations, the parameters to be set are the maximun and minimum number of columns and rows, and the number of seeds. 
```bash
   seeds_number = 10  # Number of seeds
    row_min = 3  # Minimum number of rows
    row_max = 10  # Maximum number of rows
    column_min = 3  # Minimum number of columns
    column_max = 10  # Maximum number of columns
```
The solutions are generated with the solver and all the heuristic methods for all dimensions (within the established limits) for each seed, and stored in a csv file.
### mainIterDistro.py
This script is used in **Section 6.4**, the objective is to evaluate the system's behavior feeding it with various instances c<sub>ij</sub>, Q<sub>ij</sub> and R<sub>mn</sub>, simulating in this way several real-world scenarios, using different distributions.
The **distros** variable contains the three possible distributions, also the number of seeds, row_min and row_max variables can be defined. The script will iterate for each distribution, using different instance sizes and different seeds. 

The output results will be saved in the **/results/exp_general_table_distros.csv** file.


```bash
time_limit = 2*60*60  # maximum execution time in seconds
output_file = "./results/exp_general_table_distros.csv"  # output file
distros = ['uniform', 'normal', 'realistic']
seeds_number = 10  # Number of seeds
row_min = 3  # Minimum number of rows
row_max = 10  # Maximum number of rows
```

### mainIterHeuristic.py
In this code, a variation of the number of iterations of the heuristic algorithms is made for different values of the seed. The values of the number of iteration are defined as:
```bash
iterations = [5, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
```
For each seed, the the heuristic methods are executed with each of the values of the iterations vector.
### mainIterRatio.py
One of the formulated hypothesis was that the ratio between the traffic demand Rmn and the total capacity of the antenna Qij affected the solver’s time execution to compute the optimal problem, tihs scenario is described in **Section 6.3**. This script iterates over different instance sizes, different seeds and increases the traffic demand from 1 to the maximum capacity of the antennas.

The output results will be saved in the **/results/exp_general_table_ratio_NxN.csv** file.

### mainSolverStd.py


In this script, the seeds of the grid are varied. For each seed, the solver is executed a define number of iterations that is set in iternumber. Finally, the solution is stored in a csv file.

```bash
    seeds_number = 30  # Number of seeds
    iterNumber = 100
```


### graphResults.py
graphResults.py was created to plot all of our results, the class Plot() includes the methods: plot3Dbar, plot2D, plot2DIter, plot2Ddistros, plot2DRatio, and plotBox. The constructor of Plot() only needs as input the path of the data that is intended to be processed and plotted. The result of each graph is stored in the path results/Figures. 
The method plot3Dbar only receives as input the z axis title, and plots the execution time and objective function of every heuristic w.r.t. the solver (Results depicted in Test 1 Section 6.1).  
The method plot2D does not have any input argument, plots the execution time vs the dimensions of the grid of the solver and every heuristic method (Results depicted in Test 1 Section 6.1). 
The method plot2DIter does not have any input argument, plots the total cost ratio vs the number of iterations or plots the execution time vs the number of iterations of every heuristic having as reference the solver (Results depicted in Test 2 Section 6.2).
The method plot2Ddistros does not have any input argument, plots the execution time vs the NxN grid dimensions comparing the different proposed input instances (Results depicted in Test 4 Section 6.4).
The method plot2DRatio does not have any input argument, plots the execution time vs the ratio between R<sub>mn</sub> and Q<sub>ij</sub> for different NxN grid instances (Results depicted in Test 3 Section 6.3).
The method plotBox does not have any input argument, plots the descriptive analysis of running the solver for a given number of iterations for a same seed (Results depicted in Test 5 Section 6.5).  



