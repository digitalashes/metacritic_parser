from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Platform(models.Model):
    name = models.CharField(
        _('Platform'), max_length=64,
        help_text=_('Platform name.')
    )

    class Meta:
        verbose_name = _('Platform')
        verbose_name_plural = _('Platforms')
        ordering = ('name',)
        indexes = (
            models.Index(fields=['name']),
        )

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    platform = models.ForeignKey(
        to=Platform, on_delete=models.CASCADE,
        verbose_name=_('Platform'), related_name='games',
        help_text=_('Platform name.')
    )
    title = models.CharField(
        _('Title'), max_length=128,
        help_text=_('Game name.')
    )
    score = models.PositiveIntegerField(
        _('Score'), default=0,
        help_text=_('Game score.')
    )

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        ordering = ('title',)
        indexes = (
            models.Index(fields=['platform', 'title', 'score', 'created']),
        )

    def __str__(self):
        return f'{self.title.capitalize()} (Platform: {self.platform.name})'
