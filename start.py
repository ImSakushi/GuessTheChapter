from flask import Flask, request, render_template, session
import random

app = Flask(__name__)
app.secret_key = 'scanr'  # Change this to a secret key

@app.route('/', methods=['GET', 'POST'])
def game():
    session['score'] = session.get('score', 0)
    session['tries'] = session.get('tries', 0)
    message = ''

    if 'random_chapter' not in session or 'random_page' not in session:
        session['random_chapter'] = random.choice(range(1, 122))
        session['random_page'] = random.choice(range(1, 19))
        session['tries'] = 0

    url = f"https://s22.anime-sama.fr/s1/scans/Oshi%20no%20Ko/{session['random_chapter']}/{session['random_page']}.jpg"

    if request.method == 'POST':
        guess = request.form.get('chapter_guess')
        if guess:
            if int(guess) == session['random_chapter']:
                session['score'] += 1
                message = "Bravo ! Vous avez deviné correctement !"
                session.pop('random_page', None)
                session['tries'] = 0
            else:
                session['tries'] += 1
                message = f"Désolé, ce n'est pas le chapitre {guess}. Essayez encore !"
                if session['tries'] == 3:
                    message = f"Désolé, la bonne réponse était le chapitre {session['random_chapter']}."
                    session.pop('random_page', None)
                    session['tries'] = 0

    image_height = int(569 / 3 * (session['tries'] + 1))
    return render_template('game.html', image_url=url, score=session['score'], chapter=session['random_chapter'], message=message, image_height=image_height)

@app.route('/next', methods=['GET', 'POST'])
def next_game():
    if request.method == 'POST':
        return game()

    session.pop('random_chapter', None)
    session.pop('random_page', None)
    session['tries'] = 0

    return game()

if __name__ == "__main__":
    app.run(debug=True)
