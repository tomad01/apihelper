import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pdb,os
from collections import defaultdict

def hist(a):
    d = defaultdict(int)
    for i in a:
      d[i] += 1
    return zip(*sorted(d.iteritems(), key=lambda x: x[0],reverse=False))

def binar_plot(data,show=True,save=False,path='./figures/'):

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)

    label1,label2 = data.keys()
    attributes    = data[label1].keys()
    attributes.remove('timestamp')
    attr1,attr2   = attributes
    
    ax1.plot_date(data[label1]['timestamp'],data[label1][attr1],'b*',markersize=10.0,label=label1)
    ax1.plot_date(data[label2]['timestamp'],data[label2][attr1],'r*',markersize=10.0,label=label2)
    ax1.plot_date(data[label1]['timestamp'],data[label1][attr2],'bo',markersize=10.0,label=label1)
    ax1.plot_date(data[label2]['timestamp'],data[label2][attr2],'ro',markersize=10.0,label=label2)
    
    ax1.grid(True)
    
    
    ax1.title.set_text(attr1+' and '+attr2)
    
    
    legend = ax1.legend(loc='upper right', shadow=True)
    legend.draggable()
##    fig.suptitle(name, fontsize=20)
##    path = os.path.join(path.rstrip('/')+'/',name.replace('/','')+'.png')
    if save:
        fig.savefig(path,dpi=1000)
    if show:
        plt.show()
    plt.close(fig)    
##    return os.path.abspath(path)

def gb_dt_plot(name,ig,good,ib,bad,labels,show=False,save=True,path='./figures/'):
##    lg = len(good);lb = len(bad)
##    Mg = max(good);Mb = max(bad)
##    mg = min(good);mb = min(bad)
##    Mig = max(ig);Mib = max(ib)
    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    try:
        ax1.plot_date(ig,good,'b*',markersize=10.0,label=labels[0])
        ax1.plot_date(ib,bad,'r*',markersize=10.0,label=labels[1])
        x,y=hist(good)        
        ax2.bar(x,y,color="blue")
        x,y=hist(bad)
        ax3.bar(x,y,color="red")
    except Exception as er:
        print str(er)
        pdb.set_trace()

##    xlimM = Mig if Mig>Mib else Mib
##    xlimM = xlimM +20*xlimM/100.0
##    
##    ylimM = Mg if Mg>Mb else Mb
##    ylimM = ylimM +20*ylimM/100.0
##    
##    ylim = mg if mg<mb else mb
##    ylim = ylim -40*ylim/100.0
##
##    ax1.set_xlim([0, xlimM])
##    ax1.set_ylim([ylim, ylimM])
##    ax2.set_xlim([0, xlimM])
##    ax2.set_ylim([ylim, ylimM])
##    ax3.set_xlim([0, xlimM])
##    ax3.set_ylim([ylim, ylimM])
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    legend = ax1.legend(loc='upper right', shadow=True)
    legend.draggable()
    fig.suptitle(name, fontsize=20)
    path = os.path.join(path.rstrip('/')+'/',name.replace('/','')+'.png')
    if save:
        fig.savefig(path,dpi=1000)
    if show:
        plt.show()
    plt.close(fig)    
    return os.path.abspath(path)

def good_bad_plot(name,ig,good,ib,bad,show=False,save=True,path='./figures/'):

    lg = len(good);lb = len(bad)
    Mg = max(good);Mb = max(bad)
    mg = min(good);mb = min(bad)
    Mig = max(ig);Mib = max(ib)
    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    
    ax1.plot(ig,good,'b*',markersize=10.0,label='good')
    ax1.plot(ib,bad,'r*',markersize=10.0,label='bad')
    ax2.plot(ig,good,'b*',markersize=10.0,label='good')
    ax3.plot(ib,bad,'r*',markersize=10.0,label='bad')

    xlimM = Mig if Mig>Mib else Mib
    xlimM = xlimM +20*xlimM/100.0
    
    ylimM = Mg if Mg>Mb else Mb
    ylimM = ylimM +20*ylimM/100.0
    
    ylim = mg if mg<mb else mb
    ylim = ylim -40*ylim/100.0

    ax1.set_xlim([0, xlimM])
    ax1.set_ylim([ylim, ylimM])
    ax2.set_xlim([0, xlimM])
    ax2.set_ylim([ylim, ylimM])
    ax3.set_xlim([0, xlimM])
    ax3.set_ylim([ylim, ylimM])
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    legend = ax1.legend(loc='upper right', shadow=True)
    legend.draggable()
    fig.suptitle(name, fontsize=20)
    path = os.path.join(path.rstrip('/')+'/',name.replace('/','')+'.png')
    if save:
        fig.savefig(path,dpi=1000)
    if show:
        plt.show()
    plt.close(fig)
    
    return os.path.abspath(path)

def plot_date(time_date,data,ax,fmt,label,val):
    
    def autocorr(x):
        result = np.correlate(x, x, mode='full')
        return result
    
    def gaussian(x,mu,std):        
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(std, 2.)))/std*math.sqrt(2*math.pi)

    def group_by_weeks_dt(dt_ob,vals):
        weeks = map(lambda x: datetime.strptime('-'.join([str(i) for i in x.isocalendar()[0:2]])+'-0','%Y-%W-%w'),dt_ob)
        group = {k:0 for k in set(weeks)}
        for i,w in enumerate(weeks):
            group[w]+=vals[i]
        key = max(group.iteritems(), key=itemgetter(1))[0]   
        return sorted(group.keys()),group[key]

    def group_by_weeks(dt_ob,vals):
        weeks = [i.isocalendar()[1] for i in dt_ob]
        group = {k:0 for k in set(weeks)}
        for i,w in enumerate(weeks):
            group[w]+=vals[i]
        return zip(*group.items())
    
    def group_by_days(dt_ob,vals):        
        weeks = [datetime(i.year,i.month,i.day) for i in dt_ob]
        group = {k:0 for k in set(weeks)}
        for i,w in enumerate(weeks):
            group[w]+=vals[i]        
        return zip(*sorted(group.items(), key=lambda p: p[0], reverse=False))


    if not data:
        print 'not found:',item
        return ax,0
    if unicode==type(time_date[0]):
        times = [datetime.strptime(i,'%d-%m-%Y %H:%M:%S.%f') for i in time_date]            

    unix = map(lambda x:(x - datetime(1970,1,1)).total_seconds(),times)
    diff = [(times[i]-times[i-1]).total_seconds() for i in range(1,len(times))]
    
    x,y   = group_by_days(times,[1]*len(times))
    wk,mv = group_by_weeks_dt(times,[1]*len(times))
    ax.plot_date(x=x, y=y, fmt=fmt[0]+'-',markersize=10.0,label=label)
    for item in wk:
        ax.plot_date(x=[item,item], y=[0,mv], fmt='r-',markersize=10.0)
    ax.grid(True)

    fig = ax.get_figure()
    ax2 = fig.add_subplot(312)
    ax2.plot(y,gaussian(y),fmt[0]+'-',markersize=10.0,label=label)
    ax2.grid(True)
    
if __name__=="__main__":
    good_bad_plot('test',[1,2,4],[1,2,34],[4,5,6],[44,56,32])
