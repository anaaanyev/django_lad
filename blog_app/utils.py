from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import QuerySet
from blog_app.models import Post

def q_search(
        query: str,
        posts: QuerySet[Post],
        headline_min_words: int = 5,
        headline_max_words: int = 15,
):
    vector = (
            SearchVector("title", weight="A", config="russian") +
            SearchVector("content", weight="B", config="russian") +
            SearchVector("category__title", weight="C", config="russian") +
            SearchVector("author__username", weight="D", config="russian")
    )

    search_query = SearchQuery(query, config="russian")

    headline = SearchHeadline(
        "content",
        search_query,
        config="russian",
        start_sel="<b>",
        stop_sel="</b>",
        max_words=headline_max_words,
        min_words=headline_min_words
    )

    queryset = (
        posts.annotate(
            rank=SearchRank(vector, search_query),
            headline=headline
        )
        .filter(rank__gte=0.01)
        .order_by("-rank")
    )

    return queryset
