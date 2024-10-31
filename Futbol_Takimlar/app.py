from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
import pymongo


app = Flask(__name__)

username = "mongadmin"
password = "tu6@fKhW@Sepr8oFhB"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
client = pymongo.MongoClient(f"mongodb://{encoded_username}:{encoded_password}@78.111.98.157:27017/admin")
db = client["datablastest"]
collection = db["soccerteams"]

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    print(data)

    stadium_name = data.get('stadium_name')
    match_date = data.get('match_date')
    match_time = data.get('match_time')

    team_1_provider = data.get('team_1_provider')
    team_2_provider = data.get('team_2_provider')
    team1_id = data.get('team1')
    team2_id = data.get('team2')
    league = data.get('league')

    if not all([stadium_name, match_date, match_time, team1_id, team2_id, league]):
        return jsonify({'error': 'Missing data'}), 400

    if league == 1:
        logo_dir = r"/logo"
        small = 1.50
    else:
        return jsonify({'error': 'Invalid league'}), 400
    
    team1 = collection.find_one({"providers." + team_1_provider + ".id": team1_id})
    team2 = collection.find_one({"providers." + team_2_provider + ".id": team2_id})


    if not team1 or not team2:
        return jsonify({'error': 'One or more team logos not found in the database'}), 404

    bg = Image.open("bg/bg1.png")
    bg_w, bg_h = bg.size

    try:
        #team_1_name - sorgu = pathch
        team1_logo = Image.open(f"{logo_dir}/{team1_id['logo_url']}")
        img_w1, img_h1 = team1_logo.size
        team1_logo = team1_logo.resize((int(img_w1 * small), int(img_h1 * small)))

        team2_logo = Image.open(f"{logo_dir}/{team2_id['logo_url']}")
        img_w2, img_h2 = team2_logo.size
        team2_logo = team2_logo.resize((int(img_w2 * small), int(img_h2 * small)))
    except FileNotFoundError:
        return jsonify({'error': 'One or more team logos not found'}), 404

    offset1 = ((bg_w - int(img_w1 * small)) // 4, (bg_h - int(img_h1 * small)) // 2 - 20)
    offset2 = ((bg_w - int(img_w2 * small)) * 3 // 4, (bg_h - int(img_h2 * small)) // 2 - 20)
    bg.paste(team1_logo, offset1, mask=team1_logo)
    bg.paste(team2_logo, offset2, mask=team2_logo)

    font_path = "./Montserrat-ExtraBold.ttf"
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(bg)

    bbox = draw.textbbox((0, 0), stadium_name, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (bg_w // 2) + 50
    text_y = (bg_h - (text_h // 2)) - 185
    draw.text((text_x, text_y), stadium_name, font=font, fill="white")

    bbox_n = draw.textbbox((0, 0), match_date, font=font)
    text_w = bbox_n[2] - bbox_n[0]
    text_h = bbox_n[3] - bbox_n[1]
    text_x = ((bg_w // 2) - text_w) - 50
    text_y = (bg_h - (text_h // 2)) - 197
    draw.text((text_x, text_y), match_date, font=font, fill="white")

    bbox_n_n = draw.textbbox((0, 0), match_time, font=font)
    text_w = bbox_n_n[2] - bbox_n_n[0]
    text_h = bbox_n_n[3] - bbox_n_n[1]
    text_x = ((bg_w // 2) - text_w) - 50
    text_y = (bg_h - (text_h // 2)) - 175
    draw.text((text_x, text_y), match_time, font=font, fill="white")

    img_io = io.BytesIO()
    bg.save(img_io, 'PNG', quality=100)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='match_image.png')

if __name__ == '__main__':
    app.run(debug=True)
