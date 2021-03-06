# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Candidate, PoliticalParty, Election, Vote


class CandidateAdmin(admin.ModelAdmin):

    search_fields = ['name', 'number']

    list_filter = ('political_party', 'is_active')

    raw_id_fields = ['vice', 'political_party']

    list_display = (
        'name', 'slug', 'number', 'union', 'political_party', 'is_active'
    )


class PoliticalPartyAdmin(admin.ModelAdmin):

    search_fields = ['name', 'slug', 'number']

    list_filter = ('number', 'slug')

    list_display = (
        'name', 'slug', 'number',
    )


class ElectionAdmin(admin.ModelAdmin):

    list_filter = ['year', 'turn', 'state', 'job', ]

    list_display = (
        'year', 'turn', 'state', 'job'
    )


class VoteAdmin(admin.ModelAdmin):

    search_fields = [
        'candidate__name',
        'candidate__number',
    ]

    list_filter = [
        'election',
        'candidate',
        'votes',
    ]

    raw_id_fields = ['election', 'candidate']

    list_display = (
        'election', 'turn', 'candidate',
        'votes', 'is_elected'
    )

    list_filter = ('election', 'turn')

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(PoliticalParty, PoliticalPartyAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Vote, VoteAdmin)
