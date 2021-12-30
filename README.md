# StereoVision
Bem vindo! Este repositório contém o meu trabalho de graduação!

## Descrição

O trabalho consiste em hardware e software de um sistema de visão estéreo, que é utilizado para estimativa de posição no espaço de um padrão de círculos. O padrão de círculos é preso a um VANT e pode-se, assim, utilizar a posição como entrada para um sistema de controle.

## Estrutura

O software é composto por 4 módulos, que são:

0.CapturaImagens.py: Módulo de captura de imagens utilizadas para calibração. São capturados o número de imagens especificado, com intervalo de 5 segundos entre elas.

1.CalibraIntrinsecos.py: Módulo de calibração de parâmetros intrínsecos. Deve ser executado uma vez para cada câmera. Tem como saida arquivos CSV com matriz da câmera e vetor de coeficientes de distorção.

2.CalibraExtrínsecos.py: Módulo de calibração de parâmetros extrínsecos. Deve ser executado uma vez para o par de câmeras. Tem como saira as matrizes de projeção para retificação dos pontos

3. TriangulaPontos.py: Módulo de triangulação de pontos,  exibição de medições e exportação de medições. Tem como entrada os .CSV exportados pelos outros módulos, com os parâmetros intrínsecos e extrínsecos do sistema estéreo e utiliza a biblioteca Panda3D para visualização.
