''' outline class definitions for a DLC table tool '''
# imports
from collections import OrderedDict
import pickle, uuid
import random

from gui import Gui

class DLCSet():
    ''' class represeting a set of load cases'''
    def __init__(self, name=None, cases=None):
        if not name == None:
            self.name = name
        else:
            # generate a unique names
            self.name = uuid.uuid4().hex

        if not cases == None:
            self.cases = cases
        else:
            self.cases = OrderedDict()

    def __len__(self):
        ''' return number of LoadCase objects in set'''
        return len(self.cases.values())

    def __iter__(self):
        ''' alow iteration over LoadCase objects in set'''
        return iter(self.cases.values())

    def __getitem__(self, k):
        ''' allow indexing by case names'''
        return self.cases[k]

    def add(self, case):
        ''' add a load case to the set'''
        self.cases[case.name] = case
        return None

    def nfilter(self, param, cond):
        ''' numeric filter (greater, less, equal, operators etc.)'''
        odict = tuple((k, v) for k, v in self.cases.items() if eval('%s%s' % (getattr(v, param), cond)))
        return DLCSet(cases=OrderedDict(odict))

    def ifilter(self, param, val):
        ''' iterator filter (find character in string etc.)'''
        odict = tuple((k, v) for k, v in self.cases.items() if val in getattr(v, param))
        return DLCSet(cases=OrderedDict(odict))

    def save(self, spath):
        ''' serialise and creat .dlc save file'''
        with open(spath, 'wb') as fout:
            pickle.dump(self, fout)
        return None

    def export(self, opath, format):
        ''' e.g. export to Fatigue Manger table '''
        return None

class LoadCase():
    ''' class representing a single load case'''
    def __init__(self, name=None, **kwargs):
        if not name == None:
            self.name = name
        else:
            # generate a unique names
            self.name = uuid.uuid4().hex
        # case info
        self.dlc = kwargs.pop('dlc')
        self.atype = kwargs.pop('atype')
        # wave and current
        self.seastate = kwargs.pop('seastate')
        self.hs = kwargs.pop('hs')
        self.tp = kwargs.pop('tp')
        self.wavdir = kwargs.pop('wavdir')
        self.wavseed = kwargs.pop('wavseed')
        self.current = kwargs.pop('current')
        self.wlevel = kwargs.pop('wlevel')
        self.wdepth = kwargs.pop('wdepth')
        # wind
        self.vwind = kwargs.pop('vwind')
        self.windir = kwargs.pop('windir')
        self.yawerr = kwargs.pop('yawerr')
        self.winseed = kwargs.pop('winseed')

# functions
def load(lpath):
    ''' load in a serialised .dlc file'''
    with open(lpath, 'rb') as fin:
        content = pickle.load(fin)
    return content

# testing
myset = DLCSet()

for x in range(13000):
    if x % 100 == 0:
        print('%s cases added...' % x)
    idict = OrderedDict()
    idict['dlc'] = ('1.2', '6.2', '6.4')[random.randrange(3)]
    if idict['dlc'] == '6.2':
        idict['atype'] = 'ULS'
        idict['seastate'] = 'ESS'
    else:
        idict['atype'] = 'FLS'
        idict['seastate'] = 'NSS'
    idict['hs'] = random.random()*10.0
    idict['tp'] = random.random()*10.0
    idict['wavdir'] = random.randrange(360)
    idict['wavseed'] = random.randrange(9999)
    idict['current'] = ('ECM', 'NCM')[random.randrange(2)]
    idict['wlevel'] = ('50yUWL', 'MSL')[random.randrange(2)]
    idict['wdepth'] = 50.0
    idict['vwind'] = random.random()*20.0
    idict['windir'] = random.randrange(360)
    idict['yawerr'] = (-8.0, 0.0, 8.0)[random.randrange(3)]
    idict['winseed'] = random.randrange(9999)
    myset.add(LoadCase('{v:04d}'.format(v=x+1),**idict))

myset.save('bigdlc.dlc')
myset = load('bigdlc.dlc')

for case in myset.nfilter('hs', '>7').ifilter('current', 'ECM').cases.values():
    print(case.name, case.dlc, round(case.hs,2), round(case.tp,2), case.wavdir, case.current)

g = Gui(myset, 'gui.html')
g.write()
