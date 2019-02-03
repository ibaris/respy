# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def test(*args):
    print args
    #for item in args.keys():
    #    print item
        
t = {'a':3, 'b':5}

import pandas as pd

class SubclassedSeries(pd.Series):

    @property
    def _constructor(self):
        return SubclassedSeries

    @property
    def _constructor_expanddim(self):
        return SubclassedDataFrame

    def __repr__(self):
        print "yep!"
        
class SubclassedDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return SubclassedDataFrame

    @property
    def _constructor_sliced(self):
        return SubclassedSeries
    
    def make_text_for_repr(self):
        text = str(self).split('\n')
        header = text[0]
        body = [text[1:][i].split() for i in range(len(text[1:]))]
        header_split = header.split()
        dtypes = [self.dtypes[item] for item in header_split]
        stripes = [self.make_stripe(len(str(item))) for item in dtypes]


        len_header = [len(item) for item in header_split]
        len_stripes = [len(item) for item in stripes]
                       
        stripes_align = list()
        header_align = list()
        dtype_align = list()
        body_align = list() 
        
        for i in range(len(len_header)):
            lheader = len_header[i]
            lstripes = len_stripes[i]
            
            if lheader > lstripes:
                 header_align.append(header_split[i])
                 stripes_align.append(stripes[i].rjust(lheader))
                 dtype_align.append(str(dtypes[i]).rjust(lheader))
            else:
                 header_align.append(header_split[i].rjust(lstripes))
                 stripes_align.append(stripes[i])
                 dtype_align.append(str(dtypes[i]))

        for i in range(len(body)):
            lheader = len_header[i]
            lstripes = len_stripes[i]

            if lheader > lstripes:
                 body_align.append([body[i][j].rjust(lheader) for j in range(len(body[i]))])
            else:
                 body_align.append([body[i][j].rjust(lstripes) for j in range(len(body[i]))])
            
            body_align[i][0] = body_align[i][0].split()[0]

        body_text = list()
        
        
        for i in range(len(body_align)):
            body_temp = ''
            for j in range(len(body_align[i])):
                if j == len(body_align[i])-1:
                    body_temp += body_align[i][j]
                else:
                    body_temp += body_align[i][j] + '  '
            
            body_text.append(body_temp)
        
        space = ''
        for item in header:
            if item is ' ':
                space += item
            else:
                break

        dtype_temp = ''
        stripes_temp = ''
        header_temp = ''
        for i in range(len(header_split)):
            if i == len(header_split)-1:
                dtype_temp += dtype_align[i]
                stripes_temp += stripes_align[i]
                header_temp += header_align[i]
            else:
                dtype_temp += dtype_align[i]  + '  '
                stripes_temp += stripes_align[i] + '  '
                header_temp += header_align[i] + '  '
        
        items = [header_temp, dtype_temp, stripes_temp]
            
        
#        for i in range(len(body_text)):
#            body_text[i] = space + body_text[i]

        for i in range(len(items)):
            items[i] = space + items[i]

        text_header = ''
        for i in range(len(items)):
            text_header += items[i] + '\n'
            
        text_body = ''
        for i in range(len(body_text)):
            text_body += body_text[i] + '\n'
            
        total_text = text_header + text_body
        #print total_text
        
        return total_text
    
    def space(self, n):
        space = ''
        for i in range(n):
            space += ' '
        return space
            
    def __repr__(self):
        text = str(self).split('\n')
        header  = text[0]
        if self.index.name is None:
            body_all = [text[1:][i].split() for i in range(len(text[1:]))]
            index_name = None
        else:
            index_name = text[1].split()
            body_all = [text[2:][i].split() for i in range(len(text[2:]))]
        
        index = list()
        
        body = list()
        for i in range(len(body_all)):
            body_atom = list()
            for j in range(len(body_all[i])):
                if j == 0:
                    index.append(body_all[i][j])
                else:
                    body_atom.append(body_all[i][j])
            body.append(body_atom)
            
        header_split = header.split()
        dtypes = [self.dtypes[item] for item in header_split]
        stripes = [self.make_stripe(len(str(item))) for item in dtypes]


        len_header = [len(item) for item in header_split]
        len_stripes = [len(item) for item in stripes]
        len_index_name = len(index_name[0])
        len_index = [len(item) for item in index]
                       
        stripes_align = list()
        header_align = list()
        dtype_align = list()
        body_align = list() 
    
        for i in range(len(len_header)):
            lheader = len_header[i]
            lstripes = len_stripes[i]
            lindexname = len_index_name
            lindex = len_index[i]
            
            prefix = [lindexname, lindex]
            spaces = [lheader, lstripes, lindexname, lindex]
            max_len = max(spaces)
            max_prefix = max(prefix)
            
            if i ==  0:
                sp = self.space(max_prefix + 2)
            else:
                sp = ''
                
            header_align.append(sp + header_split[i].rjust(max_len))
            stripes_align.append(sp + stripes[i].rjust(max_len))
            dtype_align.append(sp + str(dtypes[i]).rjust(max_len))
            

        for i in range(len(body)):
            lheader = len_header[i]
            lstripes = len_stripes[i]
            lindexname = len_index_name
            lindex = len_index[i]
            
            prefix = [lindexname, lindex]
            spaces = [lheader, lstripes, lindexname, lindex]
            max_len = max(spaces)
            max_prefix = max(prefix)
            sp = self.space(max_prefix + 2)
            
            body[i][0] = sp + body[i][0]
            
                
            body_align.append([body[i][j].rjust(max_len) for j in range(len(body[i]))])
            

        body_text = list()
        
        
        for i in range(len(body_align)):
            body_temp = ''
            for j in range(len(body_align[i])):
                if j == len(body_align[i])-1 or j == 0:
                    body_temp += body_align[i][j]
                else:
                    body_temp += body_align[i][j] + '  '
            
            body_text.append(body_temp)
        
        space = ''
        for item in header:
            if item is ' ':
                space += item
            else:
                break

        dtype_temp = ''
        stripes_temp = ''
        header_temp = ''
        
        for i in range(len(header_split)):
            if i == len(header_split)-1:
                dtype_temp += dtype_align[i]
                stripes_temp += stripes_align[i]
                header_temp += header_align[i]
            else:
                dtype_temp += dtype_align[i]  + '  '
                stripes_temp += stripes_align[i] + '  '
                header_temp += header_align[i] + '  '
        
        items = [header_temp, dtype_temp, stripes_temp, index_name[0]]
            
        
#        for i in range(len(body_text)):
#            body_text[i] = space + body_text[i]

        for i in range(len(items)):
            items[i] = items[i]

        text_header = ''
        for i in range(len(items)):
            text_header += items[i] + '\n'
            
        text_body = ''
        for i in range(len(body_text)):
            text_body += body_text[i] + '\n'
            
        total_text = text_header + text_body
        
        return total_text
        
    def make_stripe(self, n):
        stripe = ''
        
        for i in range(n):
            stripe += '-'
            
        return stripe
        
df = SubclassedDataFrame({'Index': [1, 2, 3], 'CCC': [1, 2, 3], 'BBB': [4, 5, 6], 'AAA': [7, 8, 9]})
self = df

print df
df2 = df.set_index('Index')
self = df2

#df = pd.DataFrame({'Index': [1, 2, 3], 'CCC': [1, 2, 3], 'BBB': [4, 5, 6], 'AAA': [7, 8, 9]})
#df2 = df.set_index('Index')
