# -*- coding: utf-8 -*-
import json
from django.shortcuts import get_object_or_404

from cms.regions import get_region
from cms.views.utils import render
from cms.views.decorators import cms_protector
from cms.metrika import api as metrika
from cms.metrika.models import Counter


@cms_protector
def statistic(request):
    date1 = ''
    date2 = ''
    if request.method == 'POST':
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')
    return render(request, 'cms/metrika.html', {
        'date1': date1,
        'date2': date2,
    })

@cms_protector
def traffic(request, **params):
    counter = get_object_or_404(Counter, region=get_region())
    api = metrika.get_api(counter)
    return render(request, 'cms/metrika/traffic.html', {
        'traffic': json.load(api.get_stat_traffic_summary(**params))
    })

@cms_protector
def traffic_hourly(request, **params):
    counter = get_object_or_404(Counter, region=get_region())
    api = metrika.get_api(counter)
    return render(request, 'cms/metrika/traffic_hourly.html', {
        'traffic_hourly': json.load(api.get_stat_traffic_hourly(**params))
    })

@cms_protector
def sources(request, **params):
    counter = get_object_or_404(Counter, region=get_region())
    api = metrika.get_api(counter)
    return render(request, 'cms/metrika/sources.html', {
        'sources': json.load(api.get_stat_sources_summary(**params))
    })

@cms_protector
def browsers(request, **params):
    counter = get_object_or_404(Counter, region=get_region())
    api = metrika.get_api(counter)

    ms_browsers = ['Firefox', 'MSIE', 'Opera', 'Google Chrome',
                   'Mobile Safari', 'Safari', 'Opera Mini']
    browsers = json.load(api.get_stat_tech_browsers(table_mode='tree', **params)),
    browsers = [b for b in browsers[0]['data']
                if b['name'] in ms_browsers]

    def cmp (x, y):
        if x['version'] > y['version']: return 1
        if x['version'] == y['version']: return 0
        if x['version'] < y['version']: return -1

    for b in browsers:
        b['chld'].sort(cmp=cmp, reverse=True)

    return render(request, 'cms/metrika/browsers.html', {
        'browsers': browsers,
    })

@cms_protector
def countries(request, **params):
    counter = get_object_or_404(Counter, region=get_region())
    api = metrika.get_api(counter)
    countries = json.load(api.get_stat_geo(**params)),
    for country in countries[0]['data']:
        if metrika.COUNTRIES.get(country['name']):
            country['code'] = metrika.COUNTRIES.get(country['name'])

    return render(request, 'cms/metrika/countries.html', {
        'countries': countries[0],
    })

@cms_protector
def regions(request, **params):
    counter = get_object_or_404(Counter, region=get_region())
    api = metrika.get_api(counter)
    regions = json.load(api.get_stat_geo(table_mode='tree', **params))

    eurasia = [e for e in regions['data'] if e['name'] == u'Евразия'][0]
    russia = [r for r in eurasia['chld'] if r['name'] == u'Россия'][0]

    for d in russia['chld']:
        if d.get('chld'):
            for r in d['chld']:
                if metrika.REGIONS.get(r['name']):
                    # Not given RU-MOW and RU-SPE
                    r['code'] = metrika.REGIONS[r['name']]

    return render(request, 'cms/metrika/regions.html', {
        'regions': russia,
    })
