from PIL import Image, ImageDraw, ImageFont
import os

stadiums = [
    "Atatürk Olimpiyat\nStadyumu",
    "Vodafone Park\nStadyumu",
    "Türk Telekom\nStadyumu",
    "Şükrü Saracoğlu\nStadyumu",
    "Fenerbahçe Şükrü\nSaracoğlu Stadyumu"
]

match_date = "19 Ağustos 2024"

match_time = "20.00"

spor = int(input("spor dalını seçin (1:futbol)"))

if spor == 1:
    football = int(input("""lig seçiniz:
1.(Süper lig)
2.(1.lig): """))
    if football == 1:
        logo_dir = "./logo"
        small = 1
        xsmall = 0.06
        # süper_lig_logo = "./trendyolsüperlig.png"
        # süper_lig = Image.open(süper_lig_logo)       
        # süper_lig_w1, süper_lig_h1 = süper_lig.size
        # süper_lig = süper_lig.resize((int(süper_lig_w1 * xsmall), int(süper_lig_h1 * xsmall)))
        bg = Image.open("./bg/bg.png")
        bg_w, bg_h = bg.size
        offset3 = (bg_w - 580, bg_h - 780)
        # bg.paste(süper_lig,offset3 ,mask=süper_lig)
        
    elif football == 2:
        logo_dir = "./1.lig"
        small = 1.3
        small1 = 0.4
        # lig1_logo = "./lig1.png"
        # lig1 = Image.open(lig1_logo)
        # lig1_w1 , lig1_h1 = lig1.size
        # lig1 = lig1.resize((int(lig1_w1 * small1), int(lig1_h1 * small1)))
        bg = Image.open("./bg/bg.png")
        bg_w, bg_h = bg.size
        offset4 = (bg_w - 580, bg_h - 780)
        # bg.paste(lig1,offset4,mask=lig1)

else:
    print("Geçersiz seçim!")
    exit()

logo_list = os.listdir(logo_dir)
logo_list = [logo for logo in logo_list if not logo.startswith(".")]

for idx, team in enumerate(logo_list):
    print(idx,team)

logo1 = int(input("1.Takımı seçin: "))
logo2 = int(input("2.Takımı seçin: "))

medium = 3
big = 5

image1 = Image.open(f"{logo_dir}/{logo_list[logo1]}")
img_w1, img_h1 = image1.size
image1 = image1.resize((int(img_w1 * small), int(img_h1 * small)))

image2 = Image.open(f"{logo_dir}/{logo_list[logo2]}")
img_w2, img_h2 = image2.size
image2 = image2.resize((int(img_w2 * small), int(img_h2 * small)))


bg_w, bg_h = bg.size
offset1 = ((bg_w - int(img_w1 * small)) // 4, (bg_h - int(img_h1 * small)) // 2)
offset2 = ((bg_w - int(img_w2 * small)) *3 // 4, (bg_h - int(img_h2 * small)) // 2)

#640 × 359

bg.paste(image1, offset1,mask=image1)
bg.paste(image2, offset2 ,mask=image2)

print("\nStadyumlar:")
for idx, stadium in enumerate(stadiums):
    print(f"{idx}: {stadium}")

stadium_index = int(input("Stadyum seçin: "))
stadium_name = stadiums[stadium_index]

font_path = "/Users/ibrahimuzunoglu/Desktop/Futbol_Takımlar/Montserrat-ExtraBold.ttf"
font_size = 20
font = ImageFont.truetype(font_path, font_size)

draw = ImageDraw.Draw(bg)
text = stadium_name
date = match_date
time = match_time

bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

text_x = (bg_w // 2) + 50
text_y = (bg_h - (text_h //2) ) - 105

max_line_length = 15
words = text.split()

y_offset = text_y
draw.text((text_x, y_offset), text, font=font, fill="white")
y_offset += text_h + 5

bbox_n = draw.textbbox((0, 0), date, font=font)
text_w = bbox_n[2] - bbox_n[0]
text_h = bbox_n[3] - bbox_n[1]

text_x = ((bg_w // 2) - text_w) - 50
text_y = (bg_h - (text_h //2) ) - 117

y_offset = text_y
draw.text((text_x, y_offset), date, font=font, fill="white")
y_offset += text_h + 5


bbox_n_n = draw.textbbox((0, 0), time, font=font)
text_w = bbox_n_n[2] - bbox_n_n[0]
text_h = bbox_n_n[3] - bbox_n_n[1]

text_x = ((bg_w // 2) - text_w) - 50
text_y = (bg_h - (text_h // 2) ) - 95

y_offset = text_y
draw.text((text_x, y_offset), time, font=font, fill="white")
y_offset += text_h + 5

bg.save('./Futbol.png', quality=100)