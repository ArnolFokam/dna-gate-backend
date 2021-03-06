<div id="top"></div>

## About The Project
This is the backend of DNA Gate, a SaaS app for robust biometric authentication. 

Check this [link](https://github.com/ArnolFokam/dna-gate) for more information.

### Built With

* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](mongodb.com)
* [Express](https://expressjs.com/)


## Getting Started

1. Clone the repository
2. Enter the project's directory and edit the .env file as follows
```
APP_NAME=ModzyHack
ENV=development

SECRET_KEY=supersecretkey
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=60

MONGODB_URL=uri of a running mongo instance (eg. mongodb://127.0.0.1:27017/?retryWrites=true&w=majority)
DATABASE=mongodb database to use

MODZY_API_KEY=your modzy api key
```
4. Run ```pip install -r requirements``` (Make sure that you have [Python <= 3.8](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installation/) before running this command)
5. Run ```uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}```

You should have your backend up and running at [http://localhost:8000](http://localhost:8000). You can see the SwaggerUI API documentation of the backend at this [link](http://localhost:8000/api/docs) 

Note:
If you deploy to heroku, you need to add soundfile library package for voice recognition to work. 
To do so, add the [apt buildpack](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt) and it will look at [Aptfile](https://github.com/ArnolFokam/dna-gate-backend/blob/main/Aptfile) in the project to install necessary libraries.

## License

Distributed under the Apache 2.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


## Contact

Arnol Fokam - [@ArnolFokam](https://twitter.com/arnolfokam)

Project Link: [https://github.com/ArnolFokam/dna-gate](https://github.com/ArnolFokam/dna-gate-backend)

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

* [Modzy](https://www.modzy.com/) (Computer Vision pre-trained models)
<p align="right">(<a href="#top">back to top</a>)</p>
