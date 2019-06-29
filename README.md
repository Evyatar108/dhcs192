# coding=utf-8# Novel Analyzer - Named Entities Relations Extractor

This is a project we made for our course "Digital Humanities"

The goal of the project is to find relations between names entities such as 
characters, locations and organizations.

Can be used to analyze text from online sources like webnovels or offline 
sources like epub files of books by implementing the corresponding content (text) provider.

## Features
Gather a novel's chapters, using premade web crawlers, from known web novel sites.

Querying the stanford corenlp model with the chapters

Aggregating tagged named entities tokens into one named entity object

Matching co-references to previously created named entities and enriching their info based on them.

Finding the corresponding object and subject named entities for each OpenIE relation after preprocessing of the relation

Using regex to construct connections between named entities (currently family) from their OpenIE relations  

Infer new connections between named entities based on their current connections to other named entities

Build connections from shared relations where two or more named entities are the subject/object of the same relation

Merge first person named entities to represent the story-teller of the webnovel if there is one

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
Run the stanford corenlp server using the command
```bash
java -Xmx4g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000
```

Create or use existing class which inherits from ContentProviderBase

```python
class MyContentProvider(ContentProviderBase):
    def provide_chapter(self, indx_chapter: int) -> str:
        ...
        
my_content_provider = MyContentProvider(...)
novel_entities = infoextrct.extract(my_content_provider)
```

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
