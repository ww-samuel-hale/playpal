<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ww-samuel-hale/playpal">
    <img src="FrontEnd/playpal/public/favicon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center"><a href="https://playpal-jwmk.onrender.com">PlayPal</a></h3>


  <p align="center">
    A video game recommendation service that uses machine learning and the IGDB API to tailor suggestions and allows users to manually filter based on a variety of criteria. 
    <br />
    <a href="https://github.com/ww-samuel-hale/playpal"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ww-samuel-hale/playpal">View Demo</a>
    ·
    <a href="https://github.com/ww-samuel-hale/playpal/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/ww-samuel-hale/playpal/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://playpal-jwmk.onrender.com/)

This project was inspired by [Swipefy](https://apps.apple.com/us/app/swipefy-for-spotify/id6449814769), a swipe-based music suggestion software created by a colleague's kid and his pals. I saw this and enjoyed how it worked. This prompted me to consider how else we may use Machine Learning and AI to tackle the content recommendation problem. After considering a few examples, I chose video games for two reasons:
1) IGDB API provides free development API keys, and I'm not made of money.
2) This solves a problem for me where I grow bored with a game I've been playing but nothing really hits my video game "taste pallette" when I browse.

The two main features are Machine Learning recommendations, which means that when you play games with thumbs up and thumbs down, a vector profile will be created. Games will be compared to this vector profile, and the top 100 most similar games will be suggested with each click of the "Generate Recommendations" button. The second feature is Category Filtering. This is mainly to offer the user choice over what they are recommended, allowing them to select by platform, rating, genre, and other more narrow categories.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![React][React.js]][React-url]
* [![Flask][Python Flask]][Python-url]
* [![PostgreSQL][PostgresImg]][Postgres-url]
* [![Python][PythonImg]][Python-link]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To use a deployed version of this program, go to [https://playpal-jwmk.onrender.com](https://playpal-jwmk.onrender.com/) (Keep in mind that this is a free instance, so there may be some latency, especially if there is no traffic). To start a local instance, follow these steps: simple steps.

### Prerequisites

[Python](https://www.python.org/downloads/) - Select to install pip and make sure it sets Python in your PATH
[NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
[PostgreSQL](https://www.postgresql.org/download/)
[IGDB API Key](https://api-docs.igdb.com/#getting-started)

### Installation

1. Create "playpal" database 
2. Set up database tables with database_commands.txt
3. Create a .env in your BackEnd folder
4. Fill in your API client secret and id
5. Fill in your database_url
6. Create a python virtual environment 'python -m venv <virtual environment name>'
7. Source the activate script via './<venvname>/Scripts/activate' on windows powershell
8. Install all dependencies 'pip install -r requirements.txt'
9. Start server with python server.py
10. Open a new terminal for your front end
11. Navigate to FrontEnd folder
12. Run npm install
13. Run npm start
14. Enjoy!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

To be updated..

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/ww-samuel-hale/playpal/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Samuel Hale - samuelhalebusiness@gmail.com

Project Link: [https://github.com/ww-samuel-hale/playpal](https://github.com/ww-samuel-hale/playpal)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ww-samuel-hale/playpal.svg?style=for-the-badge
[contributors-url]: https://github.com/ww-samuel-hale/playpal/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ww-samuel-hale/playpal.svg?style=for-the-badge
[forks-url]: https://github.com/ww-samuel-hale/playpal/network/members
[stars-shield]: https://img.shields.io/github/stars/ww-samuel-hale/playpal.svg?style=for-the-badge
[stars-url]: https://github.com/ww-samuel-hale/playpal/stargazers
[issues-shield]: https://img.shields.io/github/issues/ww-samuel-hale/playpal.svg?style=for-the-badge
[issues-url]: https://github.com/ww-samuel-hale/playpal/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/samhale07
[product-screenshot]: FrontEnd/playpal/public/PlayPalImg.png
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Python Flask]: https://img.shields.io/badge/Python-Flask-4B8BBE?style=flat&logo=python&logoColor=white
[Python-url]: https://flask.palletsprojects.com/en/3.0.x/
[PostgresImg]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[PythonImg]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-link]: https://www.python.org/

