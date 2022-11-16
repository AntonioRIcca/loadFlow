from PIL import Image, ImageDraw, ImageFont


def arrow(d, x, y, length):
    (x1, y1) = (x, y+length)
    d.line(((x, y), (x1, y1)), fill='black', width=3)
    d.polygon([(x1, y1+5), (x1-5, y1-5), (x1+5, y1-5)], fill='black')


def pwm(d, x, y):
    d.line(((x, y), (x, y + 25)), fill='black', width=3)
    d.line(((x, y + 75), (x, y + 100)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x + 15, y + 25)), fill='black', width=3)
    d.line(((x - 15, y + 75), (x + 15, y + 75)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x - 15, y + 75)), fill='black', width=3)
    d.line(((x + 15, y + 25), (x + 15, y + 75)), fill='black', width=3)
    d.line(((x + 15, y + 25), (x - 15, y + 75)), fill='black', width=3)
    pwm_font = ImageFont.truetype('arial', 18)
    d.text((x-10, y+25), '~', (0, 0, 0), font=pwm_font)
    d.text((x, y + 55), '=', (0, 0, 0), font=pwm_font)


def dcdc_conv(d, x, y):
    d.line(((x, y), (x, y + 25)), fill='black', width=3)
    d.line(((x, y + 75), (x, y + 100)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x + 15, y + 25)), fill='black', width=3)
    d.line(((x - 15, y + 75), (x + 15, y + 75)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x - 15, y + 75)), fill='black', width=3)
    d.line(((x + 15, y + 25), (x + 15, y + 75)), fill='black', width=3)
    d.line(((x + 15, y + 25), (x - 15, y + 75)), fill='black', width=3)
    pwm_font = ImageFont.truetype('arial', 18)
    d.text((x-10, y+25), '=', (0, 0, 0), font=pwm_font)
    d.text((x, y + 55), '=', (0, 0, 0), font=pwm_font)


def transforemr(d, x, y):
    d.line(((x, y), (x, y + 25)), fill='black', width=3)
    d.ellipse((x-15, y+25, x+15, y+55), outline='black', width=3)
    d.ellipse((x - 15, y + 45, x + 15, y + 75), outline='black', width=3)
    d.line(((x, y + 75), (x, y + 100)), fill='black', width=3)
    pass


def external_grid(d, x, y):
    d.line(((x, y), (x, y - 25)), fill='black', width=3)
    d.line(((x - 25, y - 25), (x + 25, y - 25)), fill='black', width=3)
    d.line(((x - 25, y - 55), (x + 25, y - 55)), fill='black', width=3)
    d.line(((x - 25, y - 25), (x - 25, y - 55)), fill='black', width=3)
    d.line(((x + 25, y - 25), (x + 25, y - 55)), fill='black', width=3)
    d.line(((x - 25, y - 40), (x, y - 25)), fill='black', width=3)
    d.line(((x - 25, y - 40), (x, y - 55)), fill='black', width=3)
    d.line(((x + 25, y - 40), (x, y - 25)), fill='black', width=3)
    d.line(((x + 25, y - 40), (x, y - 55)), fill='black', width=3)
    d.line(((x - 25, y - 25), (x + 25, y - 55)), fill='black', width=3)
    d.line(((x - 25, y - 55), (x + 25, y - 25)), fill='black', width=3)


def load(d, x, y):
    (x1, y1) = (x, y+50)
    d.line(((x, y), (x1, y1)), fill='black', width=3)
    d.polygon([(x1, y1+5), (x1-5, y1-5), (x1+5, y1-5)], fill='black')


