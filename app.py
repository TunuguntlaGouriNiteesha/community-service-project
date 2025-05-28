from flask import Flask, render_template, request
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
import os
import pickle
import re
from googletrans import Translator

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result2 = request.form['Name']
        print(result2)
        isl_text, video_result = processing(result2)
        items = {
            'Speech To Text Conversion': result2,
            'Text to Indian Sign Language': isl_text[0]
        }
        return render_template("result.html", result=items, result1=video_result)

@app.route('/how-to-use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

def processing(result):
    translator = Translator()
    trans_result = translator.translate(result, dest='en')
    print(result)
    print(trans_result)
    pos_tag_result = pos_tagging(trans_result.text)
    filter_result = filter(pos_tag_result)
    sentence_reordering_result = sentence_reordering(filter_result)
    stop_word_eliminator_result = stop_word_eliminate(sentence_reordering_result)
    lemmatize_result = convert_lemma(stop_word_eliminator_result)
    video_result = video_conversion(lemmatize_result)
    return lemmatize_result, video_result

def pos_tagging(result):
    # Your POS tagging logic (this is just a placeholder for your logic)
    return [(word, 'NOUN') for word in result.split()]

def filter(ud_sents):
    # Filter out punctuations or unwanted words
    punctuations = [',', '?', '!', '.']
    filtered = []
    for word, tag in ud_sents:
        if word not in punctuations:
            filtered.append((word.lower(), tag))
    return filtered

def sentence_reordering(ud_sents):
    # Dummy sentence reordering for now, adjust as per your requirements
    return ud_sents

def stop_word_eliminate(ud_sents):
    # Dummy stop-word removal, replace with your stop words list
    stop_words = ['a', 'the', 'is', 'of']
    return [(word, tag) for word, tag in ud_sents if word not in stop_words]

def convert_lemma(ud_sents):
    # Lemmatization placeholder (adjust as per your lemma dictionary)
    return [(word, tag) for word, tag in ud_sents]

def video_conversion(lema_isl_sent_list):
    print('\n\tVideo Conversion Module\t\n')
    start_time = time.time()
    video_array = []

    # Generate video clips for the ISL words (using placeholders here)
    for word_tuple in lema_isl_sent_list:
        word = word_tuple[0]
        word = word.lower()
        
        # Check if video files for the word exist
        if os.path.isfile(f"video_files/{word}.mp4"):
            video_array.append(VideoFileClip(f"video_files/{word}.mp4").resize((500, 380)))
        else:
            for ch in word:
                # Handle character-based videos for missing word videos
                video_array.append(VideoFileClip(f"video_files/{ch.upper()}.mp4").resize((500, 380)))

    # Create the final video by concatenating all the clips
    final_clip = concatenate_videoclips(video_array, method='compose')
    sent = "".join([word for word, _ in lema_isl_sent_list]) + ".mp4"
    final_clip.write_videofile(f"static/{sent}")

    print(time.time() - start_time)
    return sent

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)
