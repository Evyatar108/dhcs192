# Named Entities Relations Extractor

* TOC
{:toc}

We did this project for the Digital Humanities course 

The goal of this project is to find relations between names entities such as 
characters, locations, and organizations.

It can be used to analyze text from online sources, such as web novels, or offline content, such as epub files. 

## Features
Extracting novel's chapters from local content, or web novel sites using pre-made/custom-made web crawlers

Querying Stanford's CoreNLP model with each chapter

Aggregating tagged named entities tokens into one named entity object.

Pairing co-references to previously created named entities and enriching their info based on them

Determining the corresponding object and subject named entities for each OpenIE relation after relations' preprocessing 

Utilizing regex to identify connections between named entities (currently family) from their OpenIE relations  

Inferring new connections between named entities based on their current connections to other named entities

Building connections from shared relations where two or more named entities are the subject/object of the same relation

Merging first person named entities who represent the story-teller of the novel (if there is one)

Visualizing the connections/relations between the named entities using an interactive graph

## Installation
Download CoreNLP by Stanford University
```bash
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
```
Unzip the file inside the project's folder
```bash
unzip stanford-corenlp-full-2018-10-05.zip
```
To use available web crawlers download [chromedriver](http://chromedriver.chromium.org/downloads) with the version of your chrome and place it in the project's directory

## Usage
Move to the project's directory and run the Stanford CoreNLP server using the command
```bash
java -Xmx4g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000
```
Run the grphviz.py file to start an interactive console

## Adding new content providers
Create or use an existing class which inherits from 'ContentProviderBase' and implement 'provide_chapter'

```python
class MyContentProvider(ContentProviderBase):
    def provide_chapter(self, indx_chapter: int) -> str:
        ...
```

and add the class to the following list in grphviz.py
```python
remote_provider_tuples: Tuple[str, ContentProviderBase] = [
        ("Royalroad", RoyalRoadContentProvider),
        ("Wuxiaworld", WuxiaWorldContentProvider)
]
```

## Adding new relation extraction rules using regex
Adding new regex rules to identify specific relations is possible by editing the relations.py, sharedrelations.py, and commonalities.py files.

Further work needs to be done to enable easier customization of the rules without editing the source files.


## Output Example
Running the program on the first 20 chapters of the
[Dont Feed The Dark](https://www.royalroad.com/fiction/6245/dont-feed-the-dark) 
web novel we get the following graph which describe all of the extract relations between the characters
[graph](dont-feed-the-dark.html)

Running the program on [The Story Of An Hour - Summary](https://www.sparknotes.com/short-stories/the-story-of-an-hour/summary/)
using the familiy relation extraction option only - we get the following 
[graph](the_story_of_an_hour.html)
## Contributing
Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Made by
Hadar Levi

Evyatar Mitrani