def pv(d, x, y):
    d.line(((x, y), (x, y + 15)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x + 15, y + 25)), fill='black', width=3)
    d.line(((x - 15, y + 75), (x + 15, y + 75)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x - 15, y + 75)), fill='black', width=3)
    d.line(((x + 15, y + 25), (x + 15, y + 75)), fill='black', width=3)
    d.line(((x - 15, y + 25), (x, y + 40)), fill='black', width=3)
    d.line(((x + 15, y + 25), (x, y + 40)), fill='black', width=3)
    d.line(((x - 5, y + 25), (x - 5, y + 15)), fill='black', width=1)
    d.line(((x - 5, y + 15), (x + 5, y + 15)), fill='black', width=1)
    d.line(((x + 5, y + 15), (x + 5, y + 25)), fill='black', width=1)
    d.line(((x + 5, y + 15), (x - 5, y + 25)), fill='black', width=1)
    pv_font = ImageFont.truetype('arial', 8)
    d.text((x - 4, y + 12), '~', (0, 0, 0), font=pv_font)
    d.text((x, y + 17), '=', (0, 0, 0), font=pv_font)


def bess(d, x, y):
    d.line(((x, y), (x, y + 25)), fill='black', width=3)
    d.ellipse((x - 20, y + 25, x + 20, y + 65), outline='black', width=3)
    d.line(((x - 15, y + 42), (x + 15, y + 42)), fill='black', width=3)
    d.line(((x, y + 42), (x, y + 30)), fill='black', width=3)
    d.line(((x - 7, y + 48), (x + 7, y + 48)), fill='black', width=3)
    d.line(((x, y + 48), (x, y + 60)), fill='black', width=3)
    pv_font = ImageFont.truetype('arial', 18)
    d.text((x+3, y + 25), '+', (0, 0, 0), font=pv_font)
    d.text((x+5, y + 42), '-', (0, 0, 0), font=pv_font)


def wpg(d, x, y):
    d.line(((x, y), (x, y + 25)), fill='black', width=3)
    d.ellipse((x - 20, y + 25, x + 20, y + 65), outline='black', width=3)
    d.line(((x, y + 45), (x + 20, y + 45)), fill='black', width=2)
    d.line(((x, y + 45), (x - 10, y + 45 - (10 * (3**0.5)))), fill='black', width=2)
    d.line(((x, y + 45), (x - 10, y + 45 + (10 * (3**0.5)))), fill='black', width=2)
    d.line(((x, y + 45), (x + (4 * (3**0.5)), y + 45 - 4)), fill='black', width=2)
    d.line(((x + 20, y + 45), (x + (4 * (3 ** 0.5)), y + 45 - 4)), fill='black', width=2)
    d.line(((x, y + 45), (x - (4 * (3**0.5)), y + 45 - 4)), fill='black', width=2)
    d.line(((x - 10, y + 45 - (10 * (3**0.5))), (x - (4 * (3 ** 0.5)), y + 45 - 4)), fill='black', width=2)
    d.line(((x, y + 45), (x, y + 45 + 8)), fill='black', width=2)
    d.line(((x - 10, y + 45 + (10 * (3**0.5))), (x, y + 45 + 8)), fill='black', width=2)
    # pv_font = ImageFont.truetype('arial', 18)
    # d.text((x-15, y + 37), '~', (0, 0, 0), font=pv_font)



# img = Image.new('RGB', (600, 400), 'red')
img = Image.new('RGB', (600, 400), 'white')
img1 = ImageDraw.Draw(img)
# img1.line(((20, 20), (500, 20)), fill='green', width=0)
# img1.polygon([(500, 20), (490, 15), (490, 25)], fill='black')
load(img1, 50, 60)
pwm(img1, 150, 60)
transforemr(img1, 250, 60)
dcdc_conv(img1, 350, 60)
external_grid(img1, 450, 160)
pv(img1, 550, 60)
bess(img1, 50, 260)
wpg(img1, 150, 260)


font = ImageFont.truetype('arial', 18)
img1.text((100, 100), 'Testo di esempio', (192, 158, 128), font=font)
# img1.text()

# img = img.resize((2000, 1600), Image.Resampling.LANCZOS)
img.show()

