# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Library
from django.core.urlresolvers import reverse

from opps.tse.models import Election, Candidate

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


@register.simple_tag()
def get_channel_url_state(**kwargs):
    """
    Retorna o reverse do channel long slug
    concatenado com o estado
    """
    return reverse(
        'eleicoes:apuracao-estado',
        kwargs={
            'channel__long_slug': 'noticias/brasil/politica/eleicoes2014/'
                                  'apuracao',
            'uf': kwargs.get('state')
        }
    )


@register.simple_tag()
def get_channel_result_president(**kwargs):
    """
    Retorna o reverse do channel long slug
    concatenado com o estado
    """
    return reverse(
        'eleicoes:eleicao-resultado-presidente',
        kwargs={
            'channel__long_slug': 'noticias/brasil/politica/eleicoes2014/'
                                  'resultado-geral',
        }
    )


@register.simple_tag()
def get_channel_url_complete_result(**kwargs):
    """
    Retorna o reverse do channel long slug
    concatenado com o estado
    """
    return reverse(
        'eleicoes:eleicao-resultado-estado-cargo',
        kwargs={
            'channel__long_slug': 'noticias/brasil/politica/eleicoes2014/resultado-geral',
            'uf': kwargs.get('state'),
            'jobs': kwargs.get('jobs'),
        }
    )
