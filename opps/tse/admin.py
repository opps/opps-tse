# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Candidate, PoliticalParty, Election, Vote


class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name', 'number']


class PoliticalPartyAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ElectionAdmin(admin.ModelAdmin):
    list_filter = ['job', 'state']


class VoteAdmin(admin.ModelAdmin):
    list_filter = ['election']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(PoliticalParty, PoliticalPartyAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Vote, VoteAdmin)
