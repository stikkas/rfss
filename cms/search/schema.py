from whoosh import fields
try:
    import Stemmer
    from cms.search.morphology.russian import StemmingAnalyzer
except ImportError:
    from whoosh.analysis import StemmingAnalyzer


PAGE_SCHEMA = fields.Schema(
    id=fields.NUMERIC(stored=True, unique=True),
    region=fields.NUMERIC,
    name=fields.TEXT(analyzer=StemmingAnalyzer()),
    content=fields.TEXT(analyzer=StemmingAnalyzer()),
)
