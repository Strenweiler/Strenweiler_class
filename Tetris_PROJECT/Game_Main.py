import Def_SHAPE_TEMPLATE as DST
import Primary_Function as PF
import random, time, pygame, sys
from pygame.locals import *
import Beginning_end as BE


def main():
    """游戏主进程"""
    #声明全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    
    #初始化pygame
    pygame.init
    
    #创建了一个 Pygame 的时钟对象，用于控制游戏的帧率。
    FPSCLOCK = pygame.time.Clock()
    
    #初始化窗口
    DISPLAYSURF = pygame.display.set_mode ((PF.WINDOW_WIDTH,PF.WINDOW_HEIGHT))
    
    #用于设置游戏中两种字体的大小
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf',100)
    
    #设置窗口标题
    pygame.display.set_caption('俄罗斯方块')



    while True:
        BE.run_game()
        BE.ShowTextScreen('Game Over')

    



