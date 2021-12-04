import cv2
import numpy as np
import pandas as pd

# Variaveis de entrada
tabuleiro = (9,7) # Formato do tabuleiro: (maior,menor)

intrinsecos = [pd.read_csv('cam0_intrinsecos.csv').to_numpy(),
               pd.read_csv('cam1_intrinsecos.csv').to_numpy()]
dist = [pd.read_csv('cam0_distorcoes.csv').to_numpy(),
        pd.read_csv('cam1_distorcoes.csv').to_numpy()]

# Declara vetor de pontos no tabuleiro (1 casa = unidade)
pts_tabuleiro = np.zeros((1,tabuleiro[0]*tabuleiro[1], 3), np.float32)
pts_tabuleiro[0,:, :2] = np.mgrid[0:tabuleiro[0], 0:tabuleiro[1]].T.reshape(-1,2)
pts_tabuleiro = 22*pts_tabuleiro
