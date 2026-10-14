from django.db.models import Aggregate, CharField


class GroupConcat(Aggregate):
    """Database agnostic 'GROUP_CONCAT'."""
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct_)s%(expressions)s%(ordering)s%(separator)s)'

    def __init__(self, expressions, distinct_=False, ordering=None, separator=',', **extra):
        super().__init__(
            expressions,
            distinct_='DISTINCT ' if distinct_ else '',
            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
            separator=(", '%s'" % separator) if separator != ',' else '',
            output_field=CharField(),
            **extra
        )

    def as_mysql(self, compiler, connection, separator=',', **extra_context):
        """Version for MySQL/MariaDB."""
        return super().as_sql(
            compiler, 
            connection, 
            separator=" SEPARATOR '%s'" % separator,
            **extra_context
        )


# For PostgreSQL, we might just alias `StringAgg`:
#
# from django.contrib.postgres.aggregates import StringAgg
#
# GroupConcat = StringAgg
