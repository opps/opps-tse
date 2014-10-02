# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Candidate, PoliticalParty, Election, Vote


class CandidateAdmin(admin.ModelAdmin):

    search_fields = ['name', 'number']

    list_filter = ('political_party', )

    raw_id_fields = ['vice', ]

    list_display = (
        'name', 'slug', 'number', 'union', 'political_party'
    )


class PoliticalPartyAdmin(admin.ModelAdmin):

    search_fields = ['name', 'slug', 'number']

    list_filter = ('number', 'slug')

    list_display = (
        'name', 'slug', 'number',
    )


class ElectionAdmin(admin.ModelAdmin):

    list_filter = ['year', 'job', 'state']

    list_display = (
        'year', 'job', 'state',
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

    list_display = (
        'election', 'turn', 'candidate',
        'votes', 'is_elected'
    )

    list_filter = ('election', 'turn')

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(PoliticalParty, PoliticalPartyAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Vote, VoteAdmin)
