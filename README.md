# CBGB-Lyrics-Guesser
Small program that guesses which CBGB-artist wrote given lyrics. All lyrics by four CBGB-artists (Blondie, Iggy Pop, Ramones, Talking Heads) are scraped and split into train and test data. The final outcome is a confusion matrix for the test lyrics. 

Contents:
  - Scraper(ScraPy): lyrics_scraper_clean.py
    
    run with: scrapy runspider -o output_lyrics.csv -L WARNING lyrics_scraper_clean.py
  - Predictor: lyrics_predictor.py
    
    based on naive bayes

The artists and the corresponding lyric sites are hard coded.

The program was written as during a coding bootcamp at Spiced Academy, Berlin, Germany.
