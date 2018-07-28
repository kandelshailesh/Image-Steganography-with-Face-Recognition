try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url
# from friendship.views import view_friends,test_view_friends, friendship_add_friend,friendship_remove_friend, friendship_accept, \
#     friendship_reject, friendship_cancel, friendship_request_list, \
#     friendship_request_list_rejected, friendship_requests_detail, followers,\
#     following, follower_add, follower_remove, all_users,block_add,block_remove,blockers,blocking

from . import views




urlpatterns = [
    url(r'^users/$',views.all_users,
        name='friendship_view_users',
    ),
    url(
        r'^friends/(?P<username>[\w-]+)/$',
        views.view_friends,
        name='friendship_view_friends',
    ),
    url(
        r'^test/$',
        views.test_view_friends,
        name='test_friendship_view_friends',
    ),

    url(
        r'^friend/add/(?P<to_username>[\w-]+)/$',
        views.friendship_add_friend,
        name='friendship_add_friend',
    ),
    url(
        r'^friend/remove/(?P<to_username>[\w-]+)/$',
        views.friendship_remove_friend,
        name='friendship_remove_friend',
    ),
    url(
        r'^friend/accept/(?P<friendship_request_id>\d+)/$',
        views.friendship_accept,
        name='friendship_accept',
    ),
    url(
        r'^friend/reject/(?P<friendship_request_id>\d+)/$',
        views.friendship_reject,
        name='friendship_reject',
    ),
    url(
        r'^friend/cancel/(?P<friendship_request_id>\d+)/$',
        views.friendship_cancel,
        name='friendship_cancel',
    ),
    url(
        r'^friend/requests/$',
        views.friendship_request_list,
        name='friendship_request_list',
    ),
    url(
        r'^friend/requests/rejected/$',
        views.friendship_request_list_rejected,
        name='friendship_requests_rejected',
    ),
    url(
        r'^friend/request/(?P<friendship_request_id>\d+)/$',
        views.friendship_requests_detail,
        name='friendship_requests_detail',
    ),
    # url(
    #     r'^followers/(?P<username>[\w-]+)/$',
    #     views.followers,
    #     name='friendship_followers',
    # ),
    # url(
    #     r'^following/(?P<username>[\w-]+)/$',
    #     views.following,
    #     name='friendship_following',
    # ),
    # url(
    #     r'^follower/add/(?P<followee_username>[\w-]+)/$',
    #     views.follower_add,
    #     name='follower_add',
    # ),
    # url(
    #     r'^follower/remove/(?P<followee_username>[\w-]+)/$',
    #     views.follower_remove,
    #     name='follower_remove',
    # ),
    # url(
    #     r'^blockers/(?P<username>[\w-]+)/$',
    #     views.blockers,
    #     name='friendship_blockers',
    # ),
    # url(
    #     r'^blocking/(?P<username>[\w-]+)/$',
    #     views.blocking,
    #     name='friendship_blocking',
    # ),
    # url(
    #     r'^block/add/(?P<blocked_username>[\w-]+)/$',
    #     views.block_add,
    #     name='block_add',
    # ),
    # url(
    #     r'^block/remove/(?P<blocked_username>[\w-]+)/$',
    #     views.block_remove,
    #     name='block_remove',
    # ),
]
