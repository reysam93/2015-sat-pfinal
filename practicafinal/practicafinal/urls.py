from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_URL2}),
    url(r'^css/style.css$', 'activities.views.serveCSS'),
    url(r'^login$', 'activities.views.loggingIn'),
    url(r'^logout$', 'activities.views.loggingOut'),
    url(r'^$', 'activities.views.mainPage'),
    url(r'^update', 'activities.views.updateActs'),
    url(r'^rss$', 'activities.views.getMainRSS'),
    url(r'^todas$', 'activities.views.getAll'),
    url(r'^edituserpage', 'activities.views.editUserPage'),
    url(r'^signin$', 'activities.views.signin'),
    url(r'^ayuda$', 'activities.views.sendHelp'),
    url(r'^actividad/([\d]+)$', 'activities.views.getActivity'),
    url(r'^actividad/([\d]+)/add$', 'activities.views.addActivity'),
    url(r'^actividad/([\d]+)/delete$', 'activities.views.delActivity'),
    url(r'^like/([\d]+)', 'activities.views.addLikes'),
    url(r'^dontlike/([\d]+)', 'activities.views.subLikes'),
    url(r'^newcomment/([\d]+)', 'activities.views.addComment'),
    url(r'^([a-zA-Z0-9@.+-_]*)/rss$', 'activities.views.getRSS'),
    url(r'^([a-zA-Z0-9@.+-_]*)$', 'activities.views.getUserPage'),
)
