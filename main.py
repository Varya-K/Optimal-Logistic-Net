from datetime import datetime
 
import numpy as np
 
from Generator import GenerateData, generate
from NetProductPath import NetProducts
from Solver import SolveMILP_Edge
from VNS import VNS
from Write import SaveResult

def RunVNS(folder, savingFolder, maxSolvingTime, vehicleCapacity):
    net = NetProducts(vehicleCapacity, folder)
    if net.storageCount > 0:
        vns = VNS(net)
        vns.Solve(maxSolvingTime)
        SaveResult(savingFolder, vns.data, vns.result)
        print("Result:", vns.result.resultPrice)
        print("Solving time:", vns.result.solvingTime)
 
 
def RunVNSAndMILP(folder, savingFolder, maxSolvingTime, vehicleCapacity):
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
    print("Optimal Result:", MILPSolution.resultPrice)
 
    with open(savingFolder + "/data.txt", "w", encoding="utf-8") as f:
        f.write(f"result price = {vns.result.resultPrice}\n")
        f.write(f"time-limited MILP result price = {MILPSolution.resultPrice}\n")
        f.write(f"init price = {vns.initRes}\n")
        f.write(f"solving time = {vns.result.solvingTime}\n")
 
 
def GenerateGraphs(folder):
    graphs_to_generate = {10: 10, 20: 7, 30: 7, 50: 5, 100: 3, 150: 1}
    for storage_count, graphs_count in graphs_to_generate.items():
        for i in range(1, graphs_count + 1):
            generate(
                GenerateData(storage_count, np.random.randint(1, 1000)),
                f"{folder}/{storage_count}_nodes_{i}"
            )
            
    
def main():
    folder = "Generated_Data/Real_Graph/"
    save = "Results/Real_Graph/VNS1/"
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
    for region in regions:
        print("Start", region)
        RunVNSAndMILP(folder+region,save+region,None,50)

if __name__ == "__main__":
    main()
