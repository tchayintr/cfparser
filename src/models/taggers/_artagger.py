# -*-coding: utf-8 -*-
import artagger

'''
    Tag POS to segmened words
    input: string of segmented words e.g. ฉัน กิน ข้าว
    output: POS-tagged pairs e.g. (.word and .tag)
'''



class ARTagger(artagger.Tagger):
    def __init__(self):
        pass


    @classmethod
    def tag(cls, inp, brackets_format='()'):
        '''Tag an input using defined arbitary format'''
        assert len(brackets_format) == 2
        brackets_format_l = brackets_format[0]
        brackets_format_r = brackets_format[1]
        pairs = []
        tags = artagger.Tagger().tag(inp)
        for tag in tags:
            pairs.append('{}{} {}{}'.format(
                brackets_format_l,
                tag.tag,
                tag.word,
                brackets_format_r
            ))
        return ' '.join(pairs)
        # return '{}{}{}'.format(brackets_format_l, ' '.join(pairs), brackets_format_r)


    @classmethod
    def default_tag(cls, inp):
        '''Tag POS to segmented words then return word and tag lists'''
        tagpairs = artagger.Tagger().tag(inp)
        words, tags = distribute(tagpairs)
        return words, tags



def distribute(tagpairs):
    '''Distribute tag pairs to taglist i.e. [artagger.Word.object, ...] to [w1, w2, ..., wn] and [t1, t2, ..., tm]'''
    words, tags = [], []
    for tagpair in tagpairs:
        words.append(tagpair.word)
        tags.append(tagpair.tag)
    assert len(words) == len(tags)
    return words, tags



if __name__ == '__main__':
    print(ARTagger.default_tag('ฉัน หิว ข้าว'))
    print(ARTagger.tag('ฉัน หิว ข้าว'))
    tags = ARTagger.tag('ฉัน หิว ข้าว')
