# Novel Analyzer - Named Entities Relations Extractor

* TOC
{:toc}

This is a project we made for the course "Digital Humanities"

The goal of this project is to find relations between names entities such as 
characters, locations and organizations.

It can be used to analyze text from online sources like webnovels or offline 
sources like epub files of books by implementing the corresponding content (text) provider.

## Features
Gather a novel's chapters, using premade web crawlers, from known web novel sites.

Querying the stanford corenlp model with the chapters

Aggregating tagged named entities tokens into one named entity object

Matching co-references to previously created named entities and enriching their info based on them.

Finding the corresponding object and subject named entities for each OpenIE relation after relations' preprocessing 

Applying regex to identify connections between named entities (currently family) from their OpenIE relations  

Inferring new connections between named entities based on their current connections to other named entities

Building connections from shared relations where two or more named entities are the subject/object of the same relation

Merging first person named entities to represent the story-teller of the novel if there is one

Visualizing the connections/relations between the named entities using a graph

## Installation
Download CoreNLP by Stanford University
```bash
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
```
Unzip the file inside the project's folder
```bash
unzip stanford-corenlp-full-2018-10-05.zip
```


## Usage
Move to the project's directory and run the stanford corenlp server using the command
```bash
java -Xmx4g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000
```
Run the grphviz.py file which will start an interactive console

## Adding new content providers
Create or use existing class which inherits from ContentProviderBase

```python
class MyContentProvider(ContentProviderBase):
    def provide_chapter(self, indx_chapter: int) -> str:
        ...
        
my_content_provider = MyContentProvider(...)
novel_entities = infoextrct.extract(my_content_provider)
```

and add the option to the grphviz.py file

## Example Output
Running the program on the first 20 chapters of the
[Dont Feed The Dark](https://www.royalroad.com/fiction/6245/dont-feed-the-dark) 
web novel we get the following
[graph](dont-feed-the-dark.html)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Made by
Hadar Levi

Evyatar Mitrani
