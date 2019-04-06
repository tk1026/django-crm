from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),

    url(r'^leads_list/', views.LeadsView.as_view(), name='leads'),
    url(r'^leads/create', views.create_leads, name='create_leads'),
    url(r'^leads/edit/(\d+)', views.edit_leads, name='edit_leads'),
    url(r'^leads/detail/(\d+)', views.detail_leads, name='detail_leads'),
    url(r'^leads/tasks_edit/(\d+)', views.leads_tasks_edit, name='leads_tasks_edit'),

    url(r'^contacts_list/', views.contacts_list, name='contacts_list'),
    url(r'^contacts/create', views.contacts, name='create_contacts'),
    url(r'^contacts/edit/(\d+)', views.contacts, name='edit_contacts'),
    url(r'^contacts/detail/(\d+)', views.detail_contacts, name='detail_contacts'),

    url(r'^accounts_list/', views.accounts_list, name='accounts_list'),
    url(r'^accounts/create', views.accounts, name='create_accounts'),
    url(r'^accounts/edit(\d+)', views.accounts, name='edit_accounts'),
    url(r'^accounts/detail(\d+)', views.detail_accounts, name='detail_accounts'),

    url(r'^potentials_list/', views.PotentialsView.as_view(), name='potentials_list'),
    url(r'^potentials/create', views.potentials, name='create_potentials'),
    url(r'^potentials/edit/(\d+)', views.potentials, name='edit_potentials'),
    url(r'^potentials/detail/(\d+)', views.detail_potentials, name='detail_potentials'),

]
