from django.core.cache import cache
from .models import Project 

CACHE_TTL = 60 * 60 

def get_project_stats():
  total = cache.get('total_projects')
  if not total:
    total = Project.objects.count()
    cache.set('total_projects', total, CACHE_TTL)

  active = cache.get('active_projects')
  if not active:
    active = Project.objects.filter(status='Active').count()
    cache.set('active_projects', active, CACHE_TTL)

  return {'total': total, 'active': active}
