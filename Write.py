import os

import pandas as pd

from Solver import SolverResult, SolverResultEdge


def SaveResult(folder, data, result: SolverResult):
    os.makedirs(folder, exist_ok=True)

    rows = [
        {
            'src': data[productId][pathI].path[0],
            'dst': data[productId][pathI].path[-1],
            'volume': round(volume, 6),
            'path_nodes': list(map(int, data[productId][pathI].path))
        }
        for productId, paths in result.productPathFlow.items()
        for pathI, volume in paths.items()
    ]
    pd.DataFrame(rows).to_csv(folder + "/result.csv", index=False, encoding='utf-8')

    vehicles = [
        {"edge_src": edge[0], "edge_dst": edge[1], "vehicle": int(vehicle)}
        for edge, vehicle in result.edgeVehicleCount.items()
    ]
    pd.DataFrame(vehicles).to_csv(folder + "/EdgeVehicleCount.csv", index=False, encoding='utf-8')

    with open(folder + "/data.txt", "w", encoding="utf-8") as f:
        f.write(f"result price = {result.resultPrice}\n")
        f.write(f"solving time = {result.solvingTime}\n")


def SaveResultEdge(folder, result: SolverResultEdge):
    os.makedirs(folder, exist_ok=True)

    pd.DataFrame(result.edgeProductFlow).to_csv(folder + "/EdgeProductFlow.csv", index=False, encoding='utf-8')
    pd.DataFrame(result.edgeVehicleCount).to_csv(folder + "/EdgeVehicleCount.csv", index=False, encoding='utf-8')

    with open(folder + "/results.txt", "w", encoding="utf-8") as f:
        f.write(f"result price = {result.resultPrice}\n")
        f.write(f"round result price = {result.resultPriceRound}\n")
        f.write(f"solving time = {result.solvingTime}\n")