# TSP-hillclimbing
Traveling Salesperson Problem with Hill Climbing 🗺️
This project solves the Traveling Salesperson Problem (TSP) using the Hill Climbing Algorithm, presented through an website built with Streamlit.
The goal of the TSP is to determine the shortest possible route that visits a set of cities exactly once and returns to the starting point.
It takes me 2 days to develop this webpage...since i got an intrest in python and web development...I explored how can I develop web using python
# Python modules used:
Streamlit,mysql.connector,random,ast
# Platforms used for developing:
Before running the code install the modules in cmd prompt using command
       pip install streamlit  etc....
PYTHON IDLE(3.12)
Cmd prompt for running the code
# Features
It provides the best neighbour and best route length after a several calculations and for the easy view of the data, results are stored in MySQL table.
# How it works
This hill climbing algorithm works by generating a initial random solution(using random modoule)
It iteratively improves the solution by making small adjustments, like swapping cities to decrease the distance.
The process stops once no further improvement is found and it results in a locally optimal solution.



