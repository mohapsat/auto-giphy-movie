## Welcome to auto-giphy-movie

AutoGiphyMovie lets you search giphy for gifs, converts them to videos, attach a soundtrack and 
stitches it all together into a movie!

Uses [MoviePy](https://zulko.github.io/moviepy/) and [GiphyAPI](https://github.com/Giphy/GiphyAPI) under the hood.

## Preview

`python main.py -s godzilla -r 3` 

will produce a short movie with 3 gifs:

![Gozilla-AutoMovie](https://github.com/mohapsat/auto-giphy-movie/blob/master/godzilla-automovie.gif?raw=true)

see more examples here [youtube playlist](https://www.youtube.com/playlist?list=PLC1K_ZG1k61h2diUlgX_m84QnaaBwJFIE)

![Godzilla](https://www.youtube.com/watch?v=f7KbrP1YFgA&list=PLC1K_ZG1k61h2diUlgX_m84QnaaBwJFIE)

![Pizza Cat](https://www.youtube.com/watch?v=8rGWWFWCd7w&list=PLC1K_ZG1k61h2diUlgX_m84QnaaBwJFIE&index=9)


---
[x] Follow me on twitter [@mohapsat](https://twitter.com/mohapsat)

## Pre-requisites and Installation
- Create config.py and add API_KEY = '<GIPHY-API-KEY>'
- Install requirements.txt 
    `pip install -r requirements.txt` 
- install ffmpeg
    
    [HomeBrew Formula](https://formulae.brew.sh/formula/ffmpeg)
    
    [Packages & executable files](https://www.ffmpeg.org/download.html)

### Usage

```buildoutcfg
$ python main.py --help

usage: main.py [-h] [-s SEARCH] [-r RESULTS]

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        search term(s) for the video, e.g. 'peppa pig' or
                        'godzilla'
  -r RESULTS, --results RESULTS
                        Number of gifs to stitch in output vide, Max 25
```

As of this release [Search Endpoint](https://developers.giphy.com/docs/api/endpoint#search) of the Giphy API currently supports 25 results by default, once you've migrated to prod you should be able to 
get more gifs back and use that in your movie.

[FFMPEG](https://zulko.github.io/moviepy/install.html)

MoviePy depends on the software FFMPEG for video reading and writing. You don’t need to worry about that, as FFMPEG should be automatically downloaded/installed by ImageIO during your first use of MoviePy (it takes a few seconds).

---

[x] Support Open Source and [MoviePy](https://github.com/Zulko/moviepy)

---