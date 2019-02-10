''' very basic html gui '''

# constants
HEADERS = [('ID', 'name'),
            ('DLC', 'dlc'),
            ('Analysis', 'atype'),
            ('Wind Speed (m/s)', 'vwind'),
            ('Wind Dir (deg)', 'wavdir'),
            ('Yaw Error (deg)', 'yawerr'),
            ('Wind Seed', 'winseed'),
            ('Sea State', 'seastate'),
            ('Hs (m)', 'hs'),
            ('Tp (s)', 'tp'),
            ('Wave Dir (deg)', 'wavdir'),
            ('Wave Seed', 'wavseed'),
            ('Current Model', 'current'),
            ('Water Level', 'wlevel'),
            ('Water Depth (m)', 'wdepth')]

class Gui():
    ''' gui object'''

    def __init__(self, dlcset, opath):
        self.dlcset = dlcset
        self.opath = opath
        self.html = self.html_table()

    def write(self, opath=None):
        ''' write out html file'''
        if not opath == None:
            self.opath = opath

        with open(self.opath, 'w') as fout:
            fout.write(self.html)

        return None

    def html_table(self):
        tbstr = '<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n'
        tbstr += '<img src="https://upload.wikimedia.org/wikipedia/commons/6/6f/Atkins-snc-lavalin-logo.svg" style="height: 50px; padding-right:25px">'
        tbstr += '<b>DLC Table</b>'
        tbstr += '<div class="w3-responsive" style="width: 100%">\n'
        tbstr += '<table class="w3-table w3-striped w3-border w3-small w3-centered">\n{row}</table>'
        tbstr += '</div>'
        tstr = '  <tr>\n{cell}  </tr>\n'
        cstr = '    <td>{cont}</td>\n'
        rows = ''
        hstr = '    <th>{cont}</th>\n'
        hrow = ''
        for h in HEADERS:
            hrow += hstr.format(cont=h[0])
        rows += tstr.format(cell=hrow)
    
        for case in self.dlcset:
            vals = ''
            for h in HEADERS:
                v = getattr(case, h[1])
                if type(v) == float:
                    v = round(v,2)
                vals += cstr.format(cont=v)
            rows += tstr.format(cell=vals)
        return tbstr.format(row=rows)
