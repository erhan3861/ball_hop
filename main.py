import play
import os
import time
import winsound

play.set_backdrop('black')

balls = []
coor_list = []
exp_list = []

for i in range(5):
    exp = play.new_image("img" + str(i) + ".gif")
    exp.hide()
    exp_list.append(exp)


@play.repeat_forever
def explode_sound(ball):

    winsound.PlaySound("patlama.wav", winsound.SND_ASYNC)

    coor_list.clear()
    coor_list.append(ball.x)
    coor_list.append(ball.y)
    coor_list.append("new_ball")


@play.when_mouse_clicked
def make_ball():
    for ball in balls:
        if play.mouse.is_touching(ball):
            return
    ball = play.new_circle(color=play.random_color(),
                           x=play.mouse.x, y=play.mouse.y, radius=20)

    ball.start_physics(bounciness=0.5, mass=100, friction=1)
    ball.is_being_dragged = False

    explode_sound(ball)

    @ball.when_clicked
    def click_ball():
        ball.is_being_dragged = True
        ball.color = play.random_color()

    @play.mouse.when_click_released
    def release_ball():
        for ball in balls:
            ball.is_being_dragged = False

    balls.append(ball)


@play.when_key_pressed('z')
def press_key(key):
    explode_sound(balls[0])
    for ball in balls:
        ball.physics.y_speed = play.random_number(80, 100)
        ball.physics.x_speed = play.random_number(-30, 30)


@play.repeat_forever  # sürekli tekrarla
def loop():
    for ball in balls:
        if ball.is_being_dragged:
            ball.physics.x_speed = play.mouse.x - ball.x
            ball.physics.y_speed = play.mouse.y - ball.y


@play.repeat_forever  # sürekli tekrarla
async def explode():
    print(coor_list)
    for i in exp_list:
        if "new_ball" in coor_list:
            i.go_to(coor_list[0], coor_list[1])
            i.show()
            await play.timer(seconds=0.1)
            i.hide()

    if "new_ball" in coor_list:
        coor_list[2] = "old_ball"

    # await play.animate()


play.start_program()
