from .bookmarks import Favorites


def favorite(request):
    return {'favorite': Favorites(request)}
