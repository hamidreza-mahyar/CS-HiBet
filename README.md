# Compressive Sensing of High Betweenness Centrality Nodes in Networks

This is the code produced as part of the paper _Compressive Sensing of High Betweenness Centrality Nodes in Networks_ 

> "Compressive Sensing of High Betweenness Centrality Nodes in Networks"
> Hamidreza Mahyar, Rouzbeh Hasheminezhad, Elahe Ghalebi, Ali Nazemian, Radu Grosu, Ali Movaghar, and Hamid R. Rabiee. Physica A: Statistical Mechanics and its Applications, vol. 497, pp. 166-184, May 2018. DOI: 10.1016/j.physa.2017.12.145. [Link](https://www.sciencedirect.com/science/article/pii/S0378437117313948)

## Packages needed

 - `networkx 2.0`
 - `numpy 1.15.0`
 - `igraph 0.1.11`
 - `cvxpy 1.0.6`

## Experiment execution

Running experiments:

### `Main.py`

This script is used for running CS-HiBet method. Inputs are the network, the required number of measurements, the measurements step size, and the sparsity level. Output is the actual values of Betweenness centrality for the network nodes and the estimated values by CS-HiBet, which will be stored in the `./result` folder. 

### `Test_F-measure.py`

This script is used for running an experiment on the accuracy of CS-HiBet for the number of correctly identified top-k betweenness centrality nodes in networks for varying sparsity percentage. The sparsity leverl should defined in the script.

### `Test-RankDistance.py`

This script is used for running an experiment on the accuracy for the distance between top k ranks assigned by CS-HiBet and those determined by the global betweenness centrality.
