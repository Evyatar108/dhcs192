# coding=utf-8
from itertools import chain

from novelanalyze.analyztn.parsedata import TextAnalysis
from novelanalyze.contntprvdr import ContentProviderBase
from novelanalyze.analyztn import corenlp, convert, enrich
from novelanalyze.prcssng.entitydata import NovelEntities
from novelanalyze.prcssng.updtrs.char import CharacterNamedEntityUpdater
from novelanalyze.prcssng.updtrs.loc import LocationNamedEntityUpdater
from novelanalyze.prcssng.updtrs.org import OrganizationNamedEntityUpdater
from novelanalyze.prcssng.insights import relations
from novelanalyze.prcssng.insights import sharedrelations
from novelanalyze.prcssng.insights import commonalities


def extract(novel_content_provider: ContentProviderBase) -> NovelEntities:
    chapters_generator = novel_content_provider.generate_all_chapters()
    novel_entities = NovelEntities()
    for indx_chapter, chapter in enumerate(chapters_generator):
        raw_data = corenlp.query_model(chapter)
        enrich.improve_coreferences(raw_data)
        text_analysis = convert.convert_to_local_obj(raw_data)
        __process_chapter_analysis(text_analysis, novel_entities, indx_chapter)

    named_entities = list(chain(novel_entities.characters, novel_entities.locations, novel_entities.organizations))

    relations.process(named_entities)
    sharedrelations.process(named_entities)
    commonalities.process(named_entities)

    return novel_entities


def __process_chapter_analysis(text_analysis: TextAnalysis, novel_entities: NovelEntities, indx_chapter: int):
    CharacterNamedEntityUpdater().update(text_analysis, novel_entities.characters, indx_chapter)
    LocationNamedEntityUpdater().update(text_analysis, novel_entities.locations, indx_chapter)
    OrganizationNamedEntityUpdater().update(text_analysis, novel_entities.organizations, indx_chapter)


# todo add an example from offline/online novel
if __name__ == "__main__":
    # # "Israel is a nice place"  # 'Renya walked him to school everyday. She\'d talk to him about love. Then, once they got to the school, Renya would leave him and go do math alone. Ichi couldn\'t fathom what she was thinking, playing around like that. Ichi knew Reyna was lying to him. Ichi could smell it on her.'

    example_sentence = 'Ron and John are good. They are nice, and he is strong' #'Ok go. John is the brother of Joseph'  # 'Ron and Anny are father and son'  # 'Zorian’s eyes abruptly shot open as a sharp pain erupted from his stomach. His whole body convulsed, buckling against the object that fell on him, and suddenly he was wide awake, not a trace of drowsiness in his mind. “Good morning, brother!” an annoyingly cheerful voice sounded right on top of him. “Morning, morning, MORNING!!!” Zorian glared at his little sister, but she just smiled back at him cheekily, still sprawled across his stomach. She was humming to herself in obvious satisfaction, kicking her feet playfully in the air as she studied the giant world map Zorian had tacked to the wall next to his bed. Or rather, pretended to study – Zorian could see her watching him intently out of the corner of her eyes for a reaction. This was what he got for not arcane locking the door and setting up a basic alarm perimeter around his bed. “Get off,” he told her in the calmest voice he could muster. “Mom said to wake you up,” she said matter-of-factly, not budging from her spot. “Not like this, she didn’t,” Zorian grumbled, swallowing his irritation and patiently waiting till she dropped her guard. Predictably, Kirielle grew visibly agitated after only a few moments of this pretend disinterest. Just before she could blow up, Zorian quickly grasped her legs and chest and flipped her over the edge of the bed. She fell to the floor with a thud and an indignant yelp, and Zorian quickly jumped to his feet to better respond to any violence she might decide to retaliate with. He glanced down on her and sniffed disdainfully. “I’ll be sure to remember this the next time I’m asked to wake you up.”'
    print('Executing Text Analysis')
    raw_data = corenlp.query_model(example_sentence)
    print('Finished Text Analysis')
    text_analysis = convert.convert_to_local_obj(raw_data)
    print('Converting Text Analysis to local object')
    pass
