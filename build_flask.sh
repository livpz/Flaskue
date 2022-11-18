#!/bin/bash

app_py="
# -*- coding:utf-8 -*-
from flask import Flask,
from flask_cors import CORS

class App:
    app=None

    @classmethod
    def initialize(cls):
        app=Flask(__name__)
        CORS(app, resources=r'/*')
        app.config['SECRET_KEY']='whatyougivewhatyouget'
        App.app=app

        @app.route('/')
        def index():
            # print('Main index')
            return 'Main index'

    @classmethod
    def get_flask_instance(cls):
        return cls.app

    @classmethod
    def run_instance(cls):
        app=cls.app
        return app.run(host='0.0.0.0', port=5000)
"

run_py="
import os

from App import App

App.initialize()

app=App.app

for root, dirnames, filenames in os.walk('./BluePrint/'):
    for dirname in dirnames:
        path=str(os.path.join(root, dirname))
        if path[-3:] == '_bp':
            __import__(path.replace('/', '.')[2:] + '.setup')
	    print('Active ' + path[-3:])

if __name__ == '__main__':
    App.run_instance()
"



if [ $# == 0 ]; then

	echo -e  "Set name for this Flask project, as long as the root foldername:"
	read -p "Project name: " _name

	project_name=${_name}

	echo -e "If set the single bp as the same name?"
	read if_single

	if [ -z "${if_single}" ]; then
		bp_name=${project_name}
		echo -e "OK." 
	else
		echo -e "Set a new name for the single bp name:"
		read _bp_name
		bp_name=${_bp_name}
	fi

else
	project_name=$1
	bp_name=$1
fi

echo "${project_name} ${bp_name}"

setup_py="
from App import App
from .${bp_name}_bp import ${bp_name}_bp


app=App.app


app.register_blueprint(${bp_name}_bp)
"

single_bp_py="
from flask import Blueprint, render_template, request 
from .config.route_map import Page


mail_bp=Blueprint(
    '${bp_name}',
    __name__,
    static_folder='./static/',
    template_folder='./templates/',
    url_prefix='/${bp_name}'
)

@${bp_name}_bp.route('/')
def index():
    return render_template(Page.index)
"

route_map_py="
class Page:
    index='${bp_name}_index.html'

class Database:
    test_db='BluePrint/${bp_name}_bp/db/test.db'

class Folder:
    zip_folder='/Blueprint/${bp_name}_bp/temp/'
    rawfile_folder='/Blueprint/${bp_name}_bp/file/'
" 

index_html="
<html>
    <head>
        <link rel='stylesheet' href='{{url_for('${bp_name}.static',filename='./css/main.css')}}' type='text/css'>
	<script src='{{url_for('${bp_name}.static',filename='./js/index.js')}}'> </script>
    	</head>

    <body>
        <div id='vue'>
            <div id='title'>
                <span><h2> ${bp_name} index.</h2></span>
            </div>
    </body>
</html>
"

main_css="
body{
    display: flex;
}

#title{
    margin: auto;
}

#vue{
    margin: auto;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
}
"

index_js="
console.log('Enjoy it.')
"

mkdir "${project_name}"

cd  "${project_name}"

mkdir -p "Blueprint/${bp_name}_bp/config"

mkdir -p "Blueprint/${bp_name}_bp/static/css"

mkdir -p "Blueprint/${bp_name}_bp/static/js"

mkdir -p "Blueprint/${bp_name}_bp/templates"

mkdir -p "Blueprint/${bp_name}_bp/temp"

mkdir -p "Blueprint/${bp_name}_bp/file"

mkdir -p "Blueprint/${bp_name}_bp/db"


echo ${run_py} > "run.py"
echo ${app_py} > "App.py"
echo ${setup_py} > "Blueprint/${bp_name}_bp/setup.py"
echo ${single_bp_py} > "Blueprint/${bp_name}_bp/${bp_name}_bp.py"
echo ${index_html} > "Blueprint/${bp_name}_bp/templates/${bp_name}_index.html"
echo ${main_css} > "Blueprint/${bp_name}_bp/static/css/main.css"
echo ${index_js} > "Blueprint/${bp_name}_bp/static/js/index.js"
echo ${route_map_py} > "Blueprint/${bp_name}_bp/config/route_map.py"

echo -e "Project is already builded."
