CH_Prof = {
    'Johanna': {'Niv1': 30, 'Niv2': 30},
    'Merhan': {'Bodywork': 60, 'LadyStyling': 60, 'AtChor': 60, 'Intensif': 55},
    'Samuel': {'Niv1': 55, 'Niv2': 55, 'AtChor': 55, 'Intensif': 55}
}

CH_Salle = {
    'Orpheon': {'Niv1': 17, 'Niv2': 17},
    'StEtMtLc': {'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0},
    'Assurance': {'Niv1': 0.51, 'Niv2': 0.51, 'Bodywork': 0.51, 'LadyStyling': 0.51}
}

CU_Déplacement = {
    'Johanna': {'Niv1': 0, 'Niv2': 0},
    'Merhan': {'Bodywork': 10, 'LadyStyling': 10, 'AtChor': 10, 'Intensif': 10},
    'Samuel': {'Niv1': 0, 'Niv2': 0, 'AtChor': 0, 'Intensif': 0}
}

cours_data = {
    'Nb': {'Niv1': 33, 'Niv2': 33, 'Bodywork': 15, 'LadyStyling': 15, 'AtChor': 10, 'Intensif': 10},
    'Durée': {'Niv1': 1.5, 'Niv2': 1.5, 'Bodywork': 1, 'LadyStyling': 1.5, 'AtChor': 2, 'Intensif': 6},
    'Total': {}
}

AddBudget = {k: 0 for k in cours_data["Nb"]}