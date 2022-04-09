from website import create_app

app = create_app()

app.app_context().push()

if __name__ == '__main__':
    #app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=5000, debug=False)
    #run flask application