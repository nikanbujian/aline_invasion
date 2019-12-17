import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

#储存游戏的主要函数
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	for event in pygame.event.get():#不断检测是否有事件发生
			if event.type == pygame.QUIT:
				sys.exit()#退出游戏
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event,ai_settings,screen,ship,bullets)
			elif event.type == pygame.KEYUP:
				check_keyup_events(event,ship)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_settings,screen,stats,sb,play_button,
				    ship,aliens,bullets,mouse_x,mouse_y)

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings,screen,ship)
			bullets.add(new_bullet)
						
def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	   
                
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	screen.fill(ai_settings.bg_color)#设置背景颜色
	#显示得分
	sb.show_score()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()#将飞船绘制到屏幕上
	aliens.draw(screen)

	# 让最近绘制的屏幕可见 不断刷新
	
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#响应子弹和外星人发生碰撞
	collisions = pygame.sprite.groupcollide(bullets,aliens,False,True)
	if len(aliens) == 0:
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ai_settings.increase_speed()
		#提高一个等级
		stats.level += 1
		sb.prep_level()
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)

def create_fleet(ai_settings,screen,ship,aliens):
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,
	    alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,
			    row_number)
		
		
def get_number_aliens_x(ai_settings,alien_width):
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	alien.rect.x = alien.x
	aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y = (ai_settings.screen_height - 
	                        (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
	aliens.update()
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
	for alien in aliens:
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
			
def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
			break

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
		
	if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		#重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
def check_high_score(stats,sb):
	#检查是否诞生了最高分
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
