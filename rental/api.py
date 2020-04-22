from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin
from . import api_views


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
friends = router.register(r'friends', api_views.FriendViewset)
friends.register(
    r'borrowings',
    api_views.BorrowedViewset,
    basename='friend-borrow',
    parents_query_lookups=['to_who'],
)
router.register(r'belongings', api_views.BelongingViewset)
router.register(r'borrowings', api_views.BorrowingsViewset)
