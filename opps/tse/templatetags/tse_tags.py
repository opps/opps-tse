# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from opps.tse.models import Election, Candidate

register = template.Library()


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
    candidate = Candidate.objects.get(**kwargs)
    return candidate
