from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__, static_folder="static")
app.secret_key = 'supersecretkey'  # 세션을 사용하려면 비밀키 필요

def generate_new_number():
    """새로운 정답 숫자를 생성하고 세션에 저장"""
    session['random_number'] = random.randint(1, 100)

@app.route('/')
def home():
    generate_new_number()  # 게임을 시작할 때 새로운 숫자 생성
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    if 'random_number' not in session:
        generate_new_number()  # 혹시 세션이 없으면 새로 생성

    user_guess = int(request.form['guess'])
    attempt_count = int(request.form['attempts'])  # 프론트엔드에서 받아온 시도 횟수
    random_number = session['random_number']  # 세션에서 숫자 불러오기

    if user_guess < random_number:
        return jsonify({'message': '올려야 해!', 'attempts': attempt_count})
    elif user_guess > random_number:
        return jsonify({'message': '낮춰야 해!', 'attempts': attempt_count})
    else:
        return jsonify({'message': f'정답! {attempt_count}번 만에 맞췄어요!', 'attempts': attempt_count})

@app.route('/reset', methods=['POST'])
def reset_game():
    """새 게임을 시작하는 엔드포인트"""
    generate_new_number()
    return jsonify({'message': '새로운 게임이 시작되었습니다!'})

if __name__ == '__main__':
    app.run(debug=True)
