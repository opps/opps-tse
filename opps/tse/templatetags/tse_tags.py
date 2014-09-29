# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Library
from django.db.models import Q

from opps.tse.models import Election, Candidate, Vote

register = Library()


@register.simple_tag(takes_context=True)
def get_election(context, **kwargs):
    """
    {% load tse_tags %}
    {% get_election 'g' 'mg' '1' %}
    """
    election = Election.objects.get(**kwargs)
    return election


@register.simple_tag(takes_context=True)
def get_candidate(context, **kwargs):
    """
    {% load tse_tags %}
    {% get_candidate 'dilma' %}
    """
    return Candidate.objects.get(**kwargs)


@register.assignment_tag()
def get_candidates(**kwargs):
    """
    Retorna a lista de candidatos de acordo
    com os parametos nomeados
    """
    return Candidate.objects.filter(
        vote__election__job=kwargs.get('job', '')
    )
