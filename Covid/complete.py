from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import random
import smtplib
import time
import math
import pygame
from pygame.locals import *

def game(username):

    username = username
    def corona():
        acc=[0,0]
        arrows=[]
        badtimer=100
        badtimer1=0
        badguys=[[1000,100]]
        healthvalue=194
        pygame.mixer.init()
        running = 1
        exitcode = 0

        while running:
            badtimer-=1
            screen.fill(0)
            for x in range (int(width/grass.get_width()+1)):
                for y in range (int(height/grass.get_height()+1)):
                    screen.blit(grass,(x*100,y*100))
            screen.blit(man1,(0,150))
            screen.blit(man3,(0,300))
            screen.blit(man2,(0,450))
            screen.blit(man4,(0,600))
            screen.blit(medicine,(244,70))
            screen.blit(grocery,(192,240))
            screen.blit(grocery,(544,640))
            position = pygame.mouse.get_pos()
            angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
            playerrot = pygame.transform.rotate(player, 360-angle*57.29)
            playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
            screen.blit(playerrot, playerpos1)
            pygame.display.flip()

            for bullet in arrows:
                index=0
                velx=math.cos(bullet[0])*20
                vely=math.sin(bullet[0])*20
                bullet[1]+=velx
                bullet[2]+=vely
                if bullet[1]<-64 or bullet[1]>1100 or bullet[2]<-64 or bullet[2]>750:
                    arrows.pop(index)
                index+=1
                for projectile in arrows:
                    arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                    screen.blit(arrow1, (projectile[1], projectile[2]))

            if badtimer==0:
                badguys.append([1100, random.randint(50,700)])
                badtimer=100-(badtimer1*2)
                if badtimer1>=35:
                    badtimer1=35
                else:
                    badtimer1+=5
            index=0
            for badguy in badguys:
                if badguy[0]<-64:
                    badguys.pop(index)
                badguy[0]-=7

                badrect = pygame.Rect(badguyimg.get_rect())
                badrect.top=badguy[1]
                badrect.left=badguy[0]
                if badrect.left<64:
                    hit.play()
                    healthvalue -= random.randint(5,20)
                    badguys.pop(index)
                
                index1=0
                for bullet in arrows:
                    bullrect=pygame.Rect(arrow.get_rect())
                    bullrect.left=bullet[1]
                    bullrect.top=bullet[2]
                    if badrect.colliderect(bullrect):
                        enemy.play()
                        acc[0]+=1
                        badguys.pop(index)
                        arrows.pop(index1)
                    index1+=1
                # 6.3.1 - Next Bad Guy
                index+=1
            for badguy in badguys:
                screen.blit(badguyimg, badguy)

            # 6.5 - Draw health bar
            screen.blit(healthbar, (5,5))
            for health1 in range(healthvalue):
                screen.blit(health, (health1+8,8))

            # 7 - update the screen
            pygame.display.flip()

            # 8 - loop through the events
            for event in pygame.event.get():
                # check if the event is the X button
                if event.type==pygame.QUIT:
                    pygame.quit()
                # exit(0)
                    # if it is quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key==K_w:
                        keys[0]=True
                    elif event.key==K_a:
                        keys[1]=True
                    elif event.key==K_s:
                        keys[2]=True
                    elif event.key==K_d:
                        keys[3]=True

                if event.type == pygame.KEYUP:
                    if event.key==pygame.K_w:
                        keys[0]=False
                    elif event.key==pygame.K_a:
                        keys[1]=False
                    elif event.key==pygame.K_s:
                        keys[2]=False
                    elif event.key==pygame.K_d:
                        keys[3]=False

                if event.type==pygame.MOUSEBUTTONDOWN:
                    shoot.play()
                    position=pygame.mouse.get_pos()
                    acc[1]+=1
                    arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])

                # 9 - Move player
            if keys[0]:
                playerpos[1]-=5
            elif keys[2]:
                playerpos[1]+=5
            if keys[1]:
                playerpos[0]-=5
            elif keys[3]:
                playerpos[0]+=5

        #10 - Win/Lose check
            if pygame.time.get_ticks()>=60000:
                running=0
                exitcode=1
            if healthvalue<=0:
                running=0
                exitcode=0
            if acc[1]!=0:
                accuracy=acc[0]*1.0/acc[1]*100
            else:
                accuracy = 0
        if exitcode==0:
            return

    def chemist(order):
        layout = pygame.image.load("resources/images/chemist.jpg")
        layout = pygame.transform.scale(layout,(1000,700))
        screen.fill(0)
        for x in range (int(1100/layout.get_width()+1)):
            for y in range (int(750/layout.get_height()+1)):
                    screen.blit(layout,(x*100,y*100))

        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(700, 10, 200, 32)
        color_inactive = pygame.Color(255,255,255)
        color_active = pygame.Color(255,0,0)
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            order = order + text + " "
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            # Render the current text.
            screen.fill(0)
            for x in range (int(1100/layout.get_width()+1)):
                for y in range (int(750/layout.get_height()+1)):
                    screen.blit(layout,(x*100,y*100))
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()
            clock.tick(30)
        s = smtplib.SMTP('smtp.gmail.com', 587)  
        s.starttls() 
        s.login("relievedorder@gmail.com", "iitdelhi@1") 
        message = "Hello!"+"\n"+"you have received the following order\n"+order+"\nTamanna has placed the order from ADDRESS-ZZZZ"
        s.sendmail("relievedorder@gmail.com", "amirag2611@gmail.com", message) 
        s.quit() 
        return order

    def grocery1(order):
        layout = pygame.image.load("resources/images/grocery1.jpg")
        layout = pygame.transform.scale(layout,(1200,700))
        screen.fill(0)
        for x in range (int(1100/layout.get_width()+1)):
            for y in range (int(750/layout.get_height()+1)):
                    screen.blit(layout,(x*100,y*100))

        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(900, 10, 200, 32)
        color_inactive = pygame.Color(255,255,255)
        color_active = pygame.Color(255,0,0)
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            order = order + text + " "
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            # Render the current text.
            screen.fill(0)
            for x in range (int(1100/layout.get_width()+1)):
                for y in range (int(750/layout.get_height()+1)):
                    screen.blit(layout,(x*100,y*100))
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()
            clock.tick(30)
        s = smtplib.SMTP('smtp.gmail.com', 587)  
        s.starttls() 
        s.login("relievedorder@gmail.com", "iitdelhi@1") 
        message = "Hello!"+"\n"+"you have received the following order\n"+order+"\nTamanna has placed the order from ADDRESS-ZZZZ"
        s.sendmail("relievedorder@gmail.com", "garimak2611@gmail.com", message) 
        s.quit()
        return order

    def grocery2(order):
        layout = pygame.image.load("resources/images/grocery2.jpg")
        layout = pygame.transform.scale(layout,(1300,700))
        screen.fill(0)
        for x in range (int(1100/layout.get_width()+1)):
            for y in range (int(750/layout.get_height()+1)):
                    screen.blit(layout,(x*100,y*100))

        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(700, 10, 200, 32)
        color_inactive = pygame.Color(255,255,255)
        color_active = pygame.Color(255,0,0)
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            order = order + text + " "
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            # Render the current text.
            screen.fill(0)
            for x in range (int(1100/layout.get_width()+1)):
                for y in range (int(750/layout.get_height()+1)):
                    screen.blit(layout,(x*100,y*100))
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()
            clock.tick(30)
        s = smtplib.SMTP('smtp.gmail.com', 587)  
        s.starttls() 
        s.login("relievedorder@gmail.com", "iitdelhi@1") 
        message = "Hello!"+"\n"+"you have received the following order\n"+order+"\nTamanna has placed the order from ADDRESS-ZZZZ"
        s.sendmail("relievedorder@gmail.com", "r.singhal.com@gmail.com", message) 
        s.quit()
        return order

    def mailTouser(order):
        s = smtplib.SMTP('smtp.gmail.com', 587)  
        s.starttls() 
        s.login("relievedorder@gmail.com", "iitdelhi@1") 
        message = "Hello!"+"\n"+"you have placed the following order\n"+order+"\nkindly paty Rs.YY at XXXXXXXXXX"
        s.sendmail("relievedorder@gmail.com", username, message) 
        s.quit() 

    pygame.init()
    width, height = 1100,750
    screen = pygame.display.set_mode((width, height))
    keys = [False, False, False, False] #position of WASD keys
    playerpos=[100,100]
    pygame.mixer.init()


    # 3 - Load images
    player = pygame.image.load("resources/images/dude.png")
    grass = pygame.image.load("resources/images/khurja.jpg")
    man1 = pygame.image.load("resources/images/man1.jpg")
    man1 = pygame.transform.scale(man1,(100,100))
    man2 = pygame.image.load("resources/images/man2.jpg")
    man2 = pygame.transform.scale(man2,(100,100))
    man3 = pygame.image.load("resources/images/man3.jpg")
    man3 = pygame.transform.scale(man3,(100,100))
    man4 = pygame.image.load("resources/images/man4.jpg")
    man4 = pygame.transform.scale(man4,(100,100))
    arrow = pygame.image.load("resources/images/bullet.png")
    badguyimg1 = pygame.image.load("resources/images/badguy.png")
    badguyimg1 = pygame.transform.scale(badguyimg1,(100,100))
    badguyimg=badguyimg1
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    #gameover = pygame.image.load("resources/images/gameover.png")
    #youwin = pygame.image.load("resources/images/youwin.png")
    medicine = pygame.image.load("resources/images/medicine.png")
    medicine = pygame.transform.scale(medicine,(80,80))
    grocery = pygame.image.load("resources/images/grocery.jpg")
    grocery = pygame.transform.scale(grocery,(55,55))

    # 3.1 - Load audio
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    counter = 1
    while 1:
        screen.fill(0)
        for x in range (int(width/grass.get_width()+1)):
            for y in range (int(height/grass.get_height()+1)):
                    screen.blit(grass,(x*100,y*100))
        screen.blit(medicine,(244,70))
        screen.blit(grocery,(192,240))
        screen.blit(grocery,(544,640))
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1)
        pygame.display.flip()
        

        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                pygame.quit()
            # exit(0)
                # if it is quit the game
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_d:
                    keys[3]=True

            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_d:
                    keys[3]=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                shop = pygame.mouse.get_pos()
                
                if ((shop[0]>250) and (shop[0]<330) and (shop[1]>70) and (shop[1]<150)):
                    order = ''
                    order = chemist(order)
                    screen.fill(0)
                    for x in range (int(width/grass.get_width()+1)):
                        for y in range (int(height/grass.get_height()+1)):
                                screen.blit(grass,(x*100,y*100))
                    screen.blit(medicine,(244,70))
                    screen.blit(grocery,(192,240))
                    screen.blit(grocery,(544,640))
                    position = pygame.mouse.get_pos()
                    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
                    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
                    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                    screen.blit(playerrot, playerpos1)
                    pygame.display.flip()
                    mailTouser(order)
                
                if ((shop[0]>196) and (shop[0]<255) and (shop[1]>230) and (shop[1]<300)):
                    order = ''
                    order = grocery1(order)
                    screen.fill(0)
                    for x in range (int(width/grass.get_width()+1)):
                        for y in range (int(height/grass.get_height()+1)):
                                screen.blit(grass,(x*100,y*100))
                    screen.blit(medicine,(244,70))
                    screen.blit(grocery,(192,240))
                    screen.blit(grocery,(544,640))
                    position = pygame.mouse.get_pos()
                    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
                    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
                    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                    screen.blit(playerrot, playerpos1)
                    pygame.display.flip()
                    mailTouser(order)

                if ((shop[0]>544) and (shop[0]<615) and (shop[1]>630) and (shop[1]<700)):
                    order = ''
                    order = grocery2(order)
                    screen.fill(0)
                    for x in range (int(width/grass.get_width()+1)):
                        for y in range (int(height/grass.get_height()+1)):
                                screen.blit(grass,(x*100,y*100))
                    screen.blit(medicine,(244,70))
                    screen.blit(grocery,(192,240))
                    screen.blit(grocery,(544,640))
                    position = pygame.mouse.get_pos()
                    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
                    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
                    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                    screen.blit(playerrot, playerpos1)
                    pygame.display.flip()
                    mailTouser(order)

            # 9 - Move player
        if keys[0]:
            playerpos[1]-=5
        elif keys[2]:
            playerpos[1]+=5
        if keys[1]:
            playerpos[0]-=5
        elif keys[3]:
            playerpos[0]+=5

        r = random.randint(1,1000) 
        if(r==900):
            corona()



app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'login'
app.config['MONGO_URI'] = 'mongodb+srv://garima:gk2611@cluster0-vzf1a.azure.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username'] 
        game(username)
        return 'You are logged out as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=False)
