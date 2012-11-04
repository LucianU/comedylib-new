from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from comedyhub.mixins import CreatedMixin

class Collection(CreatedMixin):
    ROLE_CHOICES = (
        (0, u'comedian'),
        (1, u'show'),
        (2, u'movie'),
    )
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='collections')
    description = models.TextField()
    connections = models.ManyToManyField('self', related_name='connections',
                                         blank=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES)
    slug = models.SlugField(max_length=100, blank=True)

    def __unicode__(self):
        return u"%s:%s" % (self.name, self.get_role_display())

    @models.permalink
    def get_absolute_url(self):
        return ('content:%s' % self.get_role_display(), (self.slug, self.id))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

class Video(CreatedMixin):
    title = models.CharField(max_length=255)
    url = models.URLField()
    duration = models.CharField(max_length=20,
                                help_text='Format hh:mm:ss or mm:ss')
    views = models.IntegerField(default=0)
    collection = models.ForeignKey(Collection, related_name='videos')
    picture = models.ImageField(upload_to='videos', null=True, blank=True)

    class Meta:
        ordering =['-created']

    def __unicode__(self):
        return u"%s:%s" % (self.title, "%s..." % self.url[:50]
                           if len(self.url) > 50 else self.url)

    def get_absolute_url(self):
        coll_url = reverse('content:%s' % self.collection.get_role_display(),
                           args=[self.collection.slug, self.collection.id])
        return '%s/%s' % (coll_url, self.id)
