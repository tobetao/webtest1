import urllib

alltksurl='http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&render=download'

alltks=[i.split('"')[1] for i in urllib.urlopen(alltksurl).readlines()[1:]]