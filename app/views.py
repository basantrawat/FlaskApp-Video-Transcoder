from app import app
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os
from pathlib import Path
from time import perf_counter

app.config['UPLOAD_FOLDER'] = "F:\\PROGRAMMING\\Python\\MediaEditing\\videoEditing\\app\\uploadFolder"

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/format-conversion', methods=['GET','POST'])
def format_conversion():
    if(request.method=='POST'):
        file_names = request.files.getlist('filename[]')
        file_format = request.form.get('file-format')

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        for file_name in file_names:
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))

        for file_name in file_names:
            myvideo = VideoFileClip("app/uploadFolder/"+secure_filename(file_name.filename))
            name = secure_filename(file_name.filename)[:-4]+"-NewFormat"+file_format
            myvideo.write_videofile(f"app/output_files/{name}", codec="libx264")
        
        '''RETURNING THE PAGE WITH URL LINK OF Converted FILES'''
        return render_template('format-conversion.html', msg="Merged Successfully", file_path="#")     
    else:
        return render_template('format-conversion.html', msg="", file_path="")


@app.route('/resize-video', methods=['GET','POST'])
def resizing_video():
    if(request.method=='POST'):
        file_names = request.files.getlist('filename[]')
        changed_width = int(request.form.get('width'))
        file_format = request.form.get('file-format')

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        for file_name in file_names:
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))

        for file_name in file_names:
            myvideo = VideoFileClip("app/uploadFolder/"+secure_filename(file_name.filename))
            resized_video = myvideo.resize(width=changed_width)
            name = secure_filename(file_name.filename)[:-4]+"-Resized"+file_format
            resized_video.write_videofile(f"app/output_files/{name}", codec="libx264")
        
        '''RETURNING THE PAGE WITH URL LINK OF Converted FILES'''
        return render_template('resize-video.html', msg="Merged Successfully", file_path="#")     
    else:
        return render_template('resize-video.html', msg="", file_path="")


@app.route('/merge-videos', methods=['GET', 'POST'])
def merge_videos():
    if(request.method=='POST'):
        file_names = request.files.getlist('filename[]')

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        for file_name in file_names:
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))

        '''MERGING THE UPLOADED FILES'''
        clips = []
        for file_name in file_names: 
            clips.append(VideoFileClip("app/uploadFolder/" + secure_filename(file_name.filename)))

        # video = CompositeVideoClip([clip1,clip2])  #CompositVideoClip class provide more flexibilty 
        merged_clip = concatenate_videoclips([clip for clip in clips])      
        name = secure_filename(file_names[0].filename)[:-4]+"-MergedVideo"+".mp4"
        merged_clip.write_videofile(f"app/output_files/{name}", codec="libx264")
        
        '''RETURNING THE PAGE WITH URL LINK OF MERGED FILE'''
        file_path = "output_files/" + name
        return render_template('merge-videos.html', msg="Merged Successfully", file_path=file_path) 
    
    else:
        return render_template('merge-videos.html', msg="", file_path="")


@app.route('/cut-clip', methods=['GET', 'POST'])
def cut_clip():
    if(request.method=='POST'):
        # filename, time_from, time_to
        file_name = request.files.get('filename')
        time_from = request.form.get('time_from')
        time_to = request.form.get('time_to')
        
        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))
        myvideo = VideoFileClip("app/uploadFolder/"+secure_filename(file_name.filename))

        trimmed_video = myvideo.subclip(int(time_from), int(time_to))
        name = secure_filename(file_name.filename)[:-4]+"-TrimmedVideo"+".mp4"
        trimmed_video.write_videofile(f"app/output_files/{name}", codec="libx264")
        
        '''RETURNING THE PAGE WITH URL LINK OF MERGED FILE'''
        file_path = "output_files/" + name
        return render_template('cut-clip.html', msg="Trimmed Successfully", file_path=file_path) 

    else:
        return render_template('cut-clip.html', msg="", file_path="")


@app.route('/mirror-video', methods=['GET', 'POST'])
def mirror_video():
    if(request.method=='POST'):
        file_name = request.files.get('filename')
        axis = request.form.get('axis')

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))
        myvideo = VideoFileClip("app/uploadFolder/"+secure_filename(file_name.filename))
        
        name = secure_filename(file_name.filename)[:-4]+"-Mirrored"+".mp4"

        if(axis.lower()=='x'):
            mirrored_video_on_x = myvideo.fx(vfx.mirror_x)
            mirrored_video_on_x.write_videofile(f"app/output_files/{name}", codec="libx264")
        elif(axis.lower()=='y'):
            mirrored_video_on_y = myvideo.fx(vfx.mirror_y)
            mirrored_video_on_y.write_videofile(f"app/output_files/{name}", codec="libx264")
        else:
            pass

        '''RETURNING THE PAGE WITH URL LINK OF MERGED FILE'''
        file_path = "output_files/" + name
        return render_template('mirror-video.html', msg="Mirroring done Successfully", file_path=file_path) 

    else:
        return render_template('mirror-video.html', msg="", file_path="")

