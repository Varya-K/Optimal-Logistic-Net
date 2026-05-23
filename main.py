from datetime import datetime
 
import numpy as np
 
from Generator import GenerateData, generate
from NetProductPath import NetProducts
from Solver import SolveMILP_Edge
from VNS import VNS
from Write import SaveResult

from Math import Bg

def RunVNS(folder, savingFolder, maxSolvingTime, vehicleCapacity):
    net = NetProducts(vehicleCapacity, folder)
    if net.storageCount > 0:
        vns = VNS(net)
        vns.Solve(maxSolvingTime)
        SaveResult(savingFolder, vns.data, vns.result)
        print("Result:", vns.result.resultPrice)
        print("Solving time:", vns.result.solvingTime)
 
 
def RunVNSAndMILP(folder, savingFolder, maxSolvingTime, vehicleCapacity, prev):
    net = NetProducts(vehicleCapacity, folder + "/")
    if net.storageCount == 0:
        return

    if maxSolvingTime is None:
        maxSolvingTime = 2 * net.storageCount * 60
    print("Limit time:", maxSolvingTime)
 
    vns = VNS(net)
    vns.Solve(maxSolvingTime)
    SaveResult(savingFolder, vns.data, vns.result)
    print("VNS Result:", vns.result.resultPrice)
    print("VNS Solving time:", vns.result.solvingTime)

    MILPSolution = SolveMILP_Edge(net, vns.result.solvingTime)
    print("Time-Limited Result:", MILPSolution.resultPrice)
 
    with open(savingFolder + "/data.txt", "w", encoding="utf-8") as f:
        f.write(f"VNS = {vns.result.resultPrice}")
        f.write(f"Rounded LP = {vns.result.initRes}")
        f.write(f"Time-limited MILP = {MILPSolution.resultPrice}")
        f.write(f"Solving time = {vns.result.solvingTime}")
 
 
def GenerateGraphs(folder):
    graphs_to_generate = {10: 10, 20: 7, 30: 7, 50: 5, 100: 3, 150: 1}
    for storage_count, graphs_count in graphs_to_generate.items():
        for i in range(1, graphs_count + 1):
            generate(
                GenerateData(storage_count, np.random.randint(1, 1000)),
                f"{folder}/{storage_count}_nodes_{i}"
            )
            
    
def main():
    regions = ["Denmark",
           "Belgium",
           "Netherlands",
           "Hungary",
           "Ohio_USA",
           "Georgia_USA",
           "Illinois_USA",
           "California_USA",
           "United Kingdom",
           "Sweden",
           "Italy",
           "Germany",
           "Texas_USA",
           "Spain",
           "Europe Russia"]
    graphs_to_generate = {10: 10, 20:7, 30:7, 50:5, 100:3, 150:1}

    for region in regions[12:]:
        print("Start", datetime.now(), region)
        RunVNSAndMILP("Generated_Data/Real_Graph/"+region, "Results/Real_Graph/"+region, None, 50)
    for storage_count, graphs_count in graphs_to_generate.items():
        for i in range(1, graphs_count+1):
            folder_name = str(storage_count)+"_nodes_"+str(i)
            print("Start", datetime.now(), folder_name)
            RunVNSAndMILP("Generated_Data/Synthetic/"+folder_name, "Results/Synthetic/"+folder_name, None, 50)
if __name__ == "__main__":
    main()
