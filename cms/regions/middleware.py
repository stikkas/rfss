from cms.regions import get_region_finder


class RegionDefinitionMiddleware(object):
    def process_request(self, request):
        finder = get_region_finder()
        finder.definition_region(request)
