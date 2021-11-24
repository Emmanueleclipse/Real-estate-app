from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout_then_login
from django.views.static import serve as serve_static
import settings
from agents.views import HomePageView, PreferencesView, HelpView, AnnoncesView, AgencesView, AgenceView, AgentsView, UpdateAgenciesView, json_agences, json_agents, json_monagence
from clients.views import ClientsView, ClientView, BuyersView, SellersView, ClientLeadsView, json_contacts_client, json_buyers, json_sellers, json_recent_activities, json_clients, json_clientleads, csv_clientleads, json_addclientlead, contactform
from simulations.views import SimulationMortgageView, SimulationCapitalGainsView, SimulationSeasonalRentalView
from finance.views import SommaireFinanceView, SuppliersView, json_suppliers, SuppliersFactureView, json_suppliers_facture, SuppliersFactureView, BankAccountView, json_banks, json_bankentries, json_bankupload, NotairesFactureView, json_notaire_factures, AgentsFactureView, json_agent_factures, ApporteursFactureView, json_apporteur_factures
from todo.views import ToDoView,json_todo
from chat.views import ChatView,GroupChatView,json_chat,json_unreadchat,json_listchat,json_groupchat
from news.views import json_news
from property.views import MandatsView
import oauth2_provider.views as oauth2_views
from django.contrib.auth import views as auth_views 

admin.autodiscover()

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
	url(r'^$', login_required(HomePageView.as_view())),

	url(r'^profile/$', login_required(PreferencesView.as_view())),
	url(r'^help/$', login_required(HelpView.as_view())),
	url(r'^annonces/(?P<days>[0-9]+)/$', login_required(AnnoncesView.as_view())),
	url(r'^agences/$', login_required(AgencesView.as_view())),
	url(r'^monagence/$', login_required(AgenceView.as_view())),
	url(r'^agence/$', login_required(AgenceView.as_view())),
	url(r'^agents/$', login_required(AgentsView.as_view())),
	url(r'^updateagencies/$', login_required(UpdateAgenciesView.as_view())),

	url(r'^clients/$', login_required(ClientsView.as_view())),
	url(r'^client/$', login_required(ClientView.as_view())),
	url(r'^client/(?P<clientid>[0-9]+)/$', login_required(ClientView.as_view())),
	url(r'^acheteurs/$', login_required(BuyersView.as_view())),
	url(r'^vendeurs/$', login_required(SellersView.as_view())),
	url(r'^clientleads/$', login_required(ClientLeadsView.as_view())),

	url(r'^taches/$', login_required(ToDoView.as_view())),

	url(r'^chat/$', login_required(ChatView.as_view())),
	url(r'^groupchat/$', login_required(GroupChatView.as_view())),

	url(r'^simulation-credit/$', login_required(SimulationMortgageView.as_view())),
	url(r'^simulation-plusvalue/$', login_required(SimulationCapitalGainsView.as_view())),
	url(r'^simulation-saisonniere/$', login_required(SimulationSeasonalRentalView.as_view())),

	url(r'^suppliers/$', login_required(SuppliersView.as_view())),
	url(r'^suppliers_facture/$', login_required(SuppliersFactureView.as_view())),
	url(r'^banque/$', login_required(BankAccountView.as_view())),
	url(r'^facture_notaire/$', login_required(NotairesFactureView.as_view())),
	url(r'^facture_agent/$', login_required(AgentsFactureView.as_view())),
	url(r'^facture_apporteur/$', login_required(ApporteursFactureView.as_view())),
	url(r'^sommaire_finance/$', login_required(SommaireFinanceView.as_view())),

	url(r'^json_agences/$', login_required(json_agences)),
	url(r'^json_agents/$', login_required(json_agents)),
	url(r'^json_monagence/$', login_required(json_monagence)),
	url(r'^json_clients/$', login_required(json_clients)),
	url(r'^json_contacts_client/$', login_required(json_contacts_client)),
	url(r'^json_buyers/$', login_required(json_buyers)),
	url(r'^json_sellers/$', login_required(json_sellers)),
	url(r'^json_recent_activities/$', login_required(json_recent_activities)),
	url(r'^json_todo/$', login_required(json_todo)),
	url(r'^json_chat/$', login_required(json_chat)),
	url(r'^json_unreadchat/$', login_required(json_unreadchat)),
	url(r'^json_listchat/$', login_required(json_listchat)),
	url(r'^json_groupchat/$', login_required(json_groupchat)),
	url(r'^json_news/$', login_required(json_news)),
	url(r'^json_clientleads/$', login_required(json_clientleads)),
	url(r'^csv_clientleads/$', login_required(csv_clientleads)),
	url(r'^json_addclientlead/$', login_required(json_addclientlead)),
	url(r'^json_suppliers/$', login_required(json_suppliers)),
	url(r'^json_suppliers_facture/$', login_required(json_suppliers_facture)),
	url(r'^json_banks/$', login_required(json_banks)),
	url(r'^json_bankentries/$', login_required(json_bankentries)),
	url(r'^json_bankupload/$', login_required(json_bankupload)),
	url(r'^json_notaire_factures/$', login_required(json_notaire_factures)),
	url(r'^json_agent_factures/$', login_required(json_agent_factures)),
	url(r'^json_apporteur_factures/$', login_required(json_apporteur_factures)),

	url(r'^mandats/$', login_required(MandatsView.as_view())),

	url(r'^contactform/$', contactform),

	url(r'', include('user_sessions.urls', 'user_sessions')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name="login"),
	url(r'^accounts/logout/$', logout_then_login),
	url(r'^static/(?P<path>.*)$', serve_static, {'document_root' : settings.STATIC_ROOT} ),

	url(r'^o/', include(oauth2_endpoint_views, namespace="oauth2_provider")),
	url(r'^s3direct/', include('s3direct.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


