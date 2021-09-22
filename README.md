![radlistbanner](https://user-images.githubusercontent.com/67046969/134268217-9ca29f5e-49e0-49eb-9550-b5df988dbe83.jpg)
# RAD List 
RAD List is a full stack web application that helps users discover new artists. It was inspired by my love of music and wanting to make a tool that would make finding new artists easier. RAD List generates a playlist full of tracks, based on the artist a user provides. This way, you can find new artists based on ones you already like. It also allows the user save and store playlists to their account for later recall and view a profile with user details including saved playlists.

## About the Developer
Prior to Hackbright, Alex ran a practice as an acupuncturist, working with patients and coming up with creative ways to make their lives easier. Before that, she studied chemistry because she loves science and learning how to reason and solve problems. Her programming journey began 3 years ago when she was diagnosed with cancer and had to stop working. During that time, she began taking coding courses from Code Academy and she was totally hooked! She loves puzzles and the problem-solving aspect of coding. She found that she got the same joy from solving a coding problem that she did from resolving a tricky patient case. Once she was better, she took the plunge, signed up for the program and couldn’t be happier. When she is not coding, she likes movies, music and playing games.

## Tech Stack
* HTML
* Jinja
* JavaScript
* JQuery
* CSS
* Bootstrap
* Python
* Flask
* PostgreSQL
* SQL Alchemy

## API
[Last.fm API](https://www.last.fm/api) 

## Features
* New user registration
* Enter an artist and get back a playlist with 30 tracks
* Save Playlists to account for later recall
* Login and Logout

## Installation
To run RAD List on your own machine:

Install PostgresSQL (MacOSX)

Clone or fork this repo:
```
https://github.com/al-codes/RADList.git
```

Create and activate a virtual environment inside your RAD List directory:
````
$ virtualenv
$ source env/bin/activate
````
Install the dependencies:
````
$ pip3 install -r requirements.txt
````
Sign up to use the [Last.fm API](https://www.last.fm/api) 

Save your API keys in a file called `secrets.sh` using this format:
````
export LASTFM_API_KEY="YOUR_KEY_HERE"
````
Source your keys from your secrets.sh file into your virtual environment:
````
source secrets.sh
````
Set up the database:
````
createdb radlist
python3 model.py
````

Run the app:
````
python3 server.py
````
You can now navigate to 'localhose:5000/' to access RAD List

## Using RAD List

### 1. Register as a new user or login into your account
<img width="1440" alt="homepage" src="https://user-images.githubusercontent.com/67046969/134265308-7eff193e-ba97-493a-bb32-9b4f71a440c8.png">

<img width="1422" alt="Screen Shot 2021-09-21 at 5 10 07 PM" src="https://user-images.githubusercontent.com/67046969/134263674-458e4bdb-9101-4777-8f9c-209258e2a5c8.png">

### 2. Enter an artist
<img width="1439" alt="searchhome" src="https://user-images.githubusercontent.com/67046969/134265562-be86ac51-fa04-421c-8769-f5f195936015.png">

### 3. View your playlist
<img width="1439" alt="Screen Shot 2021-09-21 at 5 47 21 PM" src="https://user-images.githubusercontent.com/67046969/134266254-5031f957-951b-4a3a-ab9c-66e5a8b98893.png">

### 4. Save your playlist
<img width="1438" alt="Screen Shot 2021-09-21 at 5 52 20 PM" src="https://user-images.githubusercontent.com/67046969/134267063-cf0dd9a1-0747-4852-b713-bfb7df8ac637.png">
<img width="1436" alt="Screen Shot 2021-09-21 at 5 59 43 PM" src="https://user-images.githubusercontent.com/67046969/134267113-4799aec8-f9ac-47a1-9f05-0d19cea415c2.png">

### 5. View your profile and view saved playlists
<img width="1436" alt="profile" src="https://user-images.githubusercontent.com/67046969/134267332-ffd60979-b386-4a0e-8648-71f2721e306c.png">

## Version 2.0
* Rebuild frontend with React for less server side rendering
* Incorporate Spotify API to save playlists to Spotify account
* Adjust number of artists or tracks in new playlist

## Author
Alexandra Sanchez

## Acknowledgments
Hackbright Instructors: Drue Gilbert, Sean Moriarty, Katrina Huber-Juma, Jocelyn Tang, Jen Meara, Heather Mahan, Cindy Hazelton, Arome Yakubu, Ashley Trinh
Thank you all for your endless support and guidance throughout the cohort!

## License

The MIT License (MIT) Copyright (c) 2021 Alexandra Sanchez

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 
