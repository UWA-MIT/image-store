# BuySell - AI-driven Marketplace

_ CITS5505 - Agile web development - Web Project _

Allow users to sell ("making a request") and buy ("answering the request") NFT-like images automatically generated by the site. Rewards for collecting certain sets of images? No actual cryptocurrency-related functionality required!

## Project members

| UWA ID  | Name | Github Username |
|---------|------|-----------------|
|24055729 |Nandani Patel|Nandani-06|
|23980376 |Sai Charan Pokuri|saicharan0812000|
|24090236 |Konstantin Tagintsev|ktagintsev|
|24079185 |Md Rayhan Chowdhury|rayhan|

## Features

- **Image Generation:** Users can request the generation of unique images using an advanced AI system.
- **Image Selling:** Users can list their generated images for sale on the platform.
- **Image Buying:** Users can buy images generated by other users in the system.
- **Image Searching:** Users can search images to find suitable image to buy.
- **Rewards:** Users can earn rewards by purchasing set of images of same category or from same user.
- **User Authentication:** Secure user authentication system using Flask-Login.
- **User Profile:** Users can view and edit their profiles, including details such as username, name, email, and avatar.
- **Purchase History:** Users can view their purchase history, including details of purchased images and transactions.
- **Pagination:** Paginated display of images to improve user experience.
- **Responsive Design:** The application is designed to be responsive and work seamlessly across devices of different screen sizes.


### Video

[![BuySell](https://img.youtube.com/vi/r6vSv8j6ANs/maxresdefault.jpg)](https://youtu.be/r6vSv8j6ANs "BuySell - AI-driven Marketplace (v3.0.0)")

### Application architecture


```bash
webapp
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── email.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models
│   │   ├── product.py
│   │   ├── reward.py
│   │   └── user.py
│   ├── products
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── requirements.txt
│   ├── static
│   │   ├── css
│   │   │   └── custom.css
│   │   ├── images
│   │   │   ├── background.jpg
│   │   │   ├── favicon.ico
│   │   │   ├── logo.png
│   │   │   ├── nft
│   │   │   └── profile-bg.webp
│   │   └── js
│   │       └── custom.js
│   ├── templates
│   │   ├── auth
│   │   │   ├── change_password.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── reset_password.html
│   │   │   └── reset_password_request.html
│   │   ├── base.html
│   │   ├── bootstrap_wtf.html
│   │   ├── email
│   │   │   ├── reset_password.html
│   │   │   └── reset_password.txt
│   │   ├── errors
│   │   │   ├── 400.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── main
│   │   │   └── index.html
│   │   ├── product.html
│   │   ├── products
│   │   │   ├── buy.html
│   │   │   ├── my_purchases.html
│   │   │   └── sell.html
│   │   └── users
│   │       ├── edit_profile.html
│   │       └── user.html
│   └── users
│       ├── __init__.py
│       ├── forms.py
│       └── routes.py
├── app.db
├── config.py
├── deliverables
├── docs
│   └── architecture.png
├── entrypoint.sh
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 01a7bdb1ddbe_.py
├── requirements.txt
├── storeapp.py
└── tests
    ├── chromedriver.exe
    ├── logs
    │   └── error.log
    ├── unittests.py
    └── usertests.py
```


### Technologies

- HTML5
- CSS
- JavaScript
- AJAX
- JQuery
- Bootstrap
- Flask
- SQLite

## Instructions on how to launch the application

1. Run the application loclaly:

	```bash
	python3 -m venv .venv
	. .venv/bin/activate
	```

	```bash
	pip install -r requirements.txt
	flask run  --debug
	```

	Access the app at: http://127.0.0.1:5000


2. Run in docker

	```bash
	docker build -t store-app .
	docker run -d --rm  -v `$PWD`:/app/webapp -p 5000:5000 --name store-app store-app

	# Run flask app
	docker exec -it store-app python -m flask run --host=0.0.0.0 --debug

	```
	Access the app at: http://localhost:5000

3. Test email in development server:

	```bash
	pip install aiosmtpd
	aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
	```

## Instructions on how to run the tests

1. To run unit tests:

	```bash
	cd tests
	python -m unittest unittests.py
	```

2. To run user tests (Selenium):



	Run the app with **FLASK_CONFIG = 'test'** before running all tests.

	```bash
	cd tests
	python -m unittest usertests.py
	```

	Run a test:

	```bash
	python -m unittest usertests.Test.testEditProfile
	```

	Run tests on Mac:

	The chromedriver needs to be installed separately for macos. Use following brew command to install it.

	```bash
	brew install cask chromedriver
	```

	---
	**NOTE**

	The Selenium tests only work for windows and mac os users who have Chrome installed.

	---

## Usage

1. Register an account or log in if you already have one.
2. Generate images using the provided tool.
3. List generated images for sale.
4. Browse and purchase images from other users.
5. View and edit your profile details.
6. Explore your purchase history and transaction details.

## Future Enhancements

- **Enhanced Image Generation:** Improve the AI system to generate more diverse and relevant images based on user input.
- **Social Features:** Add social features such as liking, commenting, and sharing images.
- **Advanced Search:** Implement advanced search functionality to allow users to find specific images easily.
- **Integration with Payment Gateways:** Integrate payment gateways to facilitate secure transactions for image purchases.
- **Notification System:** Implement a notification system to notify users about important events such as new purchases or comments on their images.

## References:

We have learned, explored and followed articles, samples and examples in our project. 

- https://getbootstrap.com/docs/4.0/examples/jumbotron/
- https://geeksui.codescandy.com/geeks/index.html
- https://mdbootstrap.com/docs/standard/extended/profiles/
- https://pypi.org/project/selenium/
- https://www.w3schools.com/css/
- https://www.w3schools.com/js/default.asp
- https://jquery.com/
- https://platform.openai.com/docs/overview
- https://chat.openai.com/
- https://github.com/
- https://git-scm.com/
- https://code.visualstudio.com/

## Contributions

Contributions are welcome! If you have any ideas for improvements or new features, feel free to submit a pull request.

## License Info

This project is licensed under the [MIT License](LICENSE).
