import game_functions as gf
import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # 初始化并创建一个屏幕对象
	pygame.init()
	ai_settings = Settings()#使用Settings类
    #用display.set_mode()返回的screen表示整个背景图
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
    #创建一个海绵宝宝
	ship = Ship(ai_settings,screen)
    #创建一个子弹编组
	bullets = Group()
    #创建一个痞老板编组
	aliens = Group()
	gf.create_fleet(ai_settings,screen,ship,aliens)
    #创建一个用于储存游戏统计信息的实例
	stats = GameStats(ai_settings) 
	#创建计分板·
	sb = Scoreboard(ai_settings,screen,stats)
	#创建play按钮
	play_button = Button(ai_settings,screen,'play')
    # 游戏的主循环
	while True:
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets)
			bullets.update()
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

		gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
  
        
  
        
    
        

run_game()

