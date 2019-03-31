# Novel Analyzer - Named Entities Relations Extractor

This is a project we made for our course "Digital Humanities"

The goal of the project is to find relations between names entities such as 
characters, locations and organizations.

Can be used to analyze text from online sources like webnovels or offline 
sources like epub files of books by implementing the corresponding content (text) provider.

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
First create or use existing class which inherits from ContentProviderBase

```python
class MyContentProvider(ContentProviderBase):
    def provide_chapter(self, indx_chapter: int) -> str:
        ...
        
my_content_provider = MyContentProvider(...)
novel_entities = infoextrct.extract(my_content_provider)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
